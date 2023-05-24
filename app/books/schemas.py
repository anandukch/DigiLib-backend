from ast import Str
from datetime import date, datetime
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from app.common import BookStatusEnum


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


# class CreateBook(BaseModel):
#     ISBN: str
#     title: str
#     language: str
#     subject: str
#     publisher: str
#     author: str


class BookItem(BaseModel):
    acc_no:int
    book_id: str
    status: BookStatusEnum
    date_of_purchase: date | None = None
    date_of_issue: date | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# class BookRequest(BaseModel):
#     book_id: ObjectId
#     user_id: ObjectId
#     status: str
#     date_of_request: date
#     date_of_issue: date

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}


class BookReturn(BaseModel):
    book_id: ObjectId
    user_id: ObjectId
    status: str
    date_of_return: date

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookTransaction(BaseModel):
    book_id: ObjectId
    user_id: ObjectId
    status: str
    date_of_issue: date
    date_of_return: date

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
