from fastapi import FastAPI, APIRouter
from app.auth.endpoint import auth_router
from app.db import init_db
from app.models.user import Student, User

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@app.on_event("startup")
async def startup_event():
    """
    Startup event
    """
    try:
        await init_db()
        print("database connected")
    except Exception as e:
        print(e)


@api_router.get("/", status_code=200)
async def root() -> dict:
    """
    Root GET
    """
    new_user=Student(email="test@gmail.com",password="test",name="name",year_of_passing=2023,branch="cse",roll_no="12")
    try:
        await Student.insert_one(new_user)
    except Exception as e:
        return e
    return {"msg": new_user}


app.include_router(auth_router, prefix="/auth")
app.include_router(api_router,prefix='/api')

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
