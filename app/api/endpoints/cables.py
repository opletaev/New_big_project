from typing import Optional
from uuid import UUID
from fastapi import APIRouter

from app.schemas.cable_schemas import AddCableDTO, CableDTO, FindCableDTO
from app.usecases.cable_usecase import CableUsecase


router = APIRouter(
    prefix="/cables",
    tags=["Кабели"],
)


@router.post("/add")
async def add_cable(cable: AddCableDTO):
    cable = await CableUsecase.add_cable(cable)
    return cable


@router.post("/search")
async def find_cables(cables: FindCableDTO) -> list[CableDTO]:
    cables = await CableUsecase.find_cables(cables)
    return cables


@router.get("/all")
async def find_all_cables() -> list[CableDTO]:
    cables = await CableUsecase.find_all_cables()
    return cables


@router.delete("/delete")
async def delete_cable(cable_id: UUID):
    await CableUsecase.delete_cable(cable_id)
