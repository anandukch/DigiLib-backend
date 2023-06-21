
from typing import Collection
from pymongo.collection import Collection
from app.common import BaseCrud
from app.db import Notifications


class NotificationCrud(BaseCrud):
  def __init__(self):
    super().__init__(Notifications)
    

    
  