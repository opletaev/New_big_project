from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.database import Base, async_session_maker
from app.core.logger import repository_log as logger


T = TypeVar("T", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def add():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id():
        raise NotImplementedError


class BaseRepository(AbstractRepository, Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, values: BaseModel) -> T:
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(
            "Add a record",
            extra={
                "model": {cls.model.__name__},
                "values": values_dict,
            },
        )
        async with async_session_maker() as session:
            new_instance = cls.model(**values_dict)  # type: ignore
            session.add(new_instance)
            try:
                await session.commit()
                logger.info(
                    "Record - Added",
                    extra={
                        "model": {cls.model.__name__},
                        "values": values_dict,
                    },
                )
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot add a record"
                extra = {
                    "model": cls.model.__name__,
                    "values": values_dict,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return new_instance

    @classmethod
    async def add_many(cls, values: list[BaseModel]) -> list[T]:
        values_list = [value.model_dump(exclude_unset=True) for value in values]
        logger.info(
            "Add many records",
            extra={
                "model": {cls.model.__name__},
                "values": values_list,
            },
        )
        async with async_session_maker() as session:
            new_instances = [cls.model(**values) for values in values_list]  # type: ignore
            session.add_all(new_instances)
            try:
                await session.commit()
                logger.info(
                    "Records - Added",
                    extra={
                        "model": {cls.model.__name__},
                        "count": len(new_instances),
                    },
                )
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot add a record"
                extra = {
                    "model": cls.model.__name__,
                    "values": values,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return new_instances

    @classmethod
    async def find_one_or_none_by_filter(cls, filters: BaseModel) -> T | None:
        filters_dict = filters.model_dump(exclude_unset=True)
        logger.info(
            "Find a record by filter",
            extra={
                "model": {cls.model.__name__},
                "filter": filters,
            },
        )
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filters_dict)
                result = await session.execute(query)
                record = result.unique().scalar_one_or_none()
                if record:
                    logger.info(
                        "A record - Found",
                        extra={
                            "model": {cls.model.__name__},
                            "filter": filters_dict,
                        },
                    )
                else:
                    logger.info(
                        "A record - Not Found",
                        extra={
                            "model": {cls.model.__name__},
                            "filter": filters_dict,
                        },
                    )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot find a record by filter"
                extra = {
                    "model": cls.model.__name__,
                    "filter": filters_dict,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return record

    @classmethod
    async def find_all_by_filter(cls, filters: BaseModel) -> list[T] | None:
        filters_dict = filters.model_dump(exclude_unset=True)
        logger.info(
            "Find all records by filter",
            extra={
                "model": cls.model.__name__,
                "filter": filters_dict,
            },
        )
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filters_dict)
                result = await session.execute(query)
                records = result.unique().scalars().all()
                logger.info(
                    "Records - Found",
                    extra={
                        "model": cls.model.__name__,
                        "filter": filters_dict,
                        "count": len(records),
                    },
                )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot find records"
                extra = {
                    "model": cls.model.__name__,
                    "filter": filters_dict,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return records

    @classmethod
    async def find_all(cls) -> list[T] | None:
        logger.info(
            "Find all records",
            extra={"model": cls.model.__name__},
        )
        async with async_session_maker() as session:
            try:
                query = select(cls.model)  # type: ignore
                result = await session.execute(query)
                records = result.unique().scalars().all()
                logger.info(
                    "Records - Found",
                    extra={
                        "model": cls.model.__name__,
                        "count": len(records),
                    },
                )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot find records"
                extra = {"model": cls.model.__name__}
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return records

    @classmethod
    async def update_instance(
        cls,
        instance_id: UUID,
        values: BaseModel,
    ) -> bool:
        values_dict = values.model_dump(exclude_none=True)
        logger.info(
            "Update a record by id",
            extra={
                "model": cls.model.__name__,
                "id": instance_id,
                "values": values_dict,
            },
        )
        async with async_session_maker() as session:
            try:
                query = (
                    update(cls.model)
                    .where(cls.model.id == instance_id)
                    .values(**values_dict)
                )
                await session.execute(query)
                await session.commit()
                logger.info(
                    "A record - Uppdated",
                    extra={
                        "model": cls.model.__name__,
                        "id": instance_id,
                        "values": values_dict,
                    },
                )
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot update a record"
                extra = {
                    "model": cls.model.__name__,
                    "id": instance_id,
                    "values": values_dict,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return True

    @classmethod
    async def delete_by_id(cls, instance_id: UUID | int) -> bool:
        logger.info(
            "Delete a record by id",
            extra={
                "model": cls.model.__name__,
                "id": instance_id,
            },
        )
        if not instance_id:
            logger.error(
                "A record id is not specified",
                extra={
                    "model": cls.model.__name__,
                    "id": instance_id,
                },
                exc_info=True,
            )
            raise ValueError("Не указан ID записи для удаления")

        async with async_session_maker() as session:
            try:
                query = delete(cls.model).where(cls.model.id == instance_id)
                await session.execute(query)
                await session.commit()
                logger.info(
                    "Record - Deleted",
                    extra={
                        "model": cls.model.__name__,
                        "id": instance_id,
                    },
                    exc_info=True,
                )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot delete record by id"
                extra = {
                    "model": cls.model.__name__,
                    "id": instance_id,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return True

    @classmethod
    async def delete_all(cls) -> bool:
        logger.info(f"Delete all records {cls.model.__name__}")
        async with async_session_maker() as session:
            try:
                query = delete(cls.model)
                await session.execute(query)
                await session.commit()
                logger.info(
                    "All records - Deleted",
                    extra={"model": cls.model.__name__},
                )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot delete records"
                extra = {
                    "model": cls.model.__name__,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return True
