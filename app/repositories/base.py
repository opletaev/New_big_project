from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, TypeVar
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.database import async_session_maker

T = TypeVar("T", bound=BaseModel)

class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def get(self, id: int) -> T:
        ...
        
    @abstractmethod
    async def add(self, id: int) -> T:
        ...
        
    # @abstractmethod
    # async def delete(self, id: int): #-> bool:
    #     ...
        
    # @abstractmethod
    # async def update(self, id: int): #-> T:
    #     ...
    
class BaseRepository:
    model = None
    
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                await session.rollback()
                raise e
            return new_instance
        
    
    @classmethod
    async def add_all(cls, instance: List[Dict[str, Any]]):
        async with async_session_maker() as session:
            new_instance = [cls.model(**values) for values in instance]
            session.add_all(new_instance)
            try:
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                await session.rollback()
                raise e
            return new_instance
    
        
    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
    
        
    @classmethod    
    async def get_by_id(cls, instance_id: UUID | int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(cls.model.id == instance_id)
                )
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            return instance
        
    
    @classmethod
    async def delete_instance(cls, instance_id: UUID | int):
        async with async_session_maker() as session:
            query = (
                delete(cls.model)
                .where(cls.model.id == instance_id)
                )
            await session.execute(query)
            await session.commit()
