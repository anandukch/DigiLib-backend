from fastapi import APIRouter

from app.notifications.cruds import NotificationCrud


notification_router = APIRouter()
notification_crud = NotificationCrud()


@notification_router.get("/")
def get_notifications():
    return notification_crud.get_all()


@notification_router.post("/")
def create_notification(notification):
    return notification_crud.create(notification)


@notification_router.put("/{notification_id}")
def update_notification(notification_id: str, status: str):
    return "success"
