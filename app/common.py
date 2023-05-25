from enum import Enum


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
    STAFF = "staff"
