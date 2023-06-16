from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, status
from app.auth.endpoint import auth_router
from app.books.endpoint import book_router
from app.users.endpoints import user_router
from app.library.endpoints import library_router

from fastapi.middleware.cors import CORSMiddleware
import app.db

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()
# @app.on_event("startup")
# async def startup_event():
#     """
#     Startup event
#     """
#     try:
#         print("Connecting to database")
#     except Exception as e:
#         print(e)


@api_router.get("/", status_code=200)
async def root() -> dict:
    """
    Root GET
    """
    return {"message": "Hello World"}


@api_router.delete("/delete")
async def seed():
    """
    Seed database
    """
    try:
        app.db.User.delete_many({})
        app.db.Book.delete_many({})
        app.db.Author.delete_many({})
        return {"message": "Database seeded"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error seeding database"
        )


origins = ["http://localhost:5173", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(book_router, prefix="/books")
api_router.include_router(user_router, prefix="/users")
api_router.include_router(library_router, prefix="/library")
app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
