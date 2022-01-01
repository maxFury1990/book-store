import time

import pytest
import requests
from assertpy import assert_that

from books_app.conftest import add_books
from books_app.models.book_type import Type
from books_app.service.books_service import BookService


class TestClass(BookService):

    host = "http://127.0.0.1:5000/v1/books/"

    book_list = {
        "book_1": {
            "title": "Let it snow",
            "type": Type.Satire.value,
            "creation_date": time.strftime("%Y-%m-%d")
        },
        "book_2": {
            "title": "Kaffry",
            "type": Type.Drama.value,
            "creation_date": time.strftime("%Y-%m-%d"),
        },
        "book_3": {
            "title": "Dalan",
            "type": Type.Science_Fiction.value,
            "creation_date": time.strftime("%Y-%m-%d"),
        }
    }

    @pytest.mark.parametrize("book_list", book_list.values(), ids=list(book_list.keys()))
    def test_add_multiple_books(self, book_list, up_and_down):
        books = requests.post(f"{self.host}manipulation", json=book_list)
        assert_that(books.status_code).is_equal_to(200)

    def test_add_one_book(self, up_and_down, book_type=Type.Satire.value,
                          title="Sartire",
                          creation_date=time.strftime("%Y-%m-%d")):
        new_book_json = add_books(book_type, title, creation_date)
        book_id = new_book_json.get("id")
        assert_that(book_id).is_not_empty()

    def test_get_book_info(self, up_and_down):
        get_info = requests.get(f"{self.host}info?id={up_and_down}")
        assert_that(get_info.status_code).is_equal_to(200)
        assert "title" in get_info.text is not None
        assert "id" in get_info.text is not None
        assert "type" in get_info.text is not None

    def test_update_book_info(self, up_and_down):
        book_json_before_updating = requests.get(f"{self.host}info?id={up_and_down}").json()
        title_before_updating = book_json_before_updating.get("title")
        payload = {'id': up_and_down, 'title': 'String Stig Sting', 'type': 'Drama'}
        requests.put(f"{self.host}manipulation?id={up_and_down}", json=payload)
        book_json_after_updating = requests.get(f"{self.host}info?id={up_and_down}").json()
        title_after_updating = book_json_after_updating.get("title")
        assert_that(title_after_updating).is_not_equal_to(title_before_updating)

    def test_get_non_existent_book(self, up_and_down, book_id="6e1815b3-ef31-4183-b40e-3c9666666"):
        get_info = requests.get(f"{self.host}info?id={book_id}")
        assert_that(get_info.status_code).is_equal_to(404)

    def test_check_updating_time(self, up_and_down):
        book_json_before_updating = requests.get(f"{self.host}info?id={up_and_down}").json()
        time_before_updating = book_json_before_updating.get("updated_date_time")
        payload = {'id': up_and_down, 'type': 'Satire'}
        requests.put(f"{self.host}manipulation?id={up_and_down}", json=payload)
        book_json_after_updating = requests.get(f"{self.host}info?id={up_and_down}").json()
        time_after_updating = book_json_after_updating.get("updated_date_time")
        assert_that(time_before_updating).is_not_equal_to(time_after_updating)

    def test_check_limit_filter(self, up_and_down, count=2):
        self.test_add_one_book(up_and_down)
        limit = requests.get(f"{self.host}latest?limit={count}")
        assert_that(limit.status_code).is_equal_to(200)
        assert_that(limit.text.count('id')).is_equal_to(count)

    def test_find_all_drama_books(self, up_and_down, limit=20):
        limit = requests.get(f"{self.host}latest?limit={limit}")
        assert_that(limit.status_code).is_equal_to(200)
        book_type = "Drama"
        limit.text.count(book_type)
        assert_that(limit.text.count(book_type)).is_greater_than(0)

    def test_delete_book(self, up_and_down):
        book_json = requests.get(f"{self.host}latest?limit=1").json()[0]
        book_id = book_json.get("id")
        req = requests.delete(f"{self.host}manipulation?id={book_id}")
        assert_that(req.status_code).is_equal_to(200)
        code_message = requests.get(f"{self.host}info?id={book_id}").reason
        assert_that(code_message).is_equal_to("NOT FOUND")









