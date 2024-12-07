from uuid import UUID

from app.repositories.base import AbstractRepository
from app.dto.user import UpdateUserProfileRequestDTO, UserDataDTO


class ProfileService:
    def __init__(self, profile_repository: AbstractRepository):
        self.profile_repository = profile_repository()

    async def create_profile(
        self,
        user_id: UUID,
        user_data: UserDataDTO,
    ) -> bool:
        await self.profile_repository.create_profile(user_id, user_data)
        return True

    async def update_profile(
        self,
        user_id: UUID,
        user_data: UpdateUserProfileRequestDTO,
    ) -> str:
        await self.profile_repository.update_profile(user_id, user_data)
        return "Данные обновлены"  # TODO: Придумать, что вернуть вместо этого
