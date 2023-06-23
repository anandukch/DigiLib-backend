from datetime import datetime
from fastapi import APIRouter, Depends
from app.common import UserRoles

from app.notifications.cruds import NotificationCrud
from app.notifications.schemas import NotificationSchema
from app.oauth import get_current_user
from app.serializers.notifications import notificationListResponseEntity, notificationResponseEntity
from app.utils import role_decorator

notification_router = APIRouter()
notification_crud = NotificationCrud()

@notification_router.get("/")
@role_decorator(
    [UserRoles.ADMIN, UserRoles.FACULITY, UserRoles.STUDENT, UserRoles.ISSUER]
)
def get_notifications(user=Depends(get_current_user)):
    return notificationListResponseEntity(list(notification_crud.get_by_user(user)))


@notification_router.post("/")
def create_notification(notification: NotificationSchema , user=Depends(get_current_user)):
    
    notification_data = notification.dict()
    notification_data["sender_id"] = user["id"]
    notification_data["created_at"]=datetime.utcnow()
    notification_data["is_read"]=False
    notification_crud.create(notification_data)
    return "success"


@notification_router.put("/{notification_id}")
def update_notification(notification_id: str, status: str):
    return "success"
