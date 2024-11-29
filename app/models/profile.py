from enum import StrEnum
import uuid

from sqlalchemy import (
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, annotated_not_nullable_str


class DivisionEnum(StrEnum):
    LAB1 = "Лаборатория 1"
    LAB2 = "Лаборатория 2"
    LAB3 = "Лаборатория 3"
    LAB5 = "Лаборатория 5"
    LAB6 = "Лаборатория 6"
    LAB7 = "Лаборатория 7"
    LAB8 = "Лаборатория 8"
    PDB = "ПДБ"


class Profile(Base):
    __tablename__ = "profiles"

    surname: Mapped[annotated_not_nullable_str]
    name: Mapped[annotated_not_nullable_str]
    patronymic: Mapped[annotated_not_nullable_str]
    division: Mapped[DivisionEnum] = mapped_column(
        Enum(DivisionEnum, name="division"),
        nullable=False,
    )
    phone_number: Mapped[annotated_not_nullable_str]
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="profile",
        uselist=False,
        passive_deletes=True,
    )
