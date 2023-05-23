
from app.books.schemas import Author, Book
from app.db import Authors, Books


def get_books():
    """
    Get all books
    """
    books =Books.all()
    return books

def get_book(book_id: int):
    """
    Get a book by id
    """
    book = Books.find_one(id=book_id)
    return book

def add_book(book:Book):
    """
    Add a book
    """
    new_book = Books.insert_one(book)
    return new_book


def add_author(author: Author):
    """
    Add an author
    """
    new_author = Authors.insert_one(author)
    return new_author

