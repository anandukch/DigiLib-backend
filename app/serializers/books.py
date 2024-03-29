def bookResposneEntity(book):
    return {
        "id": str(book["_id"]),
        "ISBN": book["ISBN"],  # noqa: E501
        "title": book["title"],
        "description": book["description"],
        "subject": book["subject"],
        "publisher": book["publisher"],
        "author": book["author"],
        "no_of_copies": book["no_of_copies"],
        "available_copies": book["available_copies"],
        "virtual_copies": book["virtual_copies"],
        "image": book["image"],
        "semester": book["semester"],
    }


def authorResposneEntity(author):
    return {
        "id": str(author["_id"]),
        "name": author["name"],
        "description": author["description"],
    }


def authorListResponseEntity(authors):
    return [authorResposneEntity(author) for author in authors]


def bookListResponseEntity(books):
    return [bookResposneEntity(book) for book in books]


def bookItemEntity(bookItem):
    return {
        "id": str(bookItem["_id"]),
        "acc_no": bookItem["acc_no"],
        "book_id": str(bookItem["book_id"]),
        "status": bookItem["status"],
    }
    
def bookItemsEntity(book_items):
    return [bookItemEntity(book_items) for book_item in book_items]
