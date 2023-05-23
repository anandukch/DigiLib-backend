from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

from app.common import UserRoleEnum, UserRoles


class UserBaseSchema(BaseModel):
    name: str
    email: str
    role: UserRoleEnum = UserRoles.STUDENT
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
