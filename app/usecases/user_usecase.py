from uuid import UUID

from app.exceptions.user import UserAlreadyExistsException
from app.models.user import User
from app.schemas.user_schemas import (
    CreateUserDTO,
    RegisterUserDTO,
    UpdateUserPasswordRequestDTO,
    UpdateUserProfileRequestDTO,
    UserDataDTO,
)
from app.service.auth_service import AuthService
from app.service.profile_service import ProfileService
from app.service.user_service import UserService


class UserUsecase:

    @classmethod
    async def create_user_and_profile(
        self,
        user: RegisterUserDTO,
        user_data: UserDataDTO,
    ) -> User | None:
        if await UserService.get_user_info_by_factory_employee_id(
            user.factory_employee_id
        ):
            raise UserAlreadyExistsException
        hashed_password = AuthService.hashed_password(user.password)
        new_user = CreateUserDTO(
            hashed_password=hashed_password,
            **user.model_dump(),
        )
        user = await UserService.create_user(new_user)
        if not user:
            return None
        await ProfileService.create_profile(user.id, user_data)
        user = await UserService.get_user_info_by_id(
            user.id
        )  # Для отладки. Потом убрать
        return user

    @classmethod
    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        return await UserService.delete_user(user_id)

    @classmethod
    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await UserService.get_user_info_by_id(user_id)

    @classmethod
    async def get_user_info_by_factory_employee_id(
        self,
        factory_employee_id: int,
    ) -> list[User] | None:
        return await UserService.get_user_info_by_factory_employee_id(
            factory_employee_id
        )

    @classmethod
    async def get_all_users(self) -> list[User] | None:
        return await UserService.get_all_users()

    @classmethod
    async def update_user_profile(
        self,
        user_id: UUID,
        new_data: UpdateUserProfileRequestDTO,
    ) -> User | None:  # Для отладки. Потом None, наверно
        await ProfileService.update_profile(user_id, new_data)
        return await UserService.get_user_info_by_id(user_id)

    @classmethod
    async def update_user_password(
        self,
        user_id: UUID,
        password: UpdateUserPasswordRequestDTO,
    ) -> None:
        hashed_password = AuthService.hashed_password(password.password)
        await UserService.update_user_password(user_id, hashed_password)
