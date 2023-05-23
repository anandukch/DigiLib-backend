from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.oauth import create_access_token, get_current_user
from app.auth.schemas import (
    CreateUserSchema,
    LoginUserSchema,
    StudentCreateSchema,
)
from app.utils import hash_password, role_decorator, verify_password
from app.db import User
from app.exception_handler import exception_handler
from app.serializers.users import userResponseEntity
from app.common import UserRoles
from app.users.schemas import UserResponse

auth_router = APIRouter()


@auth_router.post("/check")
@role_decorator(role=[UserRoles.ADMIN, UserRoles.STUDENT])
def check(current_user: str = Depends(get_current_user)):
    print(current_user)
    return {"msg": "check"}


@auth_router.post("/login")
# @exception_handler
def login(user_data: LoginUserSchema, res: Response) -> dict:
    db_user = User.find_one({"email": user_data.email.lower()})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials email",
        )
    if not verify_password(user_data.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials pass",
        )
    return {
        "status": "success",
        "access_token": create_access_token(
            {"id": str(db_user["_id"]), "role": db_user["role"]}
        ),
    }


@auth_router.post("/register")
def register(payload: CreateUserSchema):
    user = User.find_one({"email": payload.email.lower()})
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    if payload.role == UserRoles.STUDENT:
        try:
            if StudentCreateSchema.validate(payload):
                payload.adm_no = payload.adm_no.lower()
                payload.branch = payload.branch.lower()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors()
            )
    payload.password = hash_password(payload.password)
    del payload.passwordConfirm
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = userResponseEntity(User.find_one({"_id": result.inserted_id}),payload.role)
    return {"status": "success", "user": new_user}


@auth_router.delete("/delete")
def delete_all_users():
    User.delete_many({})
    return {"status": "success"}
