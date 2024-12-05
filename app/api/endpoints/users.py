from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from app.dto.user import (
    AllUserDataDTO,
    RegisterUserDTO,
    UpdateUserPasswordRequestDTO,
    UpdateUserProfileRequestDTO,
    UserDataDTO,
)
from app.service.auth import AuthService
from app.usecases.user import UserUsecase


router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.delete(
    "/delete", name="Удалить пользователя"
)  # ДЛЯ ОТЛАДКИ - доступно без токена
##### Если осталять, то сделать проверку пользователя отсутвие полученных кабелей #####
async def delete_user(
    user_id: UUID,
) -> None:
    # Дописать, что возвращает эта функция
    await UserUsecase.delete_user(user_id)


@router.post("/register", name="Регистрация")  # Добавить проеврку отсутствия токена
async def create_user_and_profile(
    user: RegisterUserDTO,
    user_data: UserDataDTO,
) -> AllUserDataDTO:
    user = await UserUsecase.create_user_and_profile(user, user_data)
    return user


@router.patch("/update_profile", name="Изменить данные пользователя")
async def update_user_profile(
    body: UpdateUserProfileRequestDTO,
    user_id: UUID = Depends(AuthService.verify_token),
) -> None:
    user = await UserUsecase.update_user_profile(user_id, body)
    return user


@router.patch("/update_password", name="Изменить пароль")
async def update_user_password(
    password: UpdateUserPasswordRequestDTO,
    user_id: UUID = Depends(AuthService.verify_token),
) -> None:
    user = await UserUsecase.update_user_password(user_id, password)
    return user


@router.get("/all", name="Найти всех пользователей")
@cache(expire=60)
async def get_all_users() -> list[AllUserDataDTO]:
    users = await UserUsecase.get_all_users()
    return users


@router.get("/{factory_employee_id}", name="Найти пользователя по таб.№")
async def get_user_info_by_factory_employee_id(
    factory_employee_id: int,
) -> AllUserDataDTO:
    user = await UserUsecase.get_user_info_by_factory_employee_id(factory_employee_id)
    if not user:
        raise HTTPException(status_code=404, detail="Страница не найдена")
    return user


@router.get("/", name="Найти текущего пользователя")
async def get_current_user(
    user_id: UUID = Depends(AuthService.verify_token),
) -> AllUserDataDTO:
    return await UserUsecase.get_user_by_id(user_id)
