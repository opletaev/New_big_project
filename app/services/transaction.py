from uuid import UUID
from app.models.transaction import Transaction
from app.repositories.base import AbstractRepository
from app.repositories.transactions import TransactionRepository
from app.dto.transaction import (
    AddTransactionDTO,
    FindTransactionDTO,
    TransactionUpdateDTO,
)


class TransactionService:
    def __init__(self, transaction_repository: AbstractRepository):
        self.transaction_repository = transaction_repository()

    async def add_transaction_record(
        self,
        transaction_data: AddTransactionDTO,
    ) -> bool:
        await self.transaction_repository.add(transaction_data)

    async def find_transactions_by_filter(
        self,
        # transaction_id: UUID | None,
        filter: FindTransactionDTO,
    ) -> list[Transaction] | None:
        transactions = await self.transaction_repository.find_all_by_filter(filter)
        return transactions

    async def get_all_transactions(self) -> list[Transaction]:
        return await self.transaction_repository.find_all()

    async def update_transaction_record(
        self,
        transaction_id: UUID,
        data: TransactionUpdateDTO,
    ) -> bool:
        await self.transaction_repository.update_instance(transaction_id, data)

    async def delete_transaction_record(
        self,
        transaction_id: UUID,
    ) -> bool:
        await self.transaction_repository.delete_by_id(transaction_id)
