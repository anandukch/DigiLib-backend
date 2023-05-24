from typing import List

from bson import ObjectId
from app.books.schemas import Author, AuthorDB, Book
from app.common import BookStatus
from app.db import Authors, BookItems, Books, Utils
from app.exception_handler import exception_handler
from app.serializers.books import (
    authorListResponseEntity,
    authorResposneEntity,
    bookListResponseEntity,
    bookResposneEntity,
)


def get_books():
    """
    Get all books
    """
    return bookListResponseEntity(list(Books.find({})))


def get_book(book_id: str) -> Book:
    """
    Get a book by id
    """
    return bookResposneEntity(Books.find_one({"_id": ObjectId(book_id)}))


def add_book(book: dict) -> Book:
    """
    Add a book
    """
    new_book = Books.insert_one(book)
    acc_no = 1000
    if not Utils.find_one({"name": "acc_no"}):
        Utils.insert_one({"name": "acc_no", "value": acc_no})
    else:
        acc_no = Utils.find_one({"name": "acc_no"})["value"]
    for i in range(book["no_of_copies"]):
        BookItems.insert_one(
            {
                "book_id": new_book.inserted_id,
                "acc_no": acc_no + 1,
                "status": BookStatus.AVAILABLE,
            }
        )
        acc_no += 1
        Utils.update_one({"name": "acc_no"}, {"$set": {"value": acc_no}})

    return get_book(new_book.inserted_id)


def add_author(author: Author) -> Author:
    """
    Add an author
    """
    new_author = Authors.insert_one(author.dict())
    return get_author(new_author.inserted_id)


def get_author(author_id: str):
    """
    Get an author by id
    """
    return authorResposneEntity(Authors.find_one({"_id": ObjectId(author_id)}))


def get_authors() -> List[AuthorDB]:
    return authorListResponseEntity(list(Authors.find({})))


def reserve_book(book_id: str):
    """
    Reserve a book
    """
    book = Books.find_one({"_id": ObjectId(book_id)})
    if book["available"]:
        Books.update_one({"_id": ObjectId(book_id)}, {"$set": {"available": False}})
        return {"message": "Book reserved"}
    else:
        return {"message": "Book not available"}
