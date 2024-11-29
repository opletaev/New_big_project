from fastapi import Response

from app.exceptions.auth import IncorrectEmailOrPassword
from app.repositories.user import UserRepository
from app.schemas.auth_schemas import SAuth
from app.service.auth_service import AuthService
from app.service.user_service import UserService


class AuthUsecase:
    def __init__(self, auth_service: AuthService):
        self.service = auth_service

    async def login_user(self, response: Response, body: SAuth) -> str:
        user = await UserService(  # Тут дерьмо какое-то
            UserRepository  # НАСТРОИТЬ ЗАВИСИМОСТИ
        ).get_user_info_by_factory_employee_id(body.factory_employee_id)
        if not user or not self.service.verify_password(
            body.password, user.hashed_password
        ):
            raise IncorrectEmailOrPassword

        access_token = self.service.create_access_token({"sub": str(user.id)})
        response.set_cookie("access_token", access_token, httponly=True)
        return access_token

    async def logout_user(self, response: Response) -> None:
        response.delete_cookie("access_token")
