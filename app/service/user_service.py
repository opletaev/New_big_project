from typing import Optional
from uuid import UUID

from pydantic import create_model

from app.models.user import User
from app.schemas.user_schemas import SAllUserData, SUserAuthData
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repository = user_repository

    async def create_user(
        self,
        factory_employee_id: int,
        hashed_password: str,
    ) -> UUID:
        user = SUserAuthData(
            factory_employee_id=factory_employee_id,
            hashed_password=hashed_password,
        )
        user_id = await self.repository.add(user)
        return user_id

    async def get_all_users(self) -> Optional[list[SAllUserData]]:
        users = await self.repository.find_all()
        return users

    async def get_user_info_by_id(
        self,
        user_id: UUID,
    ) -> Optional[User]:
        user = await self.repository.find_one_or_none_by_id(user_id)
        return user

    async def get_user_info_by_factory_employee_id(
        self,
        factory_employee_id: int,
    ) -> Optional[User]:
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
        await self.repository.delete_by_id(user_id)

    async def update_user_password(
        self,
        user_id: UUID,
        hashed_password: str,
    ) -> None:
        FilterModel = create_model(
            "FilterModel",
            hashed_password=(str, ...),
        )
        await self.repository.update_instance(
            user_id,
            FilterModel(hashed_password=hashed_password),
        )
