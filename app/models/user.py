from enum import StrEnum
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, annotated_not_nullable_str


class UserRoleEnun(StrEnum):
    USER = "Пользователь"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"


class DivisionEnum(StrEnum):
    LAB1 = "Лаборатория 1"
    LAB2 = "Лаборатория 2"
    LAB3 = "Лаборатория 3"
    LAB5 = "Лаборатория 5"
    LAB6 = "Лаборатория 6"
    LAB7 = "Лаборатория 7"
    LAB8 = "Лаборатория 8"
    PDB = "ПДБ"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    factory_employee_id: Mapped[int] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )
    hashed_password: Mapped[annotated_not_nullable_str]
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
    )


class UserProfile(Base):
    __tablename__ = "profiles"

    surname: Mapped[annotated_not_nullable_str]
    name: Mapped[annotated_not_nullable_str]
    patronymic: Mapped[annotated_not_nullable_str]
    division: Mapped[DivisionEnum] = mapped_column(nullable=False)
    phone_number: Mapped[annotated_not_nullable_str]
    is_active: Mapped[bool]
    role: Mapped[UserRoleEnun] = mapped_column(
        default=UserRoleEnun.USER, server_default=UserRoleEnun.USER.name
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="profile", uselist=False, passive_deletes=True
    )
    # recevied_cables: Mapped[list["Cable"]] = mapped_column(
    #     ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    # )
