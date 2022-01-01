import logging

from flask import Flask
from flask_restful import Api

from books_app.exception.book_exception import BookValidationException, HttpException, BookAbsenceException
from books_app.exception.error_handler import handle_book_exception
from books_app.resources.book_resources import BookIds, BookManipulation, BookInfo, BookLatest


def add_resources(app):
    api = Api(app)
    api.add_resource(BookManipulation, '/v1/books/manipulation')
    api.add_resource(BookIds, '/v1/books/ids')
    api.add_resource(BookInfo, '/v1/books/info')
    api.add_resource(BookLatest, '/v1/books/latest')
    return app


def register_handlers(app):
    app.register_error_handler(BookValidationException, handle_book_exception)
    app.register_error_handler(HttpException, handle_book_exception)
    app.register_error_handler(BookAbsenceException, handle_book_exception)


def create_flask_app():
    app = Flask(__name__)
    add_resources(app)
    register_handlers(app)
    app.logger.setLevel(logging.INFO)
    return app
