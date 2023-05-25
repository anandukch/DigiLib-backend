from datetime import datetime
from typing import List

from bson import ObjectId
from app.books.schemas import Author, AuthorDB, Book, BookDB, BookItem, BookTransaction
from app.common import BookStatus, BookTransactionStatus
from app.db import Authors, BookItems, BookQueue, BookTransactions, Books, Utils
from app.exception_handler import exception_handler
from app.serializers.books import (
    authorListResponseEntity,
    authorResposneEntity,
    bookListResponseEntity,
    bookResposneEntity,
)


def get_books():
    """
    Get all books
    """
    return bookListResponseEntity(list(Books.find({})))


def get_book(book_id: str) -> Book:
    """
    Get a book by id
    """
    return bookResposneEntity(Books.find_one({"_id": ObjectId(book_id)}))


def add_book(book: dict):
    """
    Add a book
    """
    book["available_copies"] = book["no_of_copies"]
    book["virtual_copies"] = book["no_of_copies"]
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
    book = get_book(book_id)
    if book["virtual_copies"] == 0:
        book_queue = BookQueue.find_one({"book_id": ObjectId(book_id)})
        if not book_queue:
            book_queue = BookQueue.insert_one(
                {"book_id": ObjectId(book_id), "queue": []}
            )
        if user["id"] in book_queue["queue"]:
            return {"message": "Book already in queue", "data": book}
        BookQueue.update_one(
            {"_id": ObjectId(book_queue["_id"])},
            {"$push": {"queue": user["id"]}},
        )
        bookTransaction = BookTransaction(
            book_id=ObjectId(book_id),
            user_id=ObjectId(user["id"]),
            status=BookTransactionStatus.IN_QUEUE,
            date_of_reservation=datetime.utcnow(),
        )
        BookTransactions.insert_one(bookTransaction.dict())
        return {"message": "Book not available resered", "data": book}
    else:
        book_item = BookItems.find_one(
            {"book_id": ObjectId(book_id), "status": BookStatus.AVAILABLE}
        )
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
        return book


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
        return {"message": "Book transaction not found"}
    if book_transaction["status"] == BookTransactionStatus.ISSUED:
        return {"message": "Book already issued"}
    if book_transaction["status"] == BookTransactionStatus.IN_QUEUE:
        return {"message": "Book not available"}
    book_item = BookItems.find_one({"_id": ObjectId(book_transaction["book_item_id"])})
    BookItems.update_one(
        {"_id": ObjectId(book_item["_id"])}, {"$set": {"status": BookStatus.ISSUED}}
    )
    book = Books.find_one({"_id": ObjectId(book_transaction["book_id"])})
    Books.update_one(
        {"_id": ObjectId(book_transaction["book_id"])},
        {"$set": {"available_copies": book["available_copies"] - 1}},
    )

    # check if book queue is empty
    book_queue = get_book_queue(book_transaction["book_id"])
    if book_queue:
        if len(book_queue["queue"]) > 0:
            BookQueue.update_one(
                {"_id": ObjectId(book_queue["_id"])},
                {"$pop": {"queue": -1}},
            )
            book_transaction = BookTransaction(
                book_id=ObjectId(book_transaction["book_id"]),
                user_id=ObjectId(book_queue["queue"][0]),
                status=BookStatus.RESERVED,
                date_of_reservation=datetime.utcnow(),
            )
            BookTransactions.insert_one(book_transaction.dict())

    return {
        "book": get_book(book_transaction["book_id"]),
        "book_item": book_item,
        "book_transaction": book_transaction,
    }
