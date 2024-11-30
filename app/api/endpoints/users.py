from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_auth_service
from app.dependencies.user import get_profile_service, get_user_service
from app.schemas.user_schemas import (
    AllUserDataDTO,
    RegisterUserDTO,
    UpdateUserPasswordRequestDTO,
    UpdateUserProfileRequestDTO,
    UserDataDTO,
)
from app.service.auth_service import AuthService
from app.service.profile_service import ProfileService
from app.service.user_service import UserService
from app.usecases.user_usecase import UserUsecase


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
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> None:
    # Дописать, что возвращает эта функция
    await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).delete_user(user_id)


@router.post("/register", name="Регистрация")  # Добавить проеврку отсутствия токена
async def create_user_and_profile(
    user: RegisterUserDTO,
    user_data: UserDataDTO,
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> AllUserDataDTO:
    user = await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).create_user_and_profile(user, user_data)
    return user


@router.patch("/update_profile", name="Изменить данные пользователя")
async def update_user_profile(
    body: UpdateUserProfileRequestDTO,
    user_id: UUID = Depends(AuthService.verify_token),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> None:
    user = await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).update_user_profile(user_id, body)
    return user


@router.patch("/update_password", name="Изменить пароль")
async def update_user_password(
    password: UpdateUserPasswordRequestDTO,
    user_id: UUID = Depends(AuthService.verify_token),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> None:
    user = await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).update_user_password(user_id, password)
    return user


@router.get("/all", name="Найти всех пользователей")
async def get_all_users(
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> Optional[list[AllUserDataDTO]]:
    users = await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).get_all_users()
    return users


@router.get("/{factory_employee_id}", name="Найти пользователя по таб.№")
async def get_user_info_by_factory_employee_id(
    factory_employee_id: int,
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> Optional[AllUserDataDTO]:
    user = await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).get_user_info_by_factory_employee_id(factory_employee_id)
    if not user:
        raise HTTPException(status_code=404, detail="Страница не найдена")
    return user


@router.get("/", name="Найти текущего пользователя")
async def get_current_user(
    user_id: UUID = Depends(AuthService.verify_token),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    profile_service: ProfileService = Depends(get_profile_service),
) -> Optional[AllUserDataDTO]:
    return await UserUsecase(
        auth_service,
        user_service,
        profile_service,
    ).get_user_by_id(user_id)
