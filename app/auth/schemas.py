from typing import Optional
from click import Option
from pydantic import BaseModel, EmailStr, constr

from app.users.schemas import UserBaseSchema


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    verified: bool = False
    role: constr(min_length=1)


class StudentCreateSchema(UserBaseSchema):
    # adm_no: str
    semester: int



class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
