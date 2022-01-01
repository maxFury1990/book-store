from books_app.exception.book_exception import BookValidationException
from books_app.models.book_type import Type
import uuid
from datetime import datetime


class Book:
    def __str__(self) -> str:
        return f"book_type: {self.book_type}, title: {self.title}, id: {self.id}, " \
               f"creation_date: {self.creation_date}, updated_date_time: {self.updated_date_time}"

    def __init__(self, book_type, title, creation_date):
        self.validate_book(book_type, title, creation_date)
        self.book_type = Type(book_type)
        self.title = title
        self.id = str(uuid.uuid4())
        self.creation_date = creation_date
        self.updated_date_time = datetime.now().isoformat()

    def serialize(self):
        return {"type": self.book_type.value,
                "title": self.title,
                "id": self.id,
                "creation_date": self.creation_date,
                "updated_date_time": self.updated_date_time}

    @staticmethod
    def validate_book(book_type, title, creation_date):
        validate_type(book_type)
        validate_title(title)
        validate_creation_date(creation_date)


def validate_title(title):
    if len(title) > 255:
        raise BookValidationException()


def validate_type(book_type):
    if book_type not in Type.values():
        raise BookValidationException()


def validate_creation_date(creation_date):
    if (creation_date is not None) and (not _is_valid_date(creation_date)):
        raise BookValidationException()


def _is_valid_date(creation_date):
    try:
        datetime.strptime(creation_date, '%Y-%m-%d')
    except ValueError:
        return False
    return True
