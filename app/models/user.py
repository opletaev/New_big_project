from enum import StrEnum
import uuid

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, str_not_null
from app.models.transaction import Transaction


class UserRoleEnun(StrEnum):
    USER = "Пользователь"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    factory_employee_id: Mapped[int] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )
    hashed_password: Mapped[str_not_null]
    role: Mapped[UserRoleEnun] = mapped_column(
        Enum(
            UserRoleEnun,
            name="role",
        ),
        default=UserRoleEnun.USER,
        server_default=UserRoleEnun.USER.name,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    profile: Mapped["Profile"] = relationship(  # type: ignore
        "Profile",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
    )

    received_cables: Mapped[list["Cable"]] = relationship(  # type: ignore
        back_populates="",
        secondary=Transaction.__tablename__,
        lazy="joined",
    )

    repr_columns_count = 2
