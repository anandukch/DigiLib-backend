from bson import ObjectId
from pydantic import BaseModel


class LibConfig(BaseModel):
    fine_rate: int
    days_of_return: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
