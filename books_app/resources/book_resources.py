import logging

from flask_restful import Resource, request

from books_app.exception.book_exception import HttpException, BookAbsenceException
from books_app.service.books_service import bs


class BookManipulation(Resource):

    def post(self):
        request_data = request.get_json()
        logging.info(request_data)
        if request_data and ("type" in request_data) and ("title" in request_data):
            book = bs.add_book(request_data["type"],
                               request_data["title"],
                               request_data["creation_date"] if "creation_date" in request_data else None)
            log_data = {'method_type': request.method, 'req_url': request.path, 'entity': request_data, 'id': book.id}
            logging.info(f'Book added {log_data}')
            return book.serialize(), 200
        else:
            raise HttpException()

    def delete(self):
        book_id = request.args.get('id')
        if book_id is None:
            raise HttpException
        book = bs.remove_book(book_id)
        if book:
            log_data = {'method_type': request.method, 'req_url': request.path, 'entity': book_id}
            logging.info(f'Book removed {log_data}')
            return book.serialize(), 200
        else:
            raise BookAbsenceException()

    def put(self):
        book_id = request.args.get('id')
        if not book_id:
            BookAbsenceException()

        request_data = request.get_json()
        if request_data and (("title" in request_data) or ("type" in request_data)):
            book = bs.update_book_title_and_type(book_id, request_data.get("title"), request_data.get("type"))
            log_data = {'method_type': request.method, 'req_url': request.path, 'entity': book.serialize()}
            logging.info(f'Book was updated {log_data}')
            return book.serialize(), 200
        else:
            return {"message": "Neither title no boor type are specified"}, 200

    def get(self):

        return {"message": "No implementation for `GET` method"}, 200


class BookIds(Resource):

    def get(self):
        book_type = request.args.get('book_type')
        if book_type is None:
            raise HttpException
        return bs.get_all_books(book_type), 200


class BookLatest(Resource):

    def get(self):
        limit = request.args.get('limit')
        if limit is None:
            raise HttpException
        books = [book.serialize() for book in bs.get_latest(limit)]
        return books, 200


class BookInfo(Resource):

    def get(self):
        book_id = request.args.get('id')
        print(book_id)
        if book_id is None:
            raise HttpException
        book = bs.get_book_info(book_id)
        if book:
            book_json = book.serialize()
            log_data = {'method_type': request.method, 'req_url': request.path, 'entity': book_json}
            logging.info(f'Book info was shown {log_data}')
            return book_json, 200
        else:
            raise BookAbsenceException()


logging.basicConfig(filename='book_app.log', level=logging.INFO)
