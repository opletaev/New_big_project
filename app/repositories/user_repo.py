from datetime import date
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.models.user import User

class UserRepository:  #(AbstractRepository[SUser]):       
    
    async def create_user(
        self,
        factory_employee_id: int,
        work_phone: str,
        hashed_password: str,
        name: str,
        surname: str,
        patronymic: str,
        division: str,
        role: str,
        created_at: date,
    ) -> User:
        async with async_session_maker() as session:
            new_user = User(
                    factory_employee_id=factory_employee_id,
                    work_phone=work_phone,
                    hashed_password=hashed_password,
                    name=name,
                    surname=surname,
                    patronymic=patronymic,
                    division=division,
                    role=role,
                    is_active=True,
                    created_at=created_at,
                )
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user
    
    async def delete_user(self, user_id: UUID):
        async with async_session_maker() as session:
            query = (
                delete(User)
                .where(User.id == user_id)
            )
            await session.execute(query)
            await session.commit()
    
    async def get_user_by_factory_employee_id(
        self, 
        factory_employee_id: int,
        ):  # Дописать, что возвращает функция
        async with async_session_maker() as session:
            query = (
                select(User)
                .where(factory_employee_id == factory_employee_id)
                )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    async def update_user(
        self,
        user_id: UUID,
        **kwargs,
        ):  # Дописать, что возвращает функция
        async with async_session_maker() as session:
            query = (
                update(User)
                .where(User.id == user_id)
                .values(**kwargs)
            )
            await session.execute(query)
            await session.commit()