from fastapi import Response

from app.exceptions.auth import IncorrectEmailOrPassword
from app.repositories.user import UserRepository
from app.schemas.auth_schemas import AuthDTO
from app.service.auth_service import AuthService
from app.service.user_service import UserService


class AuthUsecase:

    @classmethod
    async def login_user(cls, response: Response, body: AuthDTO) -> str:
        user = await UserService.get_user_info_by_factory_employee_id(
            body.factory_employee_id
        )
        if not user or not AuthService.verify_password(
            body.password, user.hashed_password
        ):
            raise IncorrectEmailOrPassword

        access_token = AuthService.create_access_token({"sub": str(user.id)})
        response.set_cookie("access_token", access_token, httponly=True)
        return access_token

    @classmethod
    async def logout_user(cls, response: Response) -> None:
        response.delete_cookie("access_token")
