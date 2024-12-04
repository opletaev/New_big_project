from typing import Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.database import Base, async_session_maker
from app.logger import logger

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, values: BaseModel) -> T:
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Add a {cls.model.__name__} record with values: {values_dict}")
        async with async_session_maker() as session:
            new_instance = cls.model(**values_dict)  # type: ignore
            session.add(new_instance)
            try:
                await session.commit()
                logger.info(f"{cls.model.__name__} record - Added")
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot add record"
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
        logger.info(f"Add many {cls.model.__name__} records with values: {values_list}")
        async with async_session_maker() as session:
            new_instances = [cls.model(**values) for values in values_list]  # type: ignore
            session.add_all(new_instances)
            try:
                await session.commit()
                logger.info(
                    f"{len(new_instances)} {cls.model.__name__} records - Added"
                )
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot add record"
                extra = {
                    "model": cls.model.__name__,
                    "values": values,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return new_instances

    @classmethod
    async def find_one_or_none_by_id(cls, instance_id: UUID | int) -> Optional[T]:
        logger.info(f"Find a {cls.model.__name__} record with ID: {instance_id}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model).where(cls.model.id == instance_id)
                result = await session.execute(query)
                record = result.unique().scalar_one_or_none()
                if record:
                    logger.info(
                        f"A{cls.model.__name__} record with ID: {instance_id} - Found"
                    )
                else:
                    logger.info(
                        f"A {cls.model.__name__} record with ID: {instance_id} - Not Found"
                    )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot find record"
                extra = {
                    "model": cls.model.__name__,
                    "id": instance_id,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return record

    @classmethod
    async def find_one_or_none_by_filter(cls, filters: BaseModel) -> T | None:
        filters_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Find a {cls.model.__name__} record with filter: {filters_dict}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filters_dict)
                result = await session.execute(query)
                record = result.unique().scalar_one_or_none()
                if record:
                    logger.info(
                        f"A {cls.model.__name__} record with filter: {filters_dict} - Found"
                    )
                else:
                    logger.info(
                        f"A {cls.model.__name__} record with filter: {filters_dict} - Not Found"
                    )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot find record"
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
            f"Search records to model: {cls.model.__name__} with filter: {filters_dict}"
        )
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filters_dict)
                result = await session.execute(query)
                records = result.unique().scalars().all()
                logger.info(f"{len(records)} {cls.model.__name__} records - Found")
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
        logger.info(f"Search all records to model: {cls.model.__name__}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model)  # type: ignore
                result = await session.execute(query)
                records = result.unique().scalars().all()
                logger.info(f"{len(records)} {cls.model.__name__} records - Found")
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
            f"Update {cls.model.__name__} record with ID: {instance_id}\nValues:{values_dict}"
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
                    f"{cls.model.__name__} record with ID: {instance_id} - Uppdated"
                )
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot update record"
                extra = {
                    "model": cls.model.__name__,
                    "values": values_dict,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return True

    @classmethod
    async def delete_by_id(cls, instance_id: UUID | int) -> bool:
        logger.info(f"Delete {cls.model.__name__} record with ID: {instance_id}")
        if not instance_id:
            logger.error(
                f"{cls.model.__name__} record ID is not specified", exc_info=True
            )
            raise ValueError("Не указан ID записи для удаления")

        async with async_session_maker() as session:
            try:
                query = delete(cls.model).where(cls.model.id == instance_id)
                await session.execute(query)
                await session.commit()
                logger.info(
                    f"{cls.model.__name__} record with ID: {instance_id} - Deleted"
                )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += ": Cannot delete record"
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
                logger.info(f"All records {cls.model.__name__} - Deleted")
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
