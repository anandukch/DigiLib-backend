from datetime import date
from pydantic import BaseModel
from bson.objectid import ObjectId

class Author(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class Book(BaseModel):
    ISBN: str
    title: str
    language: str
    subject: str
    publisher: str
    author: ObjectId

    class Config:
        orm_mode=True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class BookItem(BaseModel):
  book_id:ObjectId
  status:str
  date_of_purchase:date
  date_of_issue:date
  class Config:
    orm_mode=True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class BookRequest(BaseModel):
  book_id:ObjectId
  user_id:ObjectId
  status:str
  date_of_request:date
  date_of_issue:date
  class Config:
    orm_mode=True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
      

class BookReturn(BaseModel):
  book_id:ObjectId
  user_id:ObjectId
  status:str
  date_of_return:date
  class Config:
    orm_mode=True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class BookTransaction(BaseModel):
  book_id:ObjectId
  user_id:ObjectId
  status:str
  date_of_issue:date
  date_of_return:date
  class Config:
    orm_mode=True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}