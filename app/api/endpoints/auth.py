from fastapi import APIRouter, Depends, Response

from app.dependencies.auth import get_auth_service, get_user_service
from app.schemas.auth_schemas import SAuth
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.usecases.auth_usecase import AuthUsecase


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", name="Аутентификация")
async def login_user(
    response: Response,
    user_data: SAuth,
    service: AuthService = Depends(get_auth_service),
) -> str:
    user = await AuthUsecase(service).login_user(response, user_data)
    return user


@router.post("/logout", name="Выход")
async def logout_user(
    response: Response,
    service: UserService = Depends(get_user_service),
) -> None:
    await AuthUsecase(service).logout_user(response)


@router.post("/my_id", name="Получить ID текущего пользователя")
async def get_current_user_id(user_id: str = Depends(AuthService.verify_token)) -> str:
    return user_id
