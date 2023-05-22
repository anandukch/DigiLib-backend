from fastapi import APIRouter, Depends
from app.auth.oauth import create_access_token, get_current_user

from app.auth.utils import role_decorator


auth_router = APIRouter()


@auth_router.post("/login")
def login(user_data: dict):
    auth_token = create_access_token(user_data)
    return {"msg": auth_token}


@auth_router.post("/check")
@role_decorator(["admin", "user"])
def check(current_user: str = Depends(get_current_user)):
    # auth_token = create_access_token(user_data)
    print(current_user)
    return {"msg": "check"}
