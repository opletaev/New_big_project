from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from app.api.dependencies import transaction_service
from app.dto.transaction import AddTransactionDTO, FindTransactionDTO
from app.services.transaction import TransactionService


router = APIRouter(
    prefix="/transactions",
    tags=["Транзакции"],
)


@router.post("/add")
async def add_transaction(
    data: AddTransactionDTO,
    transaction_service: Annotated[TransactionService, Depends(transaction_service)],
):
    return await transaction_service.add_transaction_record(data)


@router.post("/find_by_filter")
async def find_transactions_by_filter(
    filter: FindTransactionDTO,
    transaction_service: Annotated[TransactionService, Depends(transaction_service)],
):
    return await transaction_service.find_transactions_by_filter(filter)


@router.get("/find_all")
async def get_all_transactions(
    transaction_service: Annotated[TransactionService, Depends(transaction_service)],
):
    return await transaction_service.get_all_transactions()


@router.delete("/delete")
async def delete_transaction(
    transaction_id: UUID,
    transaction_service: Annotated[TransactionService, Depends(transaction_service)],
):
    return await transaction_service.delete_transaction_record(transaction_id)
