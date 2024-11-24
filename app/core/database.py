from datetime import datetime
from typing import Annotated

from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncAttrs
    )
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL
DATEBASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATEBASE_PARAMS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


annotated_not_nullable_str = Annotated[str, mapped_column(nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())