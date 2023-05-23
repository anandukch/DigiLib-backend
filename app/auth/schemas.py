from typing import Optional
from click import Option
from pydantic import BaseModel, EmailStr, constr

from app.users.schemas import UserBaseSchema



class CreateUserSchema(UserBaseSchema):
    adm_no:Optional[str]
    semester:Optional[int]
    branch:Optional[str]
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False
    role:str

class StudentCreateSchema(UserBaseSchema):
    adm_no:str
    semester:int
    branch:str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str
