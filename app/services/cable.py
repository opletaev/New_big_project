from uuid import UUID

from pydantic import create_model

from app.models.cable import Cable
from app.repositories.base import AbstractRepository
from app.dto.cable import AddCableDTO, FindCableDTO, UpdateCableDTO


class CableService:
    def __init__(self, cable_repository: AbstractRepository):
        self.cable_repository = cable_repository()

    async def add_cable(self, cable: AddCableDTO) -> bool:
        return await self.cable_repository.add(
            cable
        )  # TODO: Добавить проверку, что такой кабель существует

    async def find_cable_by_id(self, cable_id: UUID):
        FilterModel = create_model(
            "FilterModel",
            id=(UUID, ...),
        )
        cable = await self.cable_repository.find_one_or_none_by_filter(
            FilterModel(id=cable_id),
        )
        return cable

    async def find_cables_by_filter(self, cable: FindCableDTO) -> list[Cable] | None:
        cables = await self.cable_repository.find_all_by_filter(cable)
        return cables

    async def find_all_cables(self) -> list[Cable] | None:
        cables = await self.cable_repository.find_all()
        return cables

    async def cables_to_service_in(self, date) -> list[Cable] | None:
        cables = await self.cable_repository.cables_to_service_in(date)
        return cables

    async def update_cable_info(
        self,
        cable_id: UUID,  # TODO: Добавить проверку, что такой кабель существует
        cable_info: UpdateCableDTO,
    ) -> None:
        await self.cable_repository.update_instance(cable_id, cable_info)

    async def delete_cable(self, cable_id: UUID) -> None:
        await self.cable_repository.delete_by_id(cable_id)
