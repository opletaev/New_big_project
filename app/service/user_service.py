from uuid import UUID

from pydantic import create_model

from app.models.user import User
from app.schemas.user_schemas import (
    SCreateUser,
    SUpdateUserRequest,
    SUser,
    SUserProfile,
)
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user_with_profile(
        self,
        body: SCreateUser,
        hashed_password: str,
    ) -> UUID:
        user = SUser(
            factory_employee_id=body.factory_employee_id,
            hashed_password=hashed_password,
        )
        user_info = body
        user_id = await self.repository.create_user_with_profile(
            user,
            user_info,
        )
        return user_id

    async def get_all_users(self) -> list[User] | None:
        users = await self.repository.find_all()
        return users

    async def get_user_info_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        user = await self.repository.find_one_or_none_by_id(user_id)
        return user

    async def get_user_info_by_factory_employee_id(
        self,
        factory_employee_id: int,
    ) -> User | None:
        FilterModel = create_model(
            "FilterModel",
            factory_employee_id=(int, ...),
        )
        user_info = await self.repository.find_one_or_none_by_filter(
            FilterModel(factory_employee_id=factory_employee_id),
        )
        return user_info

    async def delete_user(
        self,
        user_id: UUID,
    ) -> None:
        await self.repository.delete_by_id(instance_id=user_id)

    async def update_user(
        self,
        body: SUpdateUserRequest,
        user_id: UUID,
    ):
        print(body, "\n", user_id)
        # Добавить считывание user_id
        body = {key: value for key, value in body if value}
        print(body)
        user = await self.repository.update_user(user_id, **body)
        return user
