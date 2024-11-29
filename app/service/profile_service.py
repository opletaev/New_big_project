from uuid import UUID

from app.repositories.profile import ProfileRepository
from app.schemas.user_schemas import SCreateProfile, SUpdateUserProfileRequest, SUser


class ProfileService:
    def __init__(self, repository: ProfileRepository) -> None:
        self.repository = repository

    async def create_profile(
        self,
        user_id: UUID,
        user_data: SCreateProfile,
    ):
        await self.repository.create_profile(user_id, user_data)

    async def update_profile(
        self,
        user_id: UUID,
        new_data: SUpdateUserProfileRequest,
    ) -> None:
        await self.repository.update_profile(user_id, new_data)
