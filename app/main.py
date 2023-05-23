from fastapi import FastAPI, APIRouter, Request, Response
from app.auth.endpoint import auth_router
# from app.db import init_db
import app.db

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@app.on_event("startup")
async def startup_event():
    """
    Startup event
    """
    try:
        print("Connecting to database")
    except Exception as e:
        print(e)


@api_router.get("/", status_code=200)
async def root() -> dict:
    """
    Root GET
    """

    return {"message": "Hello World"}


app.include_router(auth_router, prefix="/auth")
app.include_router(api_router,prefix='/api')


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
