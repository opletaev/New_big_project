from fastapi import APIRouter, Depends, Response

from app.schemas.auth_schemas import AuthDTO
from app.service.auth_service import AuthService
from app.usecases.auth_usecase import AuthUsecase


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", name="Аутентификация")
async def login_user(
    response: Response,
    user_data: AuthDTO,
) -> str:
    user = await AuthUsecase.login_user(response, user_data)
    return user


@router.post("/logout", name="Выход")
async def logout_user(
    response: Response,
) -> None:
    await AuthUsecase.logout_user(response)


@router.post("/my_id", name="Получить ID текущего пользователя")
async def get_current_user_id(user_id: str = Depends(AuthService.verify_token)) -> str:
    return user_id
