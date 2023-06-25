from functools import wraps
from fastapi import HTTPException, status


def exception_handler(message: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if type(e) == HTTPException:
                    raise e
                else:
                    print(e)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=message
                    )

        return wrapper

    return decorator
