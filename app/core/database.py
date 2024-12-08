from typing import Annotated

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import mapped_column

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL
DATEBASE_PARAMS = {}
DB_ECHO = settings.DB_ECHO

engine = create_async_engine(DATABASE_URL, **DATEBASE_PARAMS, echo=DB_ECHO)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

str_not_null = Annotated[str, mapped_column(nullable=False)]


class DatabaseSession:
    def __init__(self, url: str, params: dict = {}, echo: bool = False):
        self.engine = create_async_engine(
            url=DATABASE_URL,
            echo=False,
            **params,
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_session = DatabaseSession(DATABASE_URL, echo=DB_ECHO)
