from datetime import datetime, timedelta
from os import stat
from typing import List

from bson import ObjectId
from click import File
from fastapi import HTTPException, UploadFile, status
from app.books.schemas import Author, AuthorDB, Book, BookDB, BookItem, BookTransaction
from app.common import BaseCrud, BookStatus, BookTransactionStatus
from app.cron_tasks import calculate_fine_dues
from app.db import Authors, BookItems, BookQueue, BookTransactions, Books, Utils
from app.library.crud import LibraryCrud
from app.serializers.book_trans import bookTransListEntity
from app.serializers.books import (
    authorListResponseEntity,
    authorResposneEntity,
    bookItemEntity,
    bookItemsEntity,
    bookListResponseEntity,
    bookResposneEntity,
)

libraryCrud = LibraryCrud()


def get_books():
    """
    Get all books
    """
    Books.find({}).skip(0).limit(10)
    return bookListResponseEntity(list(Books.find({})))


def get_book(book_id: str) -> Book:
    """
    Get a book by id
    """
    return bookResposneEntity(
        Books.find_one({"_id": ObjectId(book_id)}, sort=[("_id", -1)])
    )


def upload_file(file: UploadFile = File(...)):
    print(file.filename)
    return {"filename": file.filename}


def add_book(book: dict):
    """
    Add a book
    """
    if book["image"] == "":
        raise HTTPException(
            status_code=400, detail="Image is required for adding a book"
        )
    book["available_copies"] = book["no_of_copies"]
    book["virtual_copies"] = book["no_of_copies"]

    if not Utils.find_one({"name": "subjects"}):
        Utils.insert_one({"name": "subjects", "value": []})
    if book["subject"] not in Utils.find_one({"name": "subjects"})["value"]:
        Utils.update_one(
            {
                "name": "subjects",
            },
            {
                "$push": {"value": book["subject"]},
            },
        )

    new_book = Books.insert_one(book)
    acc_no = 1000
    if not Utils.find_one({"name": "acc_no"}):
        Utils.insert_one({"name": "acc_no", "value": acc_no})
    else:
        acc_no = Utils.find_one({"name": "acc_no"})["value"]
    for i in range(book["no_of_copies"]):
        bookItem = BookItem(
            acc_no=acc_no, book_id=new_book.inserted_id, status=BookStatus.AVAILABLE
        )
        BookItems.insert_one(bookItem.dict())
        acc_no += 1
        Utils.update_one({"name": "acc_no"}, {"$set": {"value": acc_no}})

    return get_book(new_book.inserted_id)


def add_author(author: Author) -> Author:
    """
    Add an author
    """
    new_author = Authors.insert_one(author.dict())
    return get_author(new_author.inserted_id)


def get_author(author_id: str):
    """
    Get an author by id
    """
    return authorResposneEntity(Authors.find_one({"_id": ObjectId(author_id)}))


def get_authors() -> List[AuthorDB]:
    return authorListResponseEntity(list(Authors.find({})))


