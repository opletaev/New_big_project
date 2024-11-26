from sqlalchemy import delete
from app.core.database import async_session_maker
from app.models.user import User, UserProfile
from app.utils import get_hashed_password


users_data = [
    {
        "factory_employee_id": i**2,
        "password": "test",
        "surname": f"test_user{i}",
        "name": f"test_user{i}",
        "patronymic": f"test_user{i}",
        "division": "Лаборатория 1",
        "phone_number": "00-00",
        "is_active": False,
        } for i in range(1,6)
    ]


async def create_users_from_dicts(
    users_data: list[dict] = users_data
):
    print(*users_data, sep="\n")
    async with async_session_maker() as session:
        users_list = []
        
        for user_data in users_data:
            new_user = User(
                factory_employee_id=user_data["factory_employee_id"],
                hashed_password=get_hashed_password(user_data["password"]),
                )
            session.add(new_user)
            await session.flush()

            user_profile = UserProfile(
                surname=user_data["surname"],
                name=user_data["name"],
                patronymic=user_data["patronymic"],
                division=user_data["division"],
                phone_number=user_data["phone_number"],
                is_active=user_data["is_active"],
                role="Пользователь",
                user_id=new_user.id,
            )
            session.add(user_profile)
            await session.flush()
            users_list.append((new_user, user_profile))  

        try:
            await session.commit()  # Коммитим изменения
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при создании пользователей: {e}")
            raise 
        return users_list
    
    
async def delete_users():
    async with async_session_maker() as session:
        query = (
            delete(User)
        )
        await session.execute(query)
        await session.commit()