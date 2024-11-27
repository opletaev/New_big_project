from fastapi import APIRouter, Depends, Response

from app.dependencies.auth import get_auth_service, get_user_service
from app.schemas.auth_schemas import SAuthUser
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.usecases.auth_usecase import AuthUsecase



router = APIRouter(
    prefix="/user",
    tags=["Аутентификация"]
    )

@router.post("/login")
async def login_user(
    response: Response, 
    user_data: SAuthUser,
    service: AuthService= Depends(get_auth_service)):
    user = await AuthUsecase(service).login_user(response, user_data)
    return user

@router.post("/logout")
async def logout_user(
    response: Response, service: UserService= Depends(get_user_service)):
    await AuthUsecase(service).logout_user(response)
    
@router.post("/get_user_id")
async def get_user_id(user_id: str = Depends(AuthService.verify_token)):
    return user_id