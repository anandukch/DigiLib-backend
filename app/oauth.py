from bson import ObjectId
from jose import jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from app.db import User
from app.serializers.users import userResponseEntity

oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/login")
# from app.settings import ALGORITHM, SECRET_KEY
ALGORITHM = "HS256"
SECRET_KET = "secret"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(weeks=4)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KET, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth_schema)):
    payload = verify_token(token)
    user = User.find_one({"_id": ObjectId(payload.get("id"))})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return userResponseEntity(user,payload.get("role"))
