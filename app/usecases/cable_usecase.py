from sqlalchemy import UUID

from app.schemas.cable_schemas import AddCableDTO, CableDTO, FindCableDTO
from app.service.cable_service import CableService


class CableUsecase:
    @classmethod
    async def add_cable(self, cable: AddCableDTO):
        cable = await CableService.add_cable(cable)

    @classmethod
    async def find_cables(self, cable: FindCableDTO) -> list[CableDTO]:
        cables = await CableService.find_cables(cable)
        return cables

    @classmethod
    async def find_all_cables(self) -> list[CableDTO]:
        cables = await CableService.find_all_cables()
        return cables

    @classmethod
    async def delete_cable(self, cable_id: UUID):
        await CableService.delete_cable(cable_id)