def reserve_book(book_id: str, user: dict):
    """
    Reserve a book
    """
    book_trans = BookTransactions.find_one(
        {
            "book_id": ObjectId(book_id),
            "user_id": ObjectId(user["id"]),
            "status": {"$ne": BookTransactionStatus.RETURNED},
        }
    )
    if book_trans:
        if book_trans["status"] == BookTransactionStatus.RESERVED:
            raise HTTPException(
                status_code=400,
                detail="Book already reserved",
            )
        elif book_trans["status"] == BookTransactionStatus.ISSUED:
            raise HTTPException(
                status_code=400,
                detail="Book already issued",
            )
        elif book_trans["status"] == BookTransactionStatus.IN_QUEUE:
            raise HTTPException(
                status_code=400,
                detail="Book already in queue",
            )
        # else:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Book already returned",
        #     )

    book_item = BookItems.find_one(
        {"book_id": ObjectId(book_id), "status": BookStatus.AVAILABLE}
    )
    book = get_book(book_id)
    if book["virtual_copies"] == 0:
        book_queue = BookQueue.find_one({"book_id": ObjectId(book_id)})
        if not book_queue:
            book_queue = BookQueue.insert_one(
                {"book_id": ObjectId(book_id), "queue": [user["id"]]}
            )
        else:
            if user["id"] in book_queue["queue"]:
                raise HTTPException(
                    status_code=400,
                    detail="Book already in queue",
                )
            BookQueue.update_one(
                {"_id": ObjectId(book_queue["_id"])},
                {"$push": {"queue": user["id"]}},
            )
        bookTransaction = BookTransaction(
            book_id=ObjectId(book_id),
            user_id=ObjectId(user["id"]),
            status=BookTransactionStatus.IN_QUEUE,
            date_of_reservation=datetime.utcnow(),
            fine=0,
        )
        BookTransactions.insert_one(bookTransaction.dict())
        return "Book added to queue"
    else:
        BookItems.update_one(
            {"_id": ObjectId(book_item["_id"])},
            {"$set": {"status": BookStatus.RESERVED}},
        )
        Books.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": {"virtual_copies": book["virtual_copies"] - 1}},
        )
        bookTransaction = BookTransaction(
            book_id=ObjectId(book_id),
            user_id=ObjectId(user["id"]),
            status=BookStatus.RESERVED,
            date_of_reservation=datetime.utcnow(),
            book_item_id=ObjectId(book_item["_id"]),
        )
        BookTransactions.insert_one(bookTransaction.dict())
        book["virtual_copies"] = book["virtual_copies"] - 1
        book_item["status"] = BookStatus.RESERVED
        return "Book reserved"


def get_book_queue(book_id: str):
    """
    Get book queue
    """
    book_queue = BookQueue.find_one({"book_id": ObjectId(book_id)})
    if not book_queue:
        return {"message": "Book queue not found"}
    book_queue["_id"] = str(book_queue["_id"])
    return book_queue


def issue_book(book_trans_id: str):
    book_transaction = BookTransactions.find_one({"_id": ObjectId(book_trans_id)})
    if not book_transaction:
        raise HTTPException(
            status_code=400,
            detail="Book transaction not found",
        )
    if book_transaction["status"] == BookTransactionStatus.ISSUED:
        return {"message": "Book already issued"}
    if book_transaction["status"] == BookTransactionStatus.IN_QUEUE:
        return {"message": "Book not available"}
    # book_item = BookItems.find_one({"_id": ObjectId(book_transaction["book_item_id"])})

    days_of_return = libraryCrud.get_lib_config()["days_of_return"]
    BookTransactions.update_one(
        {"_id": ObjectId(book_trans_id)},
        {
            "$set": {
                "status": BookTransactionStatus.ISSUED,
                "date_of_issue": datetime.utcnow(),
                "date_of_return": datetime.utcnow()
                + timedelta(days=int(days_of_return)),
            }
        },
    )
    BookItems.update_one(
        {"_id": ObjectId(book_transaction["book_item_id"])},
        {"$set": {"status": BookStatus.ISSUED}},
    )
    book = Books.find_one({"_id": ObjectId(book_transaction["book_id"])})
    Books.update_one(
        {"_id": ObjectId(book_transaction["book_id"])},
        {"$set": {"available_copies": book["available_copies"] - 1}},
    )
    return {
        "message": "Book issued",
    }


def get_reserved_books():
    """
    Get reserved books
    """
    return list(BookTransactions.find({"status": BookStatus.RESERVED}))


def get_book_transactions(bookId: str, type: str):
    """
    Get book transactions
    """
    params = {"book_id": ObjectId(bookId)}
    if type == "issued":
        params["status"] = BookStatus.ISSUED
    elif type == "returned":
        params["status"] = BookTransactionStatus.RETURNED
    return bookTransListEntity(list(BookTransactions.find(params)))


def get_book_trans(book_trans_id: str):
    return BookTransactions.find_one({"_id": ObjectId(book_trans_id)})


