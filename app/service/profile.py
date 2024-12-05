from uuid import UUID

from app.repository.profile import ProfileRepository
from app.dto.user import UpdateUserProfileRequestDTO, UserDataDTO


class ProfileService:
    __profile_repository = ProfileRepository()

    @classmethod
    async def create_profile(
        cls,
        user_id: UUID,
        user_data: UserDataDTO,
    ) -> None:
        await cls.__profile_repository.create_profile(user_id, user_data)

    @classmethod
    async def update_profile(
        cls,
        user_id: UUID,
        user_data: UpdateUserProfileRequestDTO,
    ) -> None:
        await cls.__profile_repository.update_profile(user_id, user_data)
