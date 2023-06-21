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
BookQueue = db.book_queue
BookRequests = db.book_requests
BookTransactions = db.book_transactions
Projects = db.projects
Notifications=db.notifications

User.create_index([("email", pymongo.ASCENDING)], unique=True)

