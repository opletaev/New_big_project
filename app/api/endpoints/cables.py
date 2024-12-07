from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.api.dependencies import cable_service
from app.dto.cable import (
    AddCableDTO,
    CableDTO,
    FindCableDTO,
    UpdateCableDTO,
)
from app.services.cable import CableService


router = APIRouter(
    prefix="/cables",
    tags=["Кабели"],
)


@router.post("/add", name="Добавить кабель")
async def add_cable(
    cable: AddCableDTO,
    cable_service: Annotated[CableService, Depends(cable_service)],
) -> UUID:
    await cable_service.add_cable(cable)
    cable = await cable_service.find_cables_by_filter(
        cable
    )  # TODO: Изменить на поиск одного кабеля
    return cable[0].id


@router.patch("/update", name="Обновить сроки поверки")
async def update_service_dates(
    cable_id: UUID,
    service_dates: UpdateCableDTO,
    cable_service: Annotated[CableService, Depends(cable_service)],
) -> None:
    await cable_service.update_cable_info(cable_id, service_dates)


@router.post("/search", name="Поиск кабелей")
@cache(expire=60)
async def find_cables(
    filter: FindCableDTO,
    cable_service: Annotated[CableService, Depends(cable_service)],
) -> list[CableDTO]:
    cables = await cable_service.find_cables_by_filter(filter)
    return cables


@router.get("/all", name="Вывести все кабели")
@cache(expire=60)
async def find_all_cables(
    cable_service: Annotated[CableService, Depends(cable_service)],
) -> list[CableDTO]:
    cables = await cable_service.find_all_cables()
    return cables


@router.get("/service_this_month", name="Кабели на поверку")
async def to_service_in_this_month(
    cable_service: Annotated[CableService, Depends(cable_service)],
):
    today = date.today()
    cables = await cable_service.cables_to_service_in(today)
    return cables


@router.delete("/delete", name="Удалить кабель")
async def delete_cable(
    cable_id: UUID,
    cable_service: Annotated[CableService, Depends(cable_service)],
):
    await cable_service.delete_cable(cable_id)
