from bson import ObjectId
from app.books.crud import get_book, get_book_item
from app.common import BaseCrud
from app.db import BookTransactions, User


class UserCrud(BaseCrud):
    def __init__(self):
        super().__init__(User)

    def get_non_verified(self):
        user= self.db.find({"verified": False})
        print(user)

    def get_transactions(self, user_id: str):
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
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
                    "fine": 1,
                    "issued_by": 1,
                    "date_of_reservation": 1,
                }
            },
        ]
        book_transactions = list(BookTransactions.aggregate(pipeline))
        return book_transactions


userCrud = UserCrud()
