import enum


class Type(enum.Enum):
    Science_Fiction = "Science"
    Satire = "Satire"
    Drama = "Drama"
    Action_and_Adventure = "Adventure"
    Romance = "Romance"

    @staticmethod
    def values():
        return [pair.value for pair in Type]

    def __str__(self):
        return f"book_type: {self.name}"
