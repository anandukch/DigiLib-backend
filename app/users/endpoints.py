from fastapi import APIRouter, Depends, HTTPException, status
from app.common import UserRoles

from app.oauth import get_current_user
from app.serializers.book_trans import bookTransListEntity
from app.serializers.users import userListEntity, userResponseEntity
from app.users.crud import userCrud
from app.utils import role_decorator

user_router = APIRouter()


@user_router.get("/")
@role_decorator([UserRoles.ADMIN])
def get_users(user=Depends(get_current_user)):
    return userListEntity(userCrud.get_all())


@user_router.get("/profile")
@role_decorator([UserRoles.STUDENT, UserRoles.FACULITY, UserRoles.ADMIN])
def get_user_profile(user: dict = Depends(get_current_user)):
    return userResponseEntity(userCrud.get(user.get("id")), user.get("role"))


@user_router.get("/transactions")
@role_decorator([UserRoles.STUDENT, UserRoles.FACULITY])
def get_user_transactions(user: dict = Depends(get_current_user)):
    try:
        trans = userCrud.get_transactions(user_id=user.get("id"))

        return bookTransListEntity(trans)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error getting transactions",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
