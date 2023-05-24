# from beanie import init_beanie, Document
# from motor.motor_asyncio import AsyncIOMotorClient

# from app.models.user import Admin, Issuer, Student, Teacher, User
# from app.settings import settings


# async def init_db():
#     client = AsyncIOMotorClient(settings.MONGO_URL)
#     await init_beanie(
#         database=client.digilib, document_models=[User, Student, Teacher, Admin, Issuer]
#     )


from pymongo import mongo_client
import pymongo
from app.books.schemas import Author

from app.settings import settings


client = mongo_client.MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client["digilib"]
User = db.users
Books = db.books
Authors = db.authors
BookItems = db.book_items
Utils = db.utils
# BookRequests = db.book_requests
# BookTransactions = db.book_transactions

User.create_index([("email", pymongo.ASCENDING)], unique=True)
