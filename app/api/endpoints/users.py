from uuid import UUID
from fastapi import APIRouter, Depends

from app.dependencies.user import get_user_service
from app.schemas.user_schemas import (
    SCreateUser,
    SShowUser,
    SUpdateUserRequest,
    )
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.usecases.user_usecase import UserUsecase



router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
    )
    

@router.post("/register")  # Добавить проеврку отсутствия токена
async def create_user(
    body: SCreateUser, 
    service: UserService= Depends(get_user_service)
    ) -> SShowUser:
    user = await UserUsecase(service).create_user(body)
    return user


@router.delete("/delete")  # ДЛЯ ОТЛАДКИ - доступно без токена
##### Если осталять, то сделать проверку пользователя отсутвие полученных кабелей ##### 
async def delete_user(
    user_id: UUID, 
    service: UserService = Depends(get_user_service)
    ):
    # Дописать, что возвращает эта функция
    user = await UserUsecase(service).delete_user(user_id)
    return user


@router.get("/")  # Доступно без токена
async def get_user_info_by_factory_employee_id(
    factory_employee_id: int, 
    service: UserService = Depends(get_user_service)
    ) -> SShowUser | None:
    # Дописать, что возвращает эта функция
    user = await UserUsecase(service).get_user_info_by_factory_employee_id(factory_employee_id)
    return user


@router.get("/all")
async def get_all_users(
    service: UserService = Depends(get_user_service)
    ) -> list[SShowUser] | None:
    users = await UserUsecase(service).get_all_users()
    return users


# @router.get("/")  # Доступно по токену
# async def get_user_me():
#     pass


@router.patch("/update")  # Токен работает, обновление - нет.
async def update_user(
    body: SUpdateUserRequest,
    user_id: UUID = Depends(AuthService.verify_token),
    service: UserService = Depends(get_user_service)
    ):
    user = await UserUsecase(service).update_user(body, user_id)
    return user
