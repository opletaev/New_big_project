from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_cache.decorator import cache

from app.api.dependencies import (
    auth_service,
    profile_service,
    user_service,
    verify_token,
)
from app.dto.user import (
    AllUserDataDTO,
    RegisterUserDTO,
    UpdateUserPasswordRequestDTO,
    UpdateUserProfileRequestDTO,
    UserDataDTO,
)
from app.exceptions.user import UserAlreadyExistsException
from app.services.auth import AuthService
from app.services.profile import ProfileService
from app.services.user import UserService


router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.delete("/delete", name="Удалить пользователя")
async def delete_user(  # TODO: Добавить проверку токена
    user_id: UUID,  # TODO: Cделать проверку отсутвие полученных кабелей у пользователя
    user_service: Annotated[UserService, Depends(user_service)],
) -> str:
    await user_service.delete_user(user_id)


@router.post(
    "/register", name="Регистрация"
)  # TODO: Добавить проеврку отсутствия токена
async def create_user_and_profile(
    user: RegisterUserDTO,
    user_data: UserDataDTO,
    user_service: Annotated[UserService, Depends(user_service)],
    auth_service: Annotated[AuthService, Depends(auth_service)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
) -> AllUserDataDTO:
    if await user_service.get_user(user.factory_employee_id):
        raise UserAlreadyExistsException
    hashed_password = auth_service.hashed_password(user.password)
    user = await user_service.create_user(user, hashed_password)
    await profile_service.create_profile(user.id, user_data)
    user = await user_service.get_user_by_id(
        user.id
    )  # TODO: Нужно для отладки. Потом убрать
    return user


@router.patch("/update/profile", name="Изменить данные пользователя")
async def update_user_profile(
    user_data: UpdateUserProfileRequestDTO,
    user_id: Annotated[UUID, Depends(verify_token)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
) -> str:
    return await profile_service.update_profile(user_id, user_data)


@router.patch("/update/password", name="Изменить пароль")
async def update_user_password(  # TODO: Добавить проверку токена
    password: UpdateUserPasswordRequestDTO,
    user_id: Annotated[UUID, Depends(verify_token)],
    user_service: Annotated[UserService, Depends(user_service)],
    auth_service: Annotated[AuthService, Depends(auth_service)],
) -> str:
    hashed_password = auth_service.hashed_password(password.password)
    return await user_service.update_user_password(user_id, hashed_password)


@router.get("/all", name="Найти всех пользователей")
@cache(expire=60)
async def get_all_users(
    user_service: Annotated[UserService, Depends(user_service)],
) -> list[AllUserDataDTO]:
    return await user_service.get_all_users()


@router.get("/me", name="Найти текущего пользователя")
async def get_current_user(
    user_id: Annotated[UUID, Depends(verify_token)],
    user_service: Annotated[UserService, Depends(user_service)],
) -> AllUserDataDTO:
    return await user_service.get_user_by_id(user_id)


@router.get("/", name="Найти пользователя по таб.№")
async def get_user_info_by_factory_employee_id(
    factory_employee_id: int,
    user_service: Annotated[UserService, Depends(user_service)],
) -> AllUserDataDTO:
    user_info = await user_service.get_user(factory_employee_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user_info
