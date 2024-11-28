from fastapi import HTTPException, status


class UserException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(UserException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"