def return_book(book_trans_id: str):
    book_trans = bookTransactionsCrud.get(book_trans_id)
    if not book_trans:
        raise HTTPException(
            status_code=400,
            detail="Book transaction not found",
        )
    book_item = BookItems.find_one({"_id": ObjectId(book_trans["book_item_id"])})
    if not book_item:
        raise HTTPException(
            status_code=400,
            detail="Book item not found",
        )
    BookItems.update_one(
        {"_id": ObjectId(book_item["_id"])}, {"$set": {"status": BookStatus.AVAILABLE}}
    )

    Books.update_one(
        {"_id": ObjectId(book_item["book_id"])},
        {"$inc": {"available_copies": 1, "virtual_copies": 1}},
    )

    BookTransactions.update_one(
        {"_id": ObjectId(book_trans_id)},
        {
            "$set": {
                "status": BookTransactionStatus.RETURNED,
                "actual_date_of_return": datetime.utcnow(),
            }
        },
    )

    book_queue = BookQueue.find_one({"book_id": ObjectId(book_item["book_id"])})
    if book_queue:
        if len(book_queue["queue"]) > 0:
            BookItems.update_one(
                {"_id": ObjectId(book_item["_id"])},
                {"$set": {"status": BookStatus.RESERVED}},
            )
            book = Books.find_one({"_id": ObjectId(book_item["book_id"])})
            Books.update_one(
                {"_id": ObjectId(book_item["book_id"])},
                {"$set": {"virtual_copies": book["virtual_copies"] - 1}},
            )
            bookTransactionsCrud.update(
                {
                    "user_id": ObjectId(book_queue["queue"][0]),
                    "book_id": ObjectId(book_item["book_id"]),
                    "status": BookTransactionStatus.IN_QUEUE,
                },
                {
                    "book_item_id": ObjectId(book_item["_id"]),
                    "status": BookTransactionStatus.RESERVED,
                },
            )

            book_queue["queue"].pop(0)
            bookQueueCrud.update({"_id": ObjectId(book_queue["_id"])}, book_queue)

    return {
        "message": "Book returned",
    }


def get_all_book_transactions():
    pipeline = [
        {
            "$facet": {
                "book_transactions": [
                    {
                        "$lookup": {
                            "from": "books",
                            "localField": "book_id",
                            "foreignField": "_id",
                            "as": "book",
                        }
                    },
                    {"$unwind": "$book"},
                    {
                        "$lookup": {
                            "from": "users",
                            "localField": "user_id",
                            "foreignField": "_id",
                            "as": "user",
                        }
                    },
                    {"$unwind": "$user"},
                    {
                        "$lookup": {
                            "from": "book_items",
                            "localField": "book_item_id",
                            "foreignField": "_id",
                            "as": "book_item",
                        }
                    },
                    {"$unwind": "$book_item"},
                    {
                        "$project": {
                            "book": "$book",
                            "book_item": "$book_item",
                            "id": "$_id",
                            "book_id": 1,
                            "user": "$user",
                            "status": 1,
                            "date_of_return": 1,
                            "date_of_issue": 1,
                            "actual_date_of_return": 1,
                            # "fine": 1,
                            "issued_by": 1,
                            "date_of_reservation": 1,
                        }
                    },
                ],
                "in_queue_transactions": [
                    {"$match": {"status": "in_queue"}},
                    {
                        "$lookup": {
                            "from": "books",
                            "localField": "book_id",
                            "foreignField": "_id",
                            "as": "book",
                        }
                    },
                    {"$unwind": "$book"},
                    {
                        "$lookup": {
                            "from": "users",
                            "localField": "user_id",
                            "foreignField": "_id",
                            "as": "user",
                        }
                    },
                    {"$unwind": "$user"},
                    {
                        "$project": {
                            "book": "$book",
                            "book_item": None,
                            "id": "$_id",
                            "book_id": 1,
                            "user": "$user",
                            "status": 1,
                            "date_of_return": 1,
                            "date_of_issue": 1,
                            "actual_date_of_return": 1,
                            # "fine": 1,
                            "issued_by": 1,
                            "date_of_reservation": 1,
                        }
                    },
                ],
            }
        },
        {
            "$project": {
                "transactions": {
                    "$concatArrays": [
                        "$book_transactions",
                        "$in_queue_transactions",
                    ]
                }
            }
        },
        {"$unwind": "$transactions"},
        {"$replaceRoot": {"newRoot": "$transactions"}},
        {"$sort": {"_id": -1}},
    ]
    book_trans = list(BookTransactions.aggregate(pipeline))
    fine_rate = libraryCrud.get_lib_config()["fine_rate"]
    for i in range(len(book_trans)):
        book_tran = book_trans[i]
        delay = ""
        fine = 0
        if book_tran["date_of_return"] is not None:
            if book_tran["actual_date_of_return"] is not None:
                delay = book_tran["actual_date_of_return"] - book_tran["date_of_return"]
                if delay.days > 0:
                    fine = delay.days * fine_rate
            else:
                delay = datetime.utcnow() - book_tran["date_of_return"]

                if delay.days > 0:
                    fine = delay.days * fine_rate
        book_trans[i]["fine"] = fine
        # bookTransactionsCrud.update(
        #     {
        #         "_id": ObjectId(book_tran["id"]),
        #     },
        #     {
        #         "fine": fine,
        #     },
        # )

    return book_trans


