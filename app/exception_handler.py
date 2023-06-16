
from functools import wraps
from fastapi import HTTPException, status


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            if type(e) == HTTPException:
                raise e
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e
                )

    return wrapper
