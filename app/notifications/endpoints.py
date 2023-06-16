from fastapi import APIRouter


notification_router = APIRouter()


@notification_router.get("/")
async def get_notifications():
    return {"message": "Hello World"}
