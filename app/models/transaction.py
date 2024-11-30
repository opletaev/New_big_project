from datetime import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    cable_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "cables.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    issued_by: Mapped[uuid.UUID] = mapped_column(nullable=False)
    return_date: Mapped[datetime]
    is_active: Mapped[bool] = mapped_column(nullable=False)
