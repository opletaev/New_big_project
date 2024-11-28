from typing import Optional
from uuid import UUID

from app.exceptions.user import UserAlreadyExistsException
from app.models.user import User
from app.schemas.user_schemas import (
    SCreateUser,
    SShowUser,
    SUpdateUserPasswordRequest,
    SUpdateUserProfileRequest,
)
from app.service.auth_service import AuthService, UserService


class UserUsecase:
    def __init__(self, service: UserService):
        self.service = service

    async def create_user(
        self,
        body: SCreateUser,
    ) -> Optional[SShowUser]:
        if await self.service.get_user_info_by_factory_employee_id(
            body.factory_employee_id
        ):
            raise UserAlreadyExistsException
        hashed_password = AuthService(self.service).hashed_password(
            body.password
        )  # Тут дерьмо какое-то. НАСТРОИТЬ ЗАВИСИМОСТИ
        user_id = await self.service.create_user_with_profile(body, hashed_password)
        user = await self.service.get_user_info_by_id(
            user_id
        )  # Для отладки. Потом убрать
        return user

    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        return await self.service.delete_user(user_id)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.service.get_user_info_by_id(user_id)

    async def get_user_info_by_factory_employee_id(
        self,
        factory_employee_id: int,
    ) -> Optional[SShowUser]:
        return await self.service.get_user_info_by_factory_employee_id(
            factory_employee_id
        )

    async def get_all_users(self) -> Optional[list[SShowUser]]:
        return await self.service.get_all_users()

    async def update_user_profile(
        self,
        user_id: UUID,
        body: SUpdateUserProfileRequest,
    ) -> Optional[User]:  # Для отладки. Потом None, наверно
        await self.service.update_user_profile(user_id, body)
        return await self.service.get_user_info_by_id(user_id)

    async def update_user_password(
        self,
        user_id: UUID,
        password: SUpdateUserPasswordRequest,
    ) -> None:
        hashed_password = AuthService(self.service).hashed_password(password.password)
        await self.service.update_user_password(user_id, hashed_password)
