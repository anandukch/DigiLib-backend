from bson import ObjectId
from app.common import BaseCrud
from app.db import BookTransactions, User


class UserCrud(BaseCrud):
    def __init__(self):
        super().__init__(User)

    def get_transactions(self, user_id:str):
        return list(BookTransactions.find({"user_id": ObjectId(user_id)}))


userCrud = UserCrud()
