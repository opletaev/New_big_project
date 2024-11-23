from datetime import datetime
from enum import StrEnum
import uuid

from sqlalchemy import (
    UUID, Column, DateTime, ForeignKey, String, Boolean, Integer, Null
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


class CableStatusEnum(StrEnum):
    AVAILABLE = "В наличии"
    GIVEN = "Выдан"
    ON_SERVICE = "На поверке"


class UserRoleEnun(StrEnum):
    USER = "Пользователь"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"
    

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    factory_employee_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[annotated_not_nullable_str]
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        lazy="joined"
    )
    
    
class Profile(Base):
    __tablename__ = "profiles"
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )    
    surname: Mapped[annotated_not_nullable_str]
    name: Mapped[annotated_not_nullable_str]
    patronymic: Mapped[annotated_not_nullable_str]
    division: Mapped[DivisionEnum] = mapped_column(nullable=False)
    phone_number: Mapped[annotated_not_nullable_str]
    is_active: Mapped[bool]
    role: Mapped[UserRoleEnun] = mapped_column(
        default=UserRoleEnun.USER, server_default=UserRoleEnun.USER.name
        )
    
    
class PDB_Storage(Base):
    __tablename__ = "pdb_storage"
    
    division: Mapped[DivisionEnum] = mapped_column(
        default=DivisionEnum.PDB, server_default=DivisionEnum.PDB.name
        )
    phone_number: Mapped[annotated_not_nullable_str]
    items: Mapped[list["Cable"]] = relationship(
        "Cable",
        back_populates="storage",
        cascade="all, delete-orphan"
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
        "PDB_Storage",  # Здесь используется строка вместо класса
        back_populates="items",
    )
    

# class Operation(Base):
#     __tablename__ = "operations"
#     pass