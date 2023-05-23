from typing import List

from bson import ObjectId
from app.books.schemas import Author, AuthorDB, Book
from app.db import Authors, Books
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


def get_book(book_id: str):
    """
    Get a book by id
    """
    return bookResposneEntity(Books.find_one({"_id": ObjectId(book_id)}))


def add_book(book: dict):
    """
    Add a book
    """
    new_book = Books.insert_one(book)
    return bookResposneEntity(Books.find_one({"_id": new_book.inserted_id}))


def add_author(author: Author) -> Author:
    """
    Add an author
    """
    new_author = Authors.insert_one(author.dict())
    return authorResposneEntity(Authors.find_one({"_id": new_author.inserted_id}))


def get_author(author_id: str):
    """
    Get an author by id
    """
    print(author_id)
    return authorResposneEntity(Authors.find_one({"_id": ObjectId(author_id)}))


def get_authors() -> List[AuthorDB]:
    return authorListResponseEntity(list(Authors.find({})))
