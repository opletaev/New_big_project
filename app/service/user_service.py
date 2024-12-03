from uuid import UUID

from pydantic import create_model

from app.models.user import User
from app.schemas.user_schemas import CreateUserDTO
from app.repositories.user import UserRepository


class UserService:
    __user_repository = UserRepository()

    @classmethod
    async def create_user(self, user: CreateUserDTO) -> bool:
        return await self.__user_repository.add(user)

    @classmethod
    async def get_all_users(self) -> list[User] | None:
        users = await self.__user_repository.find_all()
        return users

    @classmethod
    async def get_user_info_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        user = await self.__user_repository.find_one_or_none_by_id(user_id)
        return user

    @classmethod
    async def get_user_info_by_factory_employee_id(
        self,
        factory_employee_id: int,
    ) -> User | None:
        FilterModel = create_model(
            "FilterModel",
            factory_employee_id=(int, ...),
        )
        user_info = await self.__user_repository.find_one_or_none_by_filter(
            FilterModel(factory_employee_id=factory_employee_id),
        )
        return user_info

    @classmethod
    async def delete_user(
        self,
        user_id: UUID,
    ) -> None:
        await self.__user_repository.delete_by_id(user_id)

    @classmethod
    async def update_user_password(
        self,
        user_id: UUID,
        hashed_password: str,
    ) -> None:
        FilterModel = create_model(
            "FilterModel",
            hashed_password=(str, ...),
        )
        await self.__user_repository.update_instance(
            user_id,
            FilterModel(hashed_password=hashed_password),
        )
