from uuid import UUID

from app.models.cable import Cable
from app.repository.cable import CableRepository
from app.dto.cable import AddCableDTO, FindCableDTO, UpdateCableDTO


class CableService:
    __cable_repository = CableRepository()

    @classmethod
    async def add_cable(cls, cable: AddCableDTO) -> bool:
        return await cls.__cable_repository.add(cable)

    @classmethod
    async def find_cable_by_id(cls, cable_id: UUID):
        cable = await cls.__cable_repository.find_one_or_none_by_id(cable_id)
        return cable

    @classmethod
    async def find_cables_by_filter(cls, cable: FindCableDTO) -> list[Cable] | None:
        cables = await cls.__cable_repository.find_all_by_filter(cable)
        return cables

    @classmethod
    async def find_all_cables(cls) -> list[Cable] | None:
        cables = await cls.__cable_repository.find_all()
        return cables

    @classmethod
    async def cables_to_service_in(cls, date) -> list[Cable] | None:
        cables = await cls.__cable_repository.cables_to_service_in(date)
        return cables

    @classmethod
    async def update_cable_info(
        cls,
        cable_id: UUID,
        cable_info: UpdateCableDTO,
    ) -> None:
        await cls.__cable_repository.update_instance(cable_id, cable_info)

    @classmethod
    async def delete_cable(cls, cable_id: UUID) -> None:
        await cls.__cable_repository.delete_by_id(cable_id)
