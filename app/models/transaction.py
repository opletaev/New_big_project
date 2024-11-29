from datetime import datetime
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy import TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.cable import Cable


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    cable_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cables.id"),
        nullable=False,
    )
    cable: Mapped["Cable"] = relationship(  # type: ignore
        "Cable",
        back_populates="active_transactions",
        lazy="joined",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="active_transactions",
        lazy="joined",
    )
    issued_by: Mapped[uuid.UUID] = mapped_column(nullable=False)
    return_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
