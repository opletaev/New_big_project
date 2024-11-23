from uuid import UUID
from fastapi import APIRouter, Depends, Response

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
    

@router.post("/register")  # Добавить проеврку отсутствия токена
async def create_user(body: SCreateUser) -> SShowUser:
    user = await UserService().create_user(body)
    return user


@router.delete("/delete")  # ДЛЯ ОТЛАДКИ - доступно без токена
##### Если осталять, то сделать проверку пользователя отсутвие полученных кабелей ##### 
async def delete_user(user_id: UUID):
    # Дописать, что возвращает эта функция
    user = await UserService().delete_user(user_id)
    return user


@router.get("/")  # Доступно без токена
async def get_user_by_factory_employee_id(factory_employee_id: int):
    # Дописать, что возвращает эта функция
    user = await UserService().get_user_by_factory_employee_id(factory_employee_id)
    return user


# @router.get("/")  # Доступно по токену
# async def get_user_me():
#     pass

@router.patch("/update")  # Токен работает, обновление - нет.
async def update_user(
    body: SUpdateUserRequest,
    user_id: UUID = Depends(AuthUsecase.get_user_id)
    ):
    user = await UserService().update_user(body, user_id)
    return user
