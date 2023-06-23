
from typing import Collection
from bson import ObjectId
from pymongo.collection import Collection
from app.common import BaseCrud
from app.db import Notifications


class NotificationCrud(BaseCrud):
  def __init__(self):
    super().__init__(Notifications)
    
  def get_by_user(self, user: dict):
    return self.db.find({
    "$or": [
        {"recipient_id": ObjectId(user["id"])},
        {"recipient_type": "all"}
    ]
})
    

    
  