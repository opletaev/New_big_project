from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL
DATEBASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATEBASE_PARAMS, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


str_not_null = Annotated[str, mapped_column(nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    repr_columns_num: int = 3
    repr_columns: tuple[str] = tuple()

    def __repr__(self):
        columns = [
            f"{column}={getattr(self, column)}"
            for idx, column in enumerate(self.__table__.columns.keys())
            if column in self.repr_columns or idx < self.repr_columns_num
        ]
        return f"<{self.__class__.__name__} {','.join(columns)}>"
