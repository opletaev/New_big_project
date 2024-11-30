from typing import Optional
from app.models.user import User
from app.repositories.profile import ProfileRepository
from app.repositories.user import UserRepository
from app.schemas.user_schemas import (
    AllUserDataDTO,
    CreateUserDTO,
    RegisterUserDTO,
    UserDataDTO,
)
from app.service.auth_service import AuthService
from app.service.profile_service import ProfileService
from app.service.user_service import UserService


class DebugUserService:
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
        }
        for i in range(1, 6)
    ]

    async def create_users_from_dicts(
        self,
        users_data: list[dict] = users_data,
    ) -> Optional[list[User]]:
        for user_data in users_data:
            # new_user = SRegisterUser(**user_data)
            hashed_password = AuthService(UserService).hashed_password(
                user_data["password"]
            )  # Создать DebugUsecase и вынести туда
            user = CreateUserDTO(
                hashed_password=hashed_password,
                **user_data,
            )
            user = await UserService(UserRepository()).create_user(user)
            user_data = UserDataDTO(**user_data)
            await ProfileService(ProfileRepository()).create_profile(user.id, user_data)

        return await UserService(UserRepository()).get_all_users()

    async def delete_all_users(self) -> None:
        await UserRepository.delete_all()
