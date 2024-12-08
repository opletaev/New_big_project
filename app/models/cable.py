from datetime import date
from enum import StrEnum
import uuid

from sqlalchemy import UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import str_not_null
from app.models.base import Base
from app.models.transaction import Transaction


class CableStatusEnum(StrEnum):
    AVAILABLE = "В наличии"
    ISSUED = "Выдан"
    ON_SERVICE = "На поверке"


class Cable(Base):

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    index: Mapped[str_not_null]
    group: Mapped[str_not_null]
    assembly: Mapped[str_not_null]
    factory_number: Mapped[str_not_null]
    last_service: Mapped[date] = mapped_column(nullable=False)
    next_service: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[CableStatusEnum] = mapped_column(
        Enum(
            CableStatusEnum,
            name="status",
        ),
        nullable=False,
        default=CableStatusEnum.AVAILABLE.name,
    )

    issued_to: Mapped[list["User"]] = relationship(  # type: ignore
        back_populates="received_cables",
        secondary=Transaction.__tablename__,
        lazy="joined",
    )

    repr_columns_count = 5
