from functools import wraps

from fastapi import HTTPException

def role_decorator(role: list):
    """_summary_

    Args:
        role (list): _description_
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs["user"]
            if current_user["role"] in role:
                return func(*args, **kwargs)
            else:
                raise HTTPException(
                    status_code=403,
                    detail="You don't have permission to access this resource",
                )

        return wrapper

    return decorator


from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, BASE_PATH, SECRET_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password, hashed_password):
    """
    Verify plain password against hashed
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    """
    Create hashed password
    """
    return pwd_context.hash(password)


# def create_access_token(user_id):
#     """
#     Create a JWT Access Token with user_id
#     """
#     to_encode = {"sub": str(user_id)}
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def decode_token(token):
#     """
#     Decode subject from JWT Token
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         return user_id
#     except JWTError:
#         return None


