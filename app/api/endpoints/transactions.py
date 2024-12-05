from uuid import UUID
from fastapi import APIRouter

from app.dto.transaction import AddTransactionDTO, FindTransactionDTO
from app.usecases.cable import CableUsecase


router = APIRouter(
    prefix="/transactions",
    tags=["Транзакции"],
)


@router.post("/add")
async def add_transaction(data: AddTransactionDTO):
    return await CableUsecase.issue_cable(data)


@router.post("/find_by_filter")
async def find_transactions_by_filter(
    filter: FindTransactionDTO,
):
    return await CableUsecase.get_transactions_by_filter(filter)


@router.get("/find_all")
async def get_all_transactions():
    return await CableUsecase.get_all_transactions()


@router.delete("/delete")
async def delete_transaction(cable_id: UUID):
    return await CableUsecase.return_cable(cable_id)
