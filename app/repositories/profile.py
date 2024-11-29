from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models.user import User, UserProfile
from app.repositories.base import BaseRepository
from app.schemas.user_schemas import SUpdateUserProfileRequest


class ProfileRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = UserProfile

    async def create_profile(
        self,
        user_id: UUID,
        user_data: SUpdateUserProfileRequest,
    ):
        async with async_session_maker() as session:
            try:
                user_profile = UserProfile(
                    name=user_data.name,
                    surname=user_data.surname,
                    patronymic=user_data.patronymic,
                    division=user_data.division,
                    phone_number=user_data.phone_number,
                    is_active=True,
                    role=user_data.role,
                    user_id=user_id,
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

    async def update_profile(
        self,
        user_id: UUID,
        values: SUpdateUserProfileRequest,
    ) -> None:
        values_dict = values.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )
        print(f"Обновление запиcи Profile c ID: {user_id} c параметрами {values_dict}")
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
