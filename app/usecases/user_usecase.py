from typing import Optional
from uuid import UUID

from app.exceptions.user import UserAlreadyExistsException
from app.models.user import User
from app.schemas.user_schemas import (
    AllUserDataDTO,
    CreateUserDTO,
    RegisterUserDTO,
    UpdateUserPasswordRequestDTO,
    UpdateUserProfileRequestDTO,
    UserDataDTO,
)
from app.service.auth_service import AuthService, UserService
from app.service.profile_service import ProfileService


class UserUsecase:
    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        profile_service: ProfileService,
    ):
        self.auth_service = auth_service
        self.user_service = user_service
        self.profile_service = profile_service

    async def create_user_and_profile(
        self,
        user: RegisterUserDTO,
        user_data: UserDataDTO,
    ) -> Optional[AllUserDataDTO]:
        if await self.user_service.get_user_info_by_factory_employee_id(
            user.factory_employee_id
        ):
            raise UserAlreadyExistsException
        hashed_password = self.auth_service.hashed_password(user.password)
        new_user = CreateUserDTO(
            hashed_password=hashed_password,
            **user.model_dump(),
        )
        user = await self.user_service.create_user(new_user)
        await self.profile_service.create_profile(user.id, user_data)
        user = await self.user_service.get_user_info_by_id(
            user.id
        )  # Для отладки. Потом убрать
        return user

    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        return await self.user_service.delete_user(user_id)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.user_service.get_user_info_by_id(user_id)

    async def get_user_info_by_factory_employee_id(
        self,
        factory_employee_id: int,
    ) -> Optional[AllUserDataDTO]:
        return await self.user_service.get_user_info_by_factory_employee_id(
            factory_employee_id
        )

    async def get_all_users(self) -> Optional[list[AllUserDataDTO]]:
        return await self.user_service.get_all_users()

    async def update_user_profile(
        self,
        user_id: UUID,
        new_data: UpdateUserProfileRequestDTO,
    ) -> Optional[User]:  # Для отладки. Потом None, наверно
        await self.profile_service.update_profile(user_id, new_data)
        return await self.user_service.get_user_info_by_id(user_id)

    async def update_user_password(
        self,
        user_id: UUID,
        password: UpdateUserPasswordRequestDTO,
    ) -> None:
        hashed_password = self.auth_service.hashed_password(password.password)
        await self.user_service.update_user_password(user_id, hashed_password)