def get_book_item(book_item_id: str):
    book_item = BookItems.find_one({"_id": ObjectId(book_item_id)})
    if not book_item:
        raise HTTPException(
            status_code=400,
            detail="Book item not found",
        )
    book_item["_id"] = str(book_item["_id"])
    return book_item


# def immediate_issue(book_id: dict, user_id: dict):
#     book = get_book(book_id)
#     if not book:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
#         )
#     book_item = bookItemsCrud.get_by_status(book_id, BookStatus.AVAILABLE)
#     if not book_item:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Book not available"
#         )

#     days_of_return = libraryCrud.get_lib_config()["days_of_return"]
#     book_trans = BookTransaction(
#         book_id=ObjectId(book_id),
#         book_item_id=ObjectId(book_item["_id"]),
#         date_of_issue=datetime.utcnow(),
#         user_id=ObjectId(user_id),
#         status=BookStatus.ISSUED,
#         date_of_reservation=datetime.utcnow(),
#         date_of_return=datetime.utcnow() + timedelta(days=int(days_of_return)),
#     )
#     bookTransactionsCrud.create(book_trans.dict())
#     bookItemsCrud.update(
#         {"_id": ObjectId(book_item["_id"])}, {"status": BookStatus.ISSUED}
#     )
#     Books.update_one(
#         {"_id": ObjectId(book_id)},
#         {"$inc": {"available_copies": -1, "virtual_copies": -1}},
#     )
#     return {
#         "message": "Book issued",
#     }

from app.models.index import get_popular_books


class BookCrud(BaseCrud):
    def __init__(self):
        super().__init__(Books)

    def search(self, query: str):
        books = self.db.find(
            {
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"author": {"$regex": query, "$options": "i"}},
                    {"publisher": {"$regex": query, "$options": "i"}},
                ]
            }
        )
        return list(books)

    def immediate_issue(self, data: dict):
        book = get_book(data["book_id"])

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        book_item = bookItemEntity(bookItemsCrud.get_by_acc_no(data["acc_no"]))
        if not book_item or book_item["status"] != BookStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not available"
            )

        # check if book is already issued to user
        prev_book_trans = bookTransactionsCrud.get_by_book_id_and_user_id(
            data["book_id"], data["user_id"]
        )
        if prev_book_trans:
            if prev_book_trans["status"] == BookTransactionStatus.ISSUED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book already issued to user",
                )

            if prev_book_trans["status"] == BookTransactionStatus.RESERVED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book already reserved by user",
                )

            if prev_book_trans["status"] == BookTransactionStatus.IN_QUEUE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book already in queue by user",
                )

        days_of_return = libraryCrud.get_lib_config()["days_of_return"]
        book_trans = BookTransaction(
            book_id=ObjectId(data["book_id"]),
            book_item_id=ObjectId(book_item["id"]),
            date_of_issue=datetime.utcnow(),
            user_id=ObjectId(data["user_id"]),
            status=BookStatus.ISSUED,
            date_of_reservation=datetime.utcnow(),
            date_of_return=datetime.utcnow() + timedelta(days=int(days_of_return)),
        )
        bookTransactionsCrud.create(book_trans.dict())
        bookItemsCrud.update(
            {"_id": ObjectId(book_item["id"])},
            {"status": BookStatus.ISSUED, "acc_no": data["acc_no"]},
        )
        Books.update_one(
            {"_id": ObjectId(data["book_id"])},
            {"$inc": {"available_copies": -1, "virtual_copies": -1}},
        )
        return {
            "message": "Book issued",
        }

    def get_subjects(self):
        return Utils.find_one({"name": "subjects"})["value"]


