from uuid import UUID
from app.models.transaction import Transaction
from app.repositories.transactions import TransactionRepository
from app.schemas.transaction_schemas import (
    AddTransactionDTO,
    FindTransactionDTO,
    TransactionUpdateDTO,
)


class TransactionService:
    __transaction_repository = TransactionRepository()

    @classmethod
    async def add_transaction_record(
        self,
        transaction_data: AddTransactionDTO,
    ) -> bool:
        await self.__transaction_repository.add(transaction_data)

    @classmethod
    async def find_transactions_by_filter(
        self,
        # transaction_id: UUID | None,
        filter: FindTransactionDTO,
    ) -> list[Transaction] | None:
        transactions = await self.__transaction_repository.find_all_by_filter(filter)
        return transactions

    @classmethod
    async def get_all_transactions(self) -> list[Transaction]:
        return await self.__transaction_repository.find_all()

    @classmethod
    async def update_transaction_record(
        self,
        transaction_id: UUID,
        data: TransactionUpdateDTO,
    ) -> bool:
        await self.__transaction_repository.update_instance(transaction_id, data)

    @classmethod
    async def delete_transaction_record(
        self,
        transaction_id: UUID,
    ) -> bool:
        await self.__transaction_repository.delete_by_id(transaction_id)
