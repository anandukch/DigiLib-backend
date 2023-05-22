from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.user import Admin, Issuer, Student, Teacher, User
from app.settings import settings


async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        database=client.digilib, document_models=[User, Student, Teacher, Admin, Issuer]
    )
