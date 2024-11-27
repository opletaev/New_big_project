from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.database import Base, async_session_maker

T = TypeVar("T", bound=Base)


class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def get(self, id: int) -> T: ...

    @abstractmethod
    async def add(self, id: int) -> T: ...

    # @abstractmethod
    # async def delete(self, id: int): #-> bool:
    #     ...

    # @abstractmethod
    # async def update(self, id: int): #-> T:
    #     ...


class BaseRepository(Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, values: BaseModel) -> T:
        value_dict = values.model_dump(exclude_unset=True)

        async with async_session_maker() as session:
            new_instance = cls.model(**value_dict)  # type: ignore
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                print(e)
                await session.rollback()
                raise e
            return new_instance

    @classmethod
    async def add_all(cls, instances: list[BaseModel]) -> list[T]:
        values_list = [item.model_dump(exclude_unset=True) for item in instances]

        async with async_session_maker() as session:
            new_instances = [cls.model(**values) for values in values_list]  # type: ignore
            session.add_all(new_instances)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                print(e)
                await session.rollback()
                raise e
            return new_instances

    @classmethod
    async def find_one_or_none_by_id(cls, instance_id: UUID | int) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model).where(  # type: ignore
                cls.model.id == instance_id
            )  # type: ignore
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            return instance

    @classmethod
    async def find_one_or_none_by_filter(cls, filter: BaseModel) -> T | None:
        filter_dict = filter.model_dump(exclude_unset=True)

        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result

    @classmethod
    async def find_all(cls) -> list[T] | None:
        async with async_session_maker() as session:
            query = select(cls.model)  # type: ignore
            result = await session.execute(query)
            records = result.scalars().all()
            return records

    @classmethod
    async def find_all_by_filter(cls, filter: dict[str, Any]) -> list[T]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            result = result.scalars().all()
            return result

    @classmethod
    async def delete_by_id(cls, instance_id: UUID | int) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).where(  # type: ignore
                cls.model.id == instance_id
            )  # type: ignore
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_all(cls):
        async with async_session_maker() as session:
            query = delete(cls.model)
            await session.execute(query)
            await session.commit()
