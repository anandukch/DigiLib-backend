from enum import Enum

from bson import ObjectId


class UserRoleEnum(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    ISSUER = "issuer"
    STAFF = "staff"


class BookStatusEnum(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    ISSUED = "issued"
    LOST = "lost"
    DAMAGED = "damaged"


class BookTransactionStatusEnum(str, Enum):
    IN_QUEUE = "in_queue"
    RESERVED = "reserved"
    ISSUED = "issued"
    RETURNED = "returned"
    FINE_DUE = "fine_due"
    LOST = "lost"


class BookTransactionStatus:
    IN_QUEUE = "in_queue"
    RESERVED = "reserved"
    ISSUED = "issued"
    RETURNED = "returned"
    FINE_DUE = "fine_due"
    LOST = "lost"


class BookStatus:
    AVAILABLE = "available"
    RESERVED = "reserved"
    ISSUED = "issued"
    LOST = "lost"
    DAMAGED = "damaged"


class UserRoles:
    STUDENT = "student"
    ADMIN = "admin"
    ISSUER = "issuer"
    FACULITY = "faculity"


class BaseCrud:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.find({})

    def get(self, id: str):
        return self.db.find_one({"_id": ObjectId(id)})

    def create(self, data: dict):
        return self.db.insert_one(data)

    def update(self, condition: dict, data: dict):
        return self.db.update_one(condition, {"$set": data})

    def delete(self, id: str):
        return self.db.delete_one({"_id": ObjectId(id)})
