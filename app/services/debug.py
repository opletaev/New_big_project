import logging
from app.models.user import User
from app.repositories.profile import ProfileRepository
from app.repositories.user import UserRepository
from app.dto.user import (
    RegisterUserDTO,
    UserDataDTO,
)
from app.services.auth import AuthService
from app.services.profile import ProfileService
from app.services.user import UserService

log = logging.getLogger(__name__)


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
    ) -> list[User] | None:
        for user_data in users_data:
            hashed_password = AuthService.hashed_password(user_data["password"])
            log.info(msg="Ловлю баг")
            print("Где логгер, сука?!")
            user = RegisterUserDTO(**user_data)
            user = await UserService(UserRepository).create_user(user, hashed_password)
            user_data = UserDataDTO(**user_data)
            await ProfileService(ProfileRepository).create_profile(user.id, user_data)

    async def delete_all_users(self) -> None:
        await UserRepository.delete_all()
