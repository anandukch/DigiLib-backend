from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class User(Document):
    name: str
    # age: int
    is_active: bool = True
    # role: str
    password: Optional[str] = None
    email: str
    # created_at: Optional[datetime] = datetime.now
    # updated_at: Optional[datetime] = datetime.now
    # deleted_at: Optional[datetime] = datetime.now

    class Settings:
        collection_name = "users"
        is_root = True


class Student(User):
    roll_no: Optional[str]
    year_of_passing: Optional[int]
    branch: Optional[str]

class Teacher(User):
    teacher_id: str

class Admin(User):
    admin_id: str

class Issuer(User):
    issuer_id: str
    issuer_type: str
    issuer_name: str
    issuer_address: str
