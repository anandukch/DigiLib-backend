from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.library.crud import library_crud
from app.common import UserRoles
from app.library.schemas import LibConfig
from app.oauth import get_current_user
from app.utils import role_decorator


library_router = APIRouter()


@library_router.get("/")
@role_decorator([UserRoles.ADMIN])
def get_library_config(user=Depends(get_current_user)):
    try:
        return library_crud.get_lib_config()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error"
        )


@library_router.post("/")
@role_decorator([UserRoles.ADMIN])
def create_library_config(payload: LibConfig, user=Depends(get_current_user)):
    try:
        library_crud.add_lib_config(payload)
        return Response(status_code=status.HTTP_201_CREATED,content="Library config created")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error"
        )
