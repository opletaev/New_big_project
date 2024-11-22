from datetime import date
from uuid import UUID
from app.schemas.user_schemas import SCreateUser, SShowUser, SUpdateUserRequest
from app.repositories.user_repo import UserRepository
from app.usecases.auth_usecase import AuthUsecase, get_hashed_password


class UserUsecase:
    def __init__(self):
        self.repo = UserRepository

    async def create_user(self, body: SCreateUser):
        user_repo = self.repo()
        hashed_password=get_hashed_password(body.password)
        user = await user_repo.create_user(
            factory_employee_id=body.factory_employee_id,
            work_phone=body.work_phone,
            hashed_password=hashed_password,
            name=body.name,
            surname=body.surname,
            patronymic=body.patronymic,
            division=body.division,
            role="user",
            created_at=date.today()
        )
        return SShowUser(
            user_id=user.id,
            factory_employee_id=user.factory_employee_id,
            work_phone=user.work_phone,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            division=user.division,
            is_active=user.is_active,
        )

    async def delete_user(self, user_id: UUID):
        user_repo = self.repo()
        await user_repo.delete_user(user_id=user_id)

    async def get_user_by_factory_employee_id(self, factory_employee_id: int):
        user_repo = self.repo()
        user = await user_repo.get_user_by_factory_employee_id(
            factory_employee_id=factory_employee_id
            )
        return user

    async def update_user(self, body:SUpdateUserRequest):
        user_repo = self.repo()
        # Добавить считывание user_id
        user_id = AuthUsecase.get_user_id()
        user = await user_repo.update_user(user_id, **body)
        return user