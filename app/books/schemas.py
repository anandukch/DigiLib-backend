from ast import Str
from datetime import date, datetime
from typing import Any, List
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from app.common import BookStatusEnum, BookTransactionStatus, BookTransactionStatusEnum


class Author(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class AuthorDB(Author):
    _id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Book(BaseModel):
    ISBN: str = Field(..., alias="ISBN")
    title: str = Field(..., alias="title")
    language: str = Field(..., alias="language")
    subject: str = Field(..., alias="subject")
    publisher: str = Field(..., alias="publisher")
    author: str = Field(..., alias="author")
    no_of_copies: int = Field(..., alias="no_of_copies")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookDB(Book):
    _id: str
    available_copies: int
    virtual_copies: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookItem(BaseModel):
    acc_no: int
    book_id: ObjectId
    status: BookStatusEnum
    date_of_purchase: date | None = None
    date_of_issue: date | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookTransaction(BaseModel):
    book_id: ObjectId
    book_item_id: ObjectId | None = None
    user_id: ObjectId
    status: BookTransactionStatusEnum = BookTransactionStatus.RESERVED
    date_of_reservation: datetime | None = None
    date_of_issue: datetime | None = None
    date_of_return: datetime | None = None
    actual_date_of_return: datetime | None = None
    fine: int | None = None
    issued_by: ObjectId | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookQueue(BaseModel):
    book_id: ObjectId
    queue: list

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
