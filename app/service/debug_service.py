from app.repositories.user import UserRepository
from app.schemas.user_schemas import SCreateUser
from app.service.user_service import UserService


users_data = [
    {
        "factory_employee_id": i**2,
        "password": "testtest",
        "surname": f"TestUser",
        "name": f"TestUser",
        "patronymic": f"TestUser",
        "division": "Лаборатория 1",
        "phone_number": "00-00",
        "is_active": False,
        } for i in range(1,6)
    ]


async def create_users_from_dicts(
    users_data: list[dict] = users_data
):
    for user_data in users_data:
        user_data = SCreateUser(**user_data)
        await UserService(UserRepository()).create_user_with_profile(body=user_data)
    
    return await UserService(UserRepository()).get_all_users()
    
    
async def delete_all():
    await UserRepository.delete_all()
