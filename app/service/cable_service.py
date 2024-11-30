from uuid import UUID

from app.repositories.cable import CableRepository
from app.schemas.cable_schemas import AddCableDTO, CableDTO, FindCableDTO


class CableService:
    __cable_repository = CableRepository()

    @classmethod
    async def add_cable(self, cable: AddCableDTO):
        cable = await self.__cable_repository.add(cable)
        return cable

    @classmethod
    async def find_cables(self, cable: FindCableDTO) -> list[CableDTO]:
        cables = await self.__cable_repository.find_all_by_filter(cable)
        return cables

    @classmethod
    async def find_all_cables(self) -> list[CableDTO]:
        cables = await self.__cable_repository.find_all()
        return cables

    @classmethod
    async def delete_cable(self, cable_id: UUID):
        await self.__cable_repository.delete_by_id(cable_id)
