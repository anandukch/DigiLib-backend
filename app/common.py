from enum import Enum


class UserRoleEnum(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    ISSUER = "issuer"
    STAFF = "staff"


class UserRoles:
    STUDENT = "student"
    ADMIN = "admin"
    ISSUER = "issuer"
    STAFF = "staff"
    
user_roles = UserRoles()
