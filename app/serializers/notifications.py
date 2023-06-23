def notificationResponseEntity(notification):
    return {
        "id": str(notification["_id"]),
        "recipient_id": str(notification["recipient_id"]),
        "sender_id": str(notification["sender_id"]),
        "recipient_type": str(notification["recipient_type"]),
        "text": notification["text"],
        "created_at": str(notification["created_at"]),
        "is_read": notification["is_read"],
        "time": notification["time"]
    }
    
    
def notificationListResponseEntity(notifications):
    return [notificationResponseEntity(notification) for notification in notifications]
