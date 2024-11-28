from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models.user import User
from app.models.user import UserProfile
from app.repositories.base import BaseRepository
from app.schemas.user_schemas import SUpdateUserProfileRequest, SUser, SUserProfile


class UserRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = User

    async def create_user_with_profile(  # Вынести в usecase
        self,
        user: SUser,
        user_info: SUserProfile,
    ) -> User:
        print(f"Добавление записей {self.model.__name__} и Profile")
        async with async_session_maker() as session:
            try:
                new_user = User(
                    factory_employee_id=user.factory_employee_id,
                    hashed_password=user.hashed_password,
                )
                session.add(new_user)
                await session.flush()
                print(f"Запись {new_user.__class__.__name__} - Успешно добавлена")
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"Ошибка при добавлении запиcи {new_user.__class__.__name__}")
                raise e

            try:
                user_profile = UserProfile(  # Вынести в ProfileService
                    name=user_info.name,
                    surname=user_info.surname,
                    patronymic=user_info.patronymic,
                    division=user_info.division,
                    phone_number=user_info.phone_number,
                    is_active=True,
                    role=user_info.role,
                    user_id=new_user.id,
                )
                session.add(user_profile)
                await session.commit()
                print(f"Запись {user_profile.__class__.__name__} - Успешно добавлена")
            except SQLAlchemyError as e:
                await session.rollback()
                print(
                    f"Ошибка при добавлении запиcи {user_profile.__class__.__name__} c параметрами ..."
                )
                raise e

            return new_user.id

    async def update_user_profile(  # Вынести в ProfileService
        self,
        user_id: UUID,
        values: SUpdateUserProfileRequest,
    ) -> None:
        values_dict = values.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )
        print(f"Обновление запиcи Profile c ID: {...} c параметрами {values_dict}")
        async with async_session_maker() as session:
            try:
                user = await session.get(User, user_id)
                if user:
                    for key, value in values_dict.items():
                        setattr(user.profile, key, value)
                    await session.commit()
                    print(
                        f"Запиcь {user.profile.__class__} c ID: {user.profile.id} - Обновлена"
                    )
            except SQLAlchemyError as e:
                await session.rollback()
                print(
                    f"Ошибка при обновлении запиcи {user.profile.__class__} c ID: {user.profile.id} c параметрами {values_dict}"
                )
                raise e
