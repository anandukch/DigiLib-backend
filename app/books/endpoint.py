import json
from logging import Logger
from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
import app.books.crud as crud
from app.books.schemas import Author, Book
from app.common import UserRoles
from app.oauth import get_current_user
from app.utils import role_decorator

book_router = APIRouter()


@book_router.get("/authors")
def get_authors():
    try:
        return crud.get_authors()
    except Exception as e:
        print(e)
        return {"error": "Error getting authors"}


@book_router.post("/authors")
def add_author(author: Author):
    try:
        return crud.add_author(author)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error adding author"
        )


@book_router.get("/")
def get_all_books():
    try:
        return crud.get_books()
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
@role_decorator(role=[UserRoles.ADMIN])
def add_book(book: Book, user=Depends(get_current_user)):
    try:
        return crud.add_book(book.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error adding book"
        )


@book_router.post("/reserve/{book_id}")
@role_decorator(role=[UserRoles.STUDENT])
def reserve_book(book_id: str, user: str = Depends(get_current_user)):
    return crud.reserve_book(book_id, user)

@book_router.post("/issue/{book_item_id}")
def issue_book(book_item_id: str):
    try:
        return crud.issue_book(book_item_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error issuing book"
        )


@book_router.post("/return/{book_item_id}")
@role_decorator(role=[UserRoles.STUDENT])
def return_book(book_trans_id: str):
    try:
        return crud.return_book(book_trans_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error returning book"
        )


@book_router.get("/transaction/{book_id}/")
def get_book_transactions(
    book_id: str, type: str = None, user=Depends(get_current_user)
):
    try:
        return crud.get_book_transactions(book_id, type)
    except Exception as e:
        if type(e) == HTTPException:
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error getting book transactions",
        )
        

@book_router.post("/upload")
def upload_books(file: UploadFile = File(...)):
    try:
        return crud.upload_file(file)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error uploading books"
        )
        