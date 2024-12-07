from typing import Annotated
from fastapi import APIRouter, Depends, Response

from app.api.dependencies import auth_service, user_service
from app.dto.auth import AuthDTO
from app.exceptions.auth import IncorrectEmailOrPassword
from app.services.auth import AuthService
from app.services.user import UserService


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", name="Аутентификация")
async def login_user(
    response: Response,
    user_data: AuthDTO,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    user_service: Annotated[UserService, Depends(user_service)],
) -> str:
    user = await user_service.get_user(user_data.factory_employee_id)
    if not user or not auth_service.verify_password(
        user_data.password, user.hashed_password
    ):
        raise IncorrectEmailOrPassword
    access_token = auth_service.create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return access_token


@router.post("/logout", name="Выход")
async def logout_user(
    response: Response,
) -> None:
    await AuthService.logout_user(response)


@router.post("/my_id", name="Получить ID текущего пользователя")
async def get_current_user_id(user_id: str = Depends(AuthService.verify_token)) -> str:
    return user_id
