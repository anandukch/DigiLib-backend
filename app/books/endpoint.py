from fastapi import APIRouter
import app.books.crud as crud
from app.books.schemas import Author, Book

book_router = APIRouter()


@book_router.get("/")
async def get_all_books():
    try:
        await crud.get_books()
    except Exception as e:
        print(e)
        return {"error": "Error getting books"}

@book_router.get("/{book_id}")
async def get_book(book_id: int):
    try:
        await crud.get(book_id)
    except Exception as e:
        print(e)
        return {"error": "Error getting book"}

@book_router.post("/")
async def add_book(book: Book):
    try:
        await crud.add_book(book)
    except Exception as e:
        print(e)
        return {"error": "Error adding book"}

# add author
@book_router.post("/author")
async def add_author(author: Author):
    try:
        await crud.add_author(author)
    except Exception as e:
        print(e)
        return {"error": "Error adding author"}