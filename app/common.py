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
