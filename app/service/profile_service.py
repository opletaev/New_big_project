from uuid import UUID

from app.repositories.profile import ProfileRepository
from app.schemas.user_schemas import SUpdateUserProfileRequest, SUserData


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository) -> None:
        self.repository = profile_repository

    async def create_profile(
        self,
        user_id: UUID,
        user_data: SUserData,
    ):
        await self.repository.create_profile(user_id, user_data)

    async def update_profile(
        self,
        user_id: UUID,
        user_data: SUpdateUserProfileRequest,
    ) -> None:
        await self.repository.update_profile(user_id, user_data)
