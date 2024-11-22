from fastapi import APIRouter, Response

from app.schemas.auth_schemas import SAuthUser
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/user",
    tags=["Аутентификация"]
    )

@router.post("/login")
async def login_user(response: Response, user_data: SAuthUser):
    user = await AuthService().login_user(response, user_data)
    return user

@router.post("/logout")
async def logout_user(response: Response):
    AuthService().logout_user(response)