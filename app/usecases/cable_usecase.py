from datetime import date
from sqlalchemy import UUID

from app.models.cable import Cable
from app.models.transaction import Transaction
from app.schemas.cable_schemas import AddCableDTO, FindCableDTO, UpdateCableDTO
from app.schemas.transaction_schemas import AddTransactionDTO, FindTransactionDTO
from app.service.cable_service import CableService
from app.service.transaction_service import TransactionService


class CableUsecase:

    @classmethod
    async def add_cable(self, cable: AddCableDTO) -> UUID:
        await CableService.add_cable(cable)
        cable = await CableService.find_cables_by_filter(cable)
        return cable[0].id

    @classmethod
    async def find_cables_by_filter(self, cable: FindCableDTO) -> list[Cable] | None:
        cables = await CableService.find_cables_by_filter(cable)
        return cables

    @classmethod
    async def find_all_cables(self) -> list[Cable] | None:
        cables = await CableService.find_all_cables()
        return cables

    @classmethod
    async def to_service_in_this_month(self) -> list[Cable] | None:
        today = date.today()
        cables = await CableService.cables_to_service_in(today)
        return cables

    @classmethod
    async def update_cable_info(
        self,
        cable_id: UUID,
        cable_info: UpdateCableDTO,
    ) -> None:
        await CableService.update_cable_info(cable_id, cable_info)

    @classmethod
    async def delete_cable(self, cable_id: UUID) -> None:
        await CableService.delete_cable(cable_id)

    @classmethod
    async def issue_cable(
        self,
        data: AddTransactionDTO,
    ) -> bool:
        return await TransactionService.add_transaction_record(data)

    @classmethod
    async def return_cable(
        self,
        cable_id: UUID,
        cable: FindCableDTO = None,  # ???
    ) -> bool:
        return await TransactionService.delete_transaction_record(cable_id)

    @classmethod
    async def get_all_transactions(self) -> list[Transaction]:
        transactions = await TransactionService.get_all_transactions()
        return transactions

    @classmethod
    async def get_transactions_by_filter(
        self,
        filter: FindTransactionDTO,
    ) -> list[Transaction]:
        transactions = await TransactionService.find_transactions_by_filter(filter)
        return transactions
