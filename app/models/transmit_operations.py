from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, annotated_not_nullable_str


class TransmitOperations(Base):
    __tablename__ = "transmit_operations"

    cable: Mapped[annotated_not_nullable_str]
    user: Mapped[annotated_not_nullable_str]
    issue_date: Mapped[datetime] = mapped_column(nullable=False)
    return_date: Mapped[datetime]
