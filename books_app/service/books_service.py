"""Works with books collection 'list_books'
"""
from datetime import datetime

from books_app.exception.book_exception import BookAbsenceException, HttpException
from books_app.models.book import Book, validate_title, validate_type
from books_app.models.book_type import Type


class BookService:
    list_books = []

    def get_all_books(self, book_type):
        """
        Retrieve all books with book type
        :param book_type: book's type
        :return: list of books
        """
        validate_type(book_type)
        return [book.serialize() for book in self.list_books if book.book_type == Type(book_type)]

    def add_book(self, book_type, title, creation_date):
        """
        Adds book to book_list in case it is valid.
        :param book_type: type of the book
        :param title: book's title
        :param creation_date: date of creation
        :return: created book
        """
        book = Book(book_type, title, creation_date)
        self.list_books.append(book)
        return book

    def remove_book(self, book_id):
        book = self.find_book_by_id(book_id)
        if book:
            self.list_books.remove(book)
        return book

    def get_latest(self, limit):
        limit = check_limit(limit)
        books = sorted(self.list_books, key=lambda b: b.updated_date_time, reverse=True)
        if books:
            return books[:limit]
        else:
            raise BookAbsenceException()

    def get_book_info(self, book_id):
        book = self.find_book_by_id(book_id)
        return book

    def find_book_by_id(self, book_id):
        return next((i for i in self.list_books if i.id == book_id), None)

    def update_book_title_and_type(self, book_id, title, book_type):
        if title is not None:
            validate_title(title)
        if book_type:
            validate_type(book_type)
        book = self.find_book_by_id(book_id)
        if book:
            book.title = title if title is not None else book.title
            book.book_type = Type(book_type) if book_type else book.book_type
            book.updated_date_time = datetime.now().isoformat()
            return book
        else:
            raise BookAbsenceException()


def check_limit(limit):
    try:
        limit = int(limit)
        if limit < 0:
            raise ValueError
    except ValueError:
        raise HttpException()
    return limit


bs = BookService()
