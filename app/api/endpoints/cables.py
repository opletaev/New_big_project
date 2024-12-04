from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.schemas.cable_schemas import (
    AddCableDTO,
    CableDTO,
    FindCableDTO,
    UpdateCableDTO,
)
from app.usecases.cable_usecase import CableUsecase


router = APIRouter(
    prefix="/cables",
    tags=["Кабели"],
)


@router.post("/add", name="Добавить кабель")
async def add_cable(cable: AddCableDTO) -> UUID:
    cable = await CableUsecase.add_cable(cable)
    return cable


@router.patch("/update", name="Обновить сроки поверки")
async def update_service_dates(cable_id: UUID, service_dates: UpdateCableDTO) -> None:
    await CableUsecase.update_cable_info(cable_id, service_dates)


@router.post("/search", name="Поиск кабелей")
@cache(expire=60)
async def find_cables(filter: FindCableDTO) -> list[CableDTO]:
    cables = await CableUsecase.find_cables_by_filter(filter)
    return cables


@router.get("/all", name="Вывести все кабели")
@cache(expire=60)
async def find_all_cables() -> list[CableDTO]:
    cables = await CableUsecase.find_all_cables()
    return cables


@router.get("/service_this_month", name="Кабели на поверку")
async def to_service_in_this_month():
    cables = await CableUsecase.to_service_in_this_month()
    return cables


@router.delete("/delete", name="Удалить кабель")
async def delete_cable(cable_id: UUID):
    await CableUsecase.delete_cable(cable_id)
