class User:
    def __init__(
        self,
        id: int,
        name: str,
        surname: str,
        patronymic: str,
        phone_number: str,
    ):
        self.id = id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.phone_number = phone_number
