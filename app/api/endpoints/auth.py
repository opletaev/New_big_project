from fastapi import APIRouter, Depends, Request, Response

from app.dependencies.auth import get_auth_usecase
from app.schemas.auth_schemas import SAuthUser
from app.services.auth_service import AuthService
from app.usecases.auth_usecase import AuthUsecase


router = APIRouter(
    prefix="/user",
    tags=["Аутентификация"]
    )

@router.post("/login")
async def login_user(
    response: Response, 
    user_data: SAuthUser,
    usecase: AuthUsecase = Depends(get_auth_usecase)):
    user = await AuthService(usecase).login_user(response, user_data)
    return user

@router.post("/logout")
async def logout_user(
    response: Response, usecase: AuthUsecase = Depends(get_auth_usecase)):
    await AuthService(usecase).logout_user(response)
    
@router.post("/get_user_id")
def get_user_id(user_id: str = Depends(AuthUsecase.get_user_id)):
    return user_id