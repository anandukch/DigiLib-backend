from pydantic import BaseModel


# class NotificationSchema(BaseModel):
#     id: str
#     title: str
#     description: str
#     created_at: str
#     updated_at: str
#     user_id: str
#     is_read: bool

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {"ObjectId": str}
        
# class NotificationCreateSchema(BaseModel):
#     title: str
#     description: str
#     user_id: str

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {"ObjectId": str}

class NotificationSchema(BaseModel):
    description: str
    reciever_id: str | None = None
    sender_id: str | None = None
    
    class Config:
        orm_mode = True
        
class NotificationDBSchema(NotificationSchema):
    id: str
    created_at: str
    updated_at: str
    is_read: bool
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {"ObjectId": str}
