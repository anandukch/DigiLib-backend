# class BookCrud(BaseCrud):
#     def __init__(self, db):
#         super().__init__(db)

#     def get_transactions(self, book_id: str):
#         return list(BookTransactions.find({"book_id": ObjectId(book_id)}))

#     def get_queue(self, book_id: str):
#         return list(BookQueue.find({"book_id": ObjectId(book_id)}))

#     def get_book_items(self, book_id: str):
#         return list(BookItems.find({"book_id": ObjectId(book_id)}))

#     def get_book_item(self, acc_no: int):
#         return BookItems.find_one({"acc_no": acc_no})

#     def get_book_item_by_id(self, book_item_id: str):
#         return BookItems.find_one({"_id": ObjectId(book_item_id)})

#     def get_book_transaction(self, book_transaction_id: str):
#         return BookTransactions.find_one({"_id": ObjectId(book_transaction_id)})

#     def get_book_transaction_by_book_item_id(self, book_item_id: str):
#         return BookTransactions.find_one({"book_item_id": ObjectId(book_item_id)})

#     def get_book_transaction_by_user_id(self, user_id: str):
#         return BookTransactions.find_one({"user_id": ObjectId(user_id)})

#     def get_book_transaction_by_book_id(self, book_id: str):
#         return BookTransactions.find_one({"book_id": ObjectId(book_id)})

#     def create_book_item(self, book_item: BookItem):
#         return BookItems.insert_one(book_item.dict())

#     def create_book_transaction(self, book_transaction: BookTransaction):
#         return BookTransactions.insert_one(book_transaction.dict())

#     def create_book_queue(self, book_queue: BookQueue):
#         return BookQueue.insert_one(book_queue.dict())

#     def update_book_item(self, book_item: BookItem):
#         return BookItems.update_one(
#             {"_id": ObjectId(book_item.id)}, {"$set": book_item.dict()}
#         )

#     def update_book_transaction(self, book_transaction: BookTransaction):
#         return BookTransactions.update_one(
#             {"_id": ObjectId(book_transaction.id)}, {"$set": book_transaction.dict()}
#         )

#     def update_book_queue(self, book_queue: BookQueue):
#         return BookQueue.update_one(
#             {"_id": ObjectId(book_queue.id)}, {"$set": book_queue.dict()}
#         )

#     def delete_book_item(self, book_item_id: str):
#         return BookItems.delete_one({"_id": ObjectId(book_item_id)})

#     def delete_book_transaction(self, book_transaction_id: str):
#         return BookTransactions.delete_one({"_id": ObjectId(book_transaction_id)})

#     def delete_book_queue(self, book_queue_id: str):
#         return BookQueue.delete_one({"_id": ObjectId(book_queue_id)})

from app.common import BaseCrud
from app.db import User


class BookCrud(BaseCrud):
    def __init__(self):
        super().__init__(User)


