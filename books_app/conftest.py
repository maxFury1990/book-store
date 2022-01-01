import random, string
import time

import pytest
import requests
from assertpy import assert_that

from books_app.models.book import Book
from books_app.models.book_type import Type


letters = string.ascii_lowercase
result_str = ''.join(random.choice(letters) for i in range(5))


def add_books(book_type, title, creation_date):
    book = Book(book_type, title, creation_date)
    return requests.post("http://127.0.0.1:5000/v1/books/manipulation", json=book.serialize()).json()


@pytest.fixture()
def up_and_down(book_type=Type.Drama.value, title=result_str, creation_date=time.strftime("%Y-%m-%d")):
    new_book_json = add_books(book_type, title, creation_date)
    book_id = new_book_json.get("id")
    assert_that(book_id).is_not_empty()
    yield book_id
    get_all_books = requests.get("http://127.0.0.1:5000/v1/books/latest?limit=5000").json()
    if "message" in get_all_books:
        return "There is no books"
    for book_id in get_all_books:
        id = book_id.get("id")
        requests.delete(f"http://127.0.0.1:5000/v1/books/manipulation?id={id}")
