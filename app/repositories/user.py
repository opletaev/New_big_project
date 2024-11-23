from uuid import UUID

from sqlalchemy import delete, select, update

from app.core.database import async_session_maker
from app.models.user import User
from app.models.user import UserProfile
from app.schemas.user_schemas import SCreateUser


class UserRepository:  #(AbstractRepository[SUser]):       
    
    async def create_user_with_profile(
        self,
        body: SCreateUser,
        hashed_password: str,
    ) -> User:
        async with async_session_maker() as session:
            try:
                new_user = User(
                        factory_employee_id=body.factory_employee_id,
                        hashed_password=hashed_password,
                        )
                session.add(new_user)
                await session.flush()

                user_profile = UserProfile(
                    name=body.name,
                    surname=body.surname,
                    patronymic=body.patronymic,
                    division=body.division,
                    phone_number=body.phone_number,
                    is_active=True,
                    role="Пользователь",
                    user_id=new_user.id,
                    )
                session.add(user_profile)
                await session.commit()
            
            except Exception as e:
                await session.rollback()
                raise e

            return new_user, user_profile
    
    
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
        print(factory_employee_id)
        async with async_session_maker() as session:
            query = (
                select(User)
                .where(User.factory_employee_id == factory_employee_id)
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