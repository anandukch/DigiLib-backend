from fastapi import APIRouter, HTTPException, status
import app.books.crud as crud
from app.books.schemas import Author, Book

book_router = APIRouter()


@book_router.get("/authors")
def get_authors():
    try:
        return crud.get_authors()
    except Exception as e:
        print(e)
        return {"error": "Error getting authors"}


@book_router.get("/")
def get_all_books():
    try:
        crud.get_books()
    except Exception as e:
        print(e)
        return {"error": "Error getting books"}


@book_router.get("/{book_id}")
def get_book(book_id: str):
    try:
        return crud.get_book(book_id)
    except Exception as e:
        print(e)
        return {"error": "Error getting book"}


@book_router.post("/")
def add_book(book: Book):
    try:
        author = crud.get_author(book.author)
        return crud.add_book(book.dict())
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error adding book"
        )


@book_router.post("/authors")
def add_author(author: Author):
    try:
        return crud.add_author(author)
    except Exception as e:
        print(e)
        return {"error": "Error adding author"}
    
    

