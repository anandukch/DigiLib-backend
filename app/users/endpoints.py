import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.common import UserRoles

from app.oauth import get_current_user
from app.serializers.book_trans import bookTransListEntity
from app.serializers.users import (
    userListEntity,
    userResponseEntity,
    userResponsesEntity,
)
from app.users.crud import userCrud
from app.utils import hash_password, role_decorator

user_router = APIRouter()


@user_router.get("/search")
def search_user(adm_no: str = None):
    # try:
    print(adm_no)
    users = userCrud.search(adm_no)
    return userResponsesEntity(users)


# except Exception as e:
#     print(e)
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail="Error searching user",
#         headers={"WWW-Authenticate": "Bearer"},
#     )


@user_router.get("/")
@role_decorator([UserRoles.ADMIN])
def get_users(user=Depends(get_current_user)):
    return userListEntity(userCrud.get_all())


@user_router.get("/profile")
@role_decorator(
    [UserRoles.STUDENT, UserRoles.FACULITY, UserRoles.ADMIN, UserRoles.ISSUER]
)
def get_user_profile(user=Depends(get_current_user)):
    user = userResponseEntity(userCrud.get(user.get("id")), user.get("role"))
    return {
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role"),
        "verified": user.get("verified"),
        "created_at": user.get("created_at"),
    }


@user_router.get("/transactions")
@role_decorator([UserRoles.STUDENT, UserRoles.FACULITY])
def get_user_transactions(user: dict = Depends(get_current_user)):
    # try:
    trans = userCrud.get_transactions(user_id=user.get("id"))
    return bookTransListEntity(trans)


# except Exception as e:
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Error getting transactions",
#         headers={"WWW-Authenticate": "Bearer"},
#     )


@user_router.get("/nonverified")
@role_decorator([UserRoles.ADMIN])
def get_non_verified_users(user=Depends(get_current_user)):
    users = userCrud.get_non_verified()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return userListEntity(users)


@user_router.post("/verify/{user_id}")
@role_decorator([UserRoles.ADMIN])
def verify_user(user_id: str, user=Depends(get_current_user)):
    try:
        userCrud.verify(user_id)
        return {"message": "User verified"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error verifying user",
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.get("/{user_id}")
def get_user(user_id: str, user=Depends(get_current_user)):
    return userResponseEntity(userCrud.get(user_id))


@user_router.post("/")
@role_decorator([UserRoles.ADMIN])
def create_user(userData: dict, user=Depends(get_current_user)):
    try:
        userCrud.create(
            {
                "name": userData.get("name"),
                "email": userData.get("email"),
                "password": hash_password(userData.get("password")),
                "role": userData.get("role"),
                "verified": True,
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            }
        )
        return {"message": "User created"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user",
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.delete("/{user_id}")
@role_decorator([UserRoles.ADMIN])
def delete_user(user_id: str, user=Depends(get_current_user)):
    try:
        userCrud.delete(user_id)
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting user",
            headers={"WWW-Authenticate": "Bearer"},
        )
