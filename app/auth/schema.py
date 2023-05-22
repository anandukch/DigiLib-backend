from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


class Login(User):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
