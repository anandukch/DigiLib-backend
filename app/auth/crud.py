from app.auth.utils import verify_password
from app.models.user import User


def login_user(user_data: dict):
    """
    Login user
    """
    user = User.get(email=user_data["email"])
    if user and verify_password(user_data["password"], user.password):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
