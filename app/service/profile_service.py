from uuid import UUID

from app.repositories.profile import ProfileRepository
from app.schemas.user_schemas import UpdateUserProfileRequestDTO, UserDataDTO


class ProfileService:
    __profile_repository = ProfileRepository()

    @classmethod
    async def create_profile(
        self,
        user_id: UUID,
        user_data: UserDataDTO,
    ) -> None:
        await self.__profile_repository.create_profile(user_id, user_data)

    @classmethod
    async def update_profile(
        self,
        user_id: UUID,
        user_data: UpdateUserProfileRequestDTO,
    ) -> None:
        await self.__profile_repository.update_profile(user_id, user_data)
