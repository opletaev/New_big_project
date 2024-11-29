from datetime import datetime
from enum import StrEnum
from os import name
import uuid

from sqlalchemy import TIMESTAMP, UUID, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, annotated_not_nullable_str

# from app.models.transaction import Transaction


class CableStatusEnum(StrEnum):
    AVAILABLE = "В наличии"
    ISSUED = "Выдан"
    ON_SERVICE = "На поверке"


class Cable(Base):
    __tablename__ = "cables"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    index: Mapped[annotated_not_nullable_str]
    group: Mapped[annotated_not_nullable_str]
    assembly: Mapped[annotated_not_nullable_str]
    factory_number: Mapped[annotated_not_nullable_str]
    last_service: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    next_service: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    status: Mapped[CableStatusEnum] = mapped_column(
        Enum(CableStatusEnum, name="status"),
        nullable=False,
        default=CableStatusEnum.AVAILABLE.name,
    )
    active_transactions: Mapped[list["Transaction"]] = relationship(  # type: ignore
        "Transaction",
        back_populates="cable",
        passive_deletes=True,
    )
