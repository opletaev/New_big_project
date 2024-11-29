from enum import StrEnum
from typing import Optional
import uuid

from sqlalchemy import (
    UUID,
    Boolean,
    Enum,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, annotated_not_nullable_str
from app.models.transaction import Transaction


class UserRoleEnun(StrEnum):
    USER = "Пользователь"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    factory_employee_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
        index=True,
    )
    hashed_password: Mapped[annotated_not_nullable_str]
    role: Mapped[UserRoleEnun] = mapped_column(
        Enum(UserRoleEnun, name="role"),
        default=UserRoleEnun.USER,
        server_default=UserRoleEnun.USER.name,
    )
    profile: Mapped["Profile"] = relationship(  # type: ignore
        "Profile",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
    )
    active_transactions: Mapped[Optional[list["Transaction"]]] = relationship(  # type: ignore
        "Transaction",
        back_populates="user",
        passive_deletes=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
