from uuid import UUID
from fastapi import APIRouter, Depends

from app.services.user_service import UserService
from app.schemas.user_schemas import (
    SCreateUser,
    SShowUser,
    SUpdateUserRequest,
    )
from app.usecases.auth_usecase import AuthUsecase


router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
    )
    

@router.post("/register")
async def create_user(body: SCreateUser) -> SShowUser:
    user = await UserService().register_user(body)
    return user


@router.delete("/delete")
async def delete_user(user_id: UUID):
    # Дописать, что возвращает эта функция
    user = await UserService().delete_user(user_id)
    return user


@router.get("/")
async def get_user(factory_employee_id: int):
    # Дописать, что возвращает эта функция
    user = await UserService().get_user_by_factory_employee_id(factory_employee_id)
    return user


@router.patch("/update")
async def update_user(
    body: SUpdateUserRequest, 
    user_id: UUID = Depends(AuthUsecase.get_user_id)
    ):
    user = await UserService().update_user(body, user_id)
    return user
