from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL
DATEBASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATEBASE_PARAMS)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass