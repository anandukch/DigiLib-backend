from bson import ObjectId
from app.books.crud import get_book, get_book_item
from app.common import BaseCrud
from app.db import BookTransactions, User


class UserCrud(BaseCrud):
    def __init__(self):
        super().__init__(User)

    def get_non_verified(self):
        return list(self.db.find({"verified": False, "active": True}))

    def verify(self, user_id: str):
        return self.update({"_id": ObjectId(user_id)}, {"verified": True})

    def get_transactions(self, user_id: str):
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
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
                                "fine": 1,
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
                                "fine": 1,
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
        return list(BookTransactions.aggregate(pipeline))

    def search(self, adm_no: str = None):
        return list(
            self.db.find(
                {
                    # "name": {"$regex": name, "$options": "i"},
                    "adm_no": {"$regex": adm_no, "$options": "i"},
                    "active": True,
                },
            )
        )

    def soft_delete(self, user_id: str):
        return self.update({"_id": ObjectId(user_id)}, {"active": False})

    def get_active(self):
        return list(self.db.find({"active": True}))


userCrud = UserCrud()
