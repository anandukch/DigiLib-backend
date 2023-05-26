def bookTransEntity(bookTrans):
    return {
        "id": str(bookTrans["_id"]),
        "book_id": str(bookTrans["book_id"]),
        "user_id": str(bookTrans["user_id"]),
        "status": bookTrans["status"],
        "date_of_return": bookTrans["date_of_return"],
        "date_of_issue": bookTrans["date_of_issue"],
        "actual_date_of_return": bookTrans["actual_date_of_return"],
        "fine": bookTrans["fine"],
        "issued_by": bookTrans["issued_by"],
        "date_of_reservation": bookTrans["date_of_reservation"],
    }


def bookTransListEntity(bookTrans):
    return [bookTransEntity(book) for book in bookTrans]
