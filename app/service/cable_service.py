from uuid import UUID

from app.models.cable import Cable
from app.repositories.cable import CableRepository
from app.schemas.cable_schemas import AddCableDTO, FindCableDTO, UpdateCableDTO


class CableService:
    __cable_repository = CableRepository()

    @classmethod
    async def add_cable(self, cable: AddCableDTO) -> bool:
        return await self.__cable_repository.add(cable)

    @classmethod
    async def find_cable_by_id(self, cable_id: UUID):
        cable = await self.__cable_repository.find_one_or_none_by_id(cable_id)
        return cable

    @classmethod
    async def find_cables_by_filter(self, cable: FindCableDTO) -> list[Cable] | None:
        cables = await self.__cable_repository.find_all_by_filter(cable)
        return cables

    @classmethod
    async def find_all_cables(self) -> list[Cable] | None:
        cables = await self.__cable_repository.find_all()
        return cables

    @classmethod
    async def cables_to_service_in(self, date) -> list[Cable] | None:
        cables = await self.__cable_repository.cables_to_service_in(date)
        return cables

    @classmethod
    async def update_cable_info(
        self,
        cable_id: UUID,
        cable_info: UpdateCableDTO,
    ) -> None:
        await self.__cable_repository.update_instance(cable_id, cable_info)

    @classmethod
    async def delete_cable(self, cable_id: UUID) -> None:
        await self.__cable_repository.delete_by_id(cable_id)
