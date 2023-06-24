from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import app.books.crud as crud
from app.books.schemas import Author, Book
from app.common import UserRoles
from app.oauth import get_current_user
from app.serializers.book_trans import bookTransListEntity
from app.serializers.books import bookListResponseEntity
from app.utils import role_decorator

book_router = APIRouter()

book_crud = crud.BookCrud()


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


@book_router.get("/transactions")
def get_all():
    try:
        return bookTransListEntity(crud.get_all_book_transactions())
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error"
        )
@book_router.get("/search")
def serach_book(title: str = None):
    try:
        return bookListResponseEntity(book_crud.search(title))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error searching book"
        )

@book_router.post("/{book_trans_id}/return")
@role_decorator(role=[UserRoles.ADMIN])
def return_book(book_trans_id: str, user=Depends(get_current_user)):
    try:
        print("return book")
        return crud.return_book(book_trans_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error returning book"
        )


@book_router.get("/")
def get_all_books():
    try:
        return crud.get_books()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error getting books"
        )


@book_router.get("/{book_id}")
def get_book(book_id: str):
    try:
        return crud.get_book(book_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error getting book"
        )


@book_router.post("/")
@role_decorator(role=[UserRoles.ADMIN])
def add_book(book: Book, user=Depends(get_current_user)):
    try:
        return crud.add_book(book.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error adding book"
        )


@book_router.post("/{book_id}/reserve")
@role_decorator(role=[UserRoles.STUDENT])
def reserve_book(book_id: str, user: str = Depends(get_current_user)):
    return crud.reserve_book(book_id, user)


@book_router.post("/{book_trans_id}/issue")
def issue_book(book_trans_id: str, user=Depends(get_current_user)):
    try:
        return crud.issue_book(book_trans_id, type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error issuing book"
        )


@book_router.get("/transactions/{book_id}")
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



