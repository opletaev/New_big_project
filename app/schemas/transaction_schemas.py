from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionUpdateDTO(BaseModel):
    user_id: UUID
    cable_id: UUID
    is_active: bool | None = True


class AddTransactionDTO(TransactionUpdateDTO):
    issued_by: UUID


class FindTransactionDTO(BaseModel):
    id: UUID = None
    user_id: UUID = None
    cable_id: UUID = None
    is_active: bool = True
    issued_by: UUID = None
    created_at: date = None


# class TransactionDTO(FindTransactionDTO):
