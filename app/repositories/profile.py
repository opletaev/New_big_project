from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.models.user import UserProfile


class ProfileRepository:  #(AbstractRepository[SUser]):       
    
    async def create_profile(
        user_id: UUID,        
        phone_number: str,
        name: str,
        surname: str,
        patronymic: str,
        division: str,
        role: str,
        session: AsyncSession,
        ):
        async with async_session_maker() as session:
            user_profile = UserProfile(
                phone_number=phone_number,
                name=name,
                surname=surname,
                patronymic=patronymic,
                division=division,
                role=role,
                is_active=True,
                user_id=user_id
            )
            session.add(user_profile)
            await session.flush()
            return user_profile
        