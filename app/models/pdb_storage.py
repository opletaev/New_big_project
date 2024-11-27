from datetime import datetime
from enum import StrEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, annotated_not_nullable_str
from app.models.user import DivisionEnum


class CableStatusEnum(StrEnum):
    AVAILABLE = "В наличии"
    GIVEN = "Выдан"
    ON_SERVICE = "На поверке"


class PDB_Storage(Base):
    __tablename__ = "pdb_storage"

    division: Mapped[DivisionEnum] = mapped_column(
        default=DivisionEnum.PDB, server_default=DivisionEnum.PDB.name
    )
    phone_number: Mapped[annotated_not_nullable_str]
    items: Mapped[list["Cable"]] = relationship(
        "Cable",
        back_populates="storage",
        cascade="all, delete-orphan",
    )
    # employees


class Cable(Base):
    __tablename__ = "cables"

    index: Mapped[annotated_not_nullable_str]
    group: Mapped[annotated_not_nullable_str]
    assembly: Mapped[annotated_not_nullable_str]
    factory_number: Mapped[annotated_not_nullable_str]
    last_service: Mapped[datetime] = mapped_column(nullable=False)
    next_service: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[CableStatusEnum] = mapped_column(nullable=False)
    storage: Mapped["PDB_Storage"] = relationship(
        "PDB_Storage",
        back_populates="items",
    )
