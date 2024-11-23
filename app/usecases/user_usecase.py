from uuid import UUID

from app.schemas.user_schemas import SCreateUser, SShowUser, SUpdateUserRequest
from app.repositories.user import UserRepository
from app.usecases.auth_usecase import get_hashed_password


class UserUsecase:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def create_user_with_profile(self, body: SCreateUser):
        user_repo = self.repository
        hashed_password=get_hashed_password(body.password)
        user, user_profile = await user_repo.create_user_with_profile(
            body, hashed_password
            )
        return SShowUser(
            user_id=user.id,
            factory_employee_id=user.factory_employee_id,
            phone_number=user_profile.phone_number,
            name=user_profile.name,
            surname=user_profile.surname,
            patronymic=user_profile.patronymic,
            division=user_profile.division,
            is_active=user_profile.is_active,
        )


    async def delete_user(self, user_id: UUID):
        user_repo = self.repository
        await user_repo.delete_instance(instance_id=user_id)


    async def get_user_by_factory_employee_id(self, factory_employee_id: int):
        print(factory_employee_id)
        user_repo = self.repository
        user = await user_repo.get_user_by_factory_employee_id(
            factory_employee_id=factory_employee_id
            )
        return user


    async def update_user(self, body:SUpdateUserRequest, user_id: UUID):
        print(body, '\n', user_id)
        user_repo = self.repository
        # Добавить считывание user_id
        body = {key: value for key, value in body if value}
        print(body)
        user = await user_repo.update_user(user_id, **body)
        return user