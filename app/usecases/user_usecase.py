from uuid import UUID

from app.models.user import User
from app.schemas.user_schemas import SCreateUser, SUpdateUserRequest
from app.repositories.user import UserRepository
from app.usecases.auth_usecase import get_hashed_password


class UserUsecase:
    def __init__(
        self, 
        repository: UserRepository,
        ) -> None:
        self.repository = repository


    async def create_user_with_profile(
        self, 
        body: SCreateUser,
        ) -> UUID:
        user_repo = self.repository
        hashed_password=get_hashed_password(body.password)
        user_id = await user_repo.create_user_with_profile(
            body, hashed_password
            )
        return user_id


    async def delete_user(
        self, 
        user_id: UUID,
        ) -> None:
        user_repo = self.repository
        await user_repo.delete_instance(instance_id=user_id)
        
        
    async def get_all_users(self) -> list[User]:
        users = await self.repository.get_all()
        return users
    
    
    async def get_user_by_id(
        self, 
        user_id: UUID,
        ) -> User | None:
        user = await self.repository.get_by_id(user_id)
        return user


    async def get_user_by_factory_employee_id(
        self, 
        factory_employee_id: int,
        ) -> User | None:
        print(factory_employee_id)
        user_repo = self.repository
        user = await user_repo.get_user_by_factory_employee_id(
            factory_employee_id=factory_employee_id
            )
        if not user:
            return None
        
        return user
        

    async def update_user(
        self, 
        body: SUpdateUserRequest, 
        user_id: UUID,
        ):
        print(body, '\n', user_id)
        user_repo = self.repository
        # Добавить считывание user_id
        body = {key: value for key, value in body if value}
        print(body)
        user = await user_repo.update_user(user_id, **body)
        return user