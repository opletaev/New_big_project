from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import update

from app.core.database import async_session_maker
from app.models.user import User
from app.models.user import UserProfile
from app.repositories.base import BaseRepository
from app.schemas.user_schemas import SUser, SUserProfile


class UserRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = User

    async def create_user_with_profile(
        self,
        user: SUser,
        user_info: SUserProfile,
    ) -> User:
        async with async_session_maker() as session:
            try:
                new_user = User(
                    factory_employee_id=user.factory_employee_id,
                    hashed_password=user.hashed_password,
                )
                session.add(new_user)
                await session.flush()

                user_profile = UserProfile(
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

            except Exception as e:
                await session.rollback()
                raise e

            return new_user.id

    async def update_user_profile(
        self,
        user_id: UUID,
        values: BaseModel,
    ):
        values_dict = values.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )
        async with async_session_maker() as session: 
            user = await session.get(User, user_id)
            if user:
                if phone_number := values_dict["phone_number"]:
                    user.profile.phone_number = phone_number
                if division := values_dict["division"]:
                    user.profile.division = division
                await session.commit()
