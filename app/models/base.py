from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    repr_columns_count: int = 3
    repr_columns: tuple[str] = tuple()

    # Выводит ограниченное число колонок и/или только выбранные
    def __repr__(self):
        columns = [
            f"{column}={getattr(self, column)}"
            for idx, column in enumerate(self.__table__.columns.keys())
            if column in self.repr_columns or idx < self.repr_columns_count
        ]
        return f"<{self.__class__.__name__} {','.join(columns)}>"