class BookRecommendationCrud:
    def __init__(self):
        pass

    def get_popular_books(self):
        popular_df = get_popular_books()
        book_name = (list(popular_df["Book-Title"].values),)
        author = (list(popular_df["Book-Author"].values),)
        image = (list(popular_df["Image-URL-M"].values),)
        votes = (list(popular_df["num_ratings"].values),)
        rating = list(popular_df["avg_rating"].values)

        # rend as a json resposne to the client but format it in an array of objects
        # print(book_name[0])
        book_obj = []
        for i in range(len(book_name[0])):
            book_obj.append(
                {
                    "book_name": book_name[0][i],
                    "author": author[0][i],
                    "image": image[0][i],
                }
            )
        # print(book_obj)
        return book_obj

    def get_books(self, title: str):
        from app.models.index import get_book_by_title

        book = get_book_by_title(title)
        return {
            "book_name": book["Book-Title"].values[0],
            "author": book["Book-Author"].values[0],
            "image": book["Image-URL-M"].values[0],
        }

    def recommend_books(self, values: list):
        try:
            from app.models.index import recommend_books
            if all(v == 0 for v in values):
                return []
            books, extra_books = recommend_books(values)
            # print(books)

            # if not books:
            #     return []
            
            # print(list(books["BOOK"].values),)

            book_name = (list(books["BOOK"].values),)
            # author = (list(books["Book-Author"].values),)
            classes = (list(books["CLASS"].values),)
            image = (list(books["img"].values),)

            # print(book_name[0][:10])

            # rend as a json resposne to the client but format it in an array of objects
            book_obj = []
            for i in range(len(book_name[0])):
                book_obj.append(
                    {
                        "book_name": book_name[0][i],
                        "class": classes[0][i],
                        "image": image[0][i],
                    }
                )

            # print(book_obj)

            extra_book_obj = []
            # print(extra_books)
            
            if len(extra_books) > 0:
                # extra_books = extra_books[0]
                    
                # if not extra_books.empty:
                for extra_book in extra_books:
                    print(extra_book)
                    extra_book_name = (list(extra_book["BOOK"].values),)
                    # print(extra_book_name)

                    #     # extra_author = (list(extra_books["Book-Author"].values),)
                    extra_classes = (list(extra_book["CLASS"].values),)
                    extra_image = (list(extra_book["img"].values),)
                    for i in range(len(extra_book)):
                        # print(extra_book_name[0][i])
                        extra_book_obj.append(
                            {
                                "book_name": extra_book_name[0][i],
                                "class": extra_classes[0][i],
                                "image": extra_image[0][i],
                            }
                        )
            # print(extra_book_obj)
            new_books = book_obj + extra_book_obj
            return new_books
        except Exception as e:
            # print(e)
            raise e


class BookQueueCrud(BaseCrud):
    def __init__(self):
        super().__init__(BookQueue)

    pass


bookQueueCrud = BookQueueCrud()


class BookTransactionsCrud(BaseCrud):
    def __init__(self):
        super().__init__(BookTransactions)

    def get_by_book_id_and_user_id(self, book_id: str, user_id: str):
        return self.db.find_one(
            {
                "book_id": ObjectId(book_id),
                "user_id": ObjectId(user_id),
                "status": {"$ne": BookTransactionStatus.RETURNED},
            }
        )

    pass


bookTransactionsCrud = BookTransactionsCrud()


class BookItemsCrud(BaseCrud):
    def __init__(self):
        super().__init__(BookItems)

    def get_by_status(self, book_id: str, status: str):
        return self.db.find_one({"book_id": ObjectId(book_id), "status": status})

    def get_by_book_id(self, book_id: str):
        return self.db.find({"book_id": ObjectId(book_id)})

    def delete_by_book_id(self, book_id: str):
        self.db.delete_many({"book_id": ObjectId(book_id)})

    def get_by_acc_no(self, acc_no: int):
        return self.db.find_one({"acc_no": acc_no})


bookItemsCrud = BookItemsCrud()
