from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.core.logger import repository_log as logger
from app.models.profile import Profile
from app.models.user import User
from app.repositories.base import BaseRepository
from app.dto.user import UpdateUserProfileRequestDTO, UserDataDTO


class ProfileRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = Profile

    async def create_profile(
        self,
        user_id: UUID,
        user_data: UserDataDTO,
    ) -> bool:
        logger.info(
            "Add a profile record for user",
            extra={
                "model": "Profile",
                "user_id": user_id,
                "user_data": user_data,
            },
        )
        async with async_session_maker() as session:
            try:
                user_profile = Profile(
                    name=user_data.name,
                    surname=user_data.surname,
                    patronymic=user_data.patronymic,
                    division=user_data.division,
                    phone_number=user_data.phone_number,
                    user_id=user_id,
                )
                session.add(user_profile)
                await session.commit()
                logger.info(
                    "A record - Added",
                    extra={
                        "model": user_profile.__class__.__name__,
                        "user_id": user_id,
                        "user_data": user_data,
                    },
                )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot add a record"
                extra = {
                    "model": user_profile.__class__.__name__,
                    "user_id": user_id,
                    "user_data": user_data,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return True

    async def update_profile(
        self,
        user_id: UUID,
        user_data: UpdateUserProfileRequestDTO,
    ) -> bool:
        values_dict = user_data.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )
        logger.info(
            "Update a profile record for user",
            extra={
                "model": "Profile",
                "user_id": user_id,
                "user_data": user_data,
            },
        )
        async with async_session_maker() as session:
            try:
                user = await session.get(User, user_id)
                if user:
                    for key, value in values_dict.items():
                        setattr(user.profile, key, value)
                    await session.commit()
                    logger.info(
                        "A profile record for user - Updated",
                        extra={
                            "model": "Profile",
                            "user_id": user_id,
                            "user_data": user_data,
                        },
                    )
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot update a record"
                extra = {
                    "model": user.profile.__class__,
                    "user_id": user.profile.id,
                    "user_data": values_dict,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return True
