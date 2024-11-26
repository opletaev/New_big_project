from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Response


from app.dependencies.user import get_user_usecase
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.user_schemas import (
    SCreateUser,
    SShowUser,
    SUpdateUserRequest,
    )
from app.usecases.auth_usecase import AuthUsecase
from app.usecases.user_usecase import UserUsecase



router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
    )
    

@router.post("/register")  # Добавить проеврку отсутствия токена
async def create_user(
    body: SCreateUser, 
    usecase: UserUsecase = Depends(get_user_usecase)
    ) -> SShowUser:
    user = await UserService(usecase).create_user(body)
    return user


@router.delete("/delete")  # ДЛЯ ОТЛАДКИ - доступно без токена
##### Если осталять, то сделать проверку пользователя отсутвие полученных кабелей ##### 
async def delete_user(
    user_id: UUID, 
    usecase: UserUsecase = Depends(get_user_usecase)
    ):
    # Дописать, что возвращает эта функция
    user = await UserService(usecase).delete_user(user_id)
    return user


@router.get("/")  # Доступно без токена
async def get_user_info_by_factory_employee_id(
    factory_employee_id: int, 
    usecase: UserUsecase = Depends(get_user_usecase)
    ) -> SShowUser | None:
    # Дописать, что возвращает эта функция
    user = await UserService(usecase).get_user_info_by_factory_employee_id(factory_employee_id)
    return user


@router.get("/all")
async def get_all_users(
    usecase: UserUsecase = Depends(get_user_usecase)
    ) -> list[SShowUser]:
    users = await UserService(usecase).get_all_users()
    return users


# @router.get("/")  # Доступно по токену
# async def get_user_me():
#     pass

@router.patch("/update")  # Токен работает, обновление - нет.
async def update_user(
    body: SUpdateUserRequest,
    user_id: UUID = Depends(AuthUsecase.get_user_id),
    usecase: UserUsecase = Depends(get_user_usecase)
    ):
    user = await UserService(usecase).update_user(body, user_id)
    return user
