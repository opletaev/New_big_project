from uuid import UUID

from pydantic import create_model

from app.models.user import User
from app.dto.user import CreateUserDTO, RegisterUserDTO
from app.repositories.base import AbstractRepository


class UserService:
    def __init__(self, user_repository: AbstractRepository):
        self.user_repository = user_repository()

    async def create_user(
        self,
        user: RegisterUserDTO,
        hashed_password: str,
    ) -> bool:
        user = CreateUserDTO(
            hashed_password=hashed_password,
            **user.model_dump(),
        )
        return await self.user_repository.add(user)

    async def get_all_users(self) -> list[User] | None:
        users = await self.user_repository.find_all()
        return users

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        FilterModel = create_model(
            "FilterModel",
            id=(UUID, ...),
        )
        user = await self.user_repository.find_one_or_none_by_filter(
            FilterModel(id=user_id),
        )
        return user

    async def get_user(
        self,
        factory_employee_id: int,
    ) -> User:
        FilterModel = create_model(
            "FilterModel",
            factory_employee_id=(int, ...),
        )
        user_info = await self.user_repository.find_one_or_none_by_filter(
            FilterModel(factory_employee_id=factory_employee_id),
        )
        return user_info

    async def delete_user(
        self,
        user_id: UUID,
    ) -> str:
        await self.user_repository.delete_by_id(user_id)
        return "Пользователь удален"  # TODO: Придумать, что вернуть вместо этого

    async def update_user_password(
        self,
        user_id: UUID,
        hashed_password: str,
    ) -> str:
        FilterModel = create_model(
            "FilterModel",
            hashed_password=(str, ...),
        )
        await self.user_repository.update_instance(
            user_id,
            FilterModel(hashed_password=hashed_password),
        )
        return "Пароль изменен"  # TODO: Придумать, что вернуть вместо этого
