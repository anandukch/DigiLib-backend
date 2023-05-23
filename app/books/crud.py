from typing import List
from app.books.schemas import Author, AuthorDB, Book
from app.db import Authors, Books
from app.serializers.books import (
    authorListResponseEntity,
    authorResposneEntity,
    bookListResponseEntity,
)


def get_books():
    """
    Get all books
    """
    return bookListResponseEntity(list(Books.find({})))


def get_book(book_id: int):
    """
    Get a book by id
    """
    book = Books.find_one(id=book_id)
    return book


def add_book(book: Book):
    """
    Add a book
    """
    new_book = Books.insert_one(book)
    return new_book


def add_author(author: Author) -> Author:
    """
    Add an author
    """
    new_author = Authors.insert_one(author.dict())
    return authorResposneEntity(Authors.find_one({"_id": new_author.inserted_id}))


def get_authors()->List[AuthorDB]:
    return authorListResponseEntity(list(Authors.find({})))
