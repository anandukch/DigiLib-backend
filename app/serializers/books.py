def bookResposneEntity(book):
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "language": book["language"],
        "subject": book["subject"],
        "publisher": book["publisher"],
        "author": book["author"],
        "no_of_copies": book["no_of_copies"],
        "available_copies": book["available_copies"],
        'virtual_copies': book['virtual_copies'],
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
