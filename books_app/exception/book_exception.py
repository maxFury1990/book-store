class BookValidationException(Exception):

    def __init__(self, status_code=400, message="The book entity is not valid."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        msg = {'message': self.message}
        return msg


class HttpException(Exception):

    def __init__(self, status_code=400, message="The request is not valid."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        msg = {'message': self.message}
        return msg


class BookAbsenceException(Exception):

    def __init__(self, status_code=404, message="There is no such book | books."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        msg = {'message': self.message}
        return msg
