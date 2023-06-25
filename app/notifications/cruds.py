from typing import Collection
from bson import ObjectId
from pymongo.collection import Collection
from app.common import BaseCrud
from app.db import Notifications


class NotificationCrud(BaseCrud):
    def __init__(self):
        super().__init__(Notifications)

    def get_by_user(self, user: dict):
        if user["role"] == "admin":
            return self.db.find({})
        return self.db.find(
            {
                "recipient_type": {"$in": [user["role"], "all"]},
            }
        )
