from typing import Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.database import Base, async_session_maker

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, values: BaseModel) -> T:
        values_dict = values.model_dump(exclude_unset=True)
        print(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        async with async_session_maker() as session:
            new_instance = cls.model(**values_dict)  # type: ignore
            session.add(new_instance)
            try:
                await session.commit()
                print(f"Запись {cls.model.__name__} - Успешно добавлена")
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"Ошибка при добавлении записи {cls.model.__name__}: {e} ")
                raise e
            return new_instance

    @classmethod
    async def add_many(cls, values: list[BaseModel]) -> list[T]:
        values_list = [value.model_dump(exclude_unset=True) for value in values]
        print(
            f"Добавление нескольких записей {cls.model.__name__} с параметрами: {values_list}"
        )
        async with async_session_maker() as session:
            new_instances = [cls.model(**values) for values in values_list]  # type: ignore
            session.add_all(new_instances)
            try:
                await session.commit()
                print(
                    f"{len(new_instances)} записей {cls.model.__name__} - Успешно добавлены"
                )
            except SQLAlchemyError as e:
                await session.rollback()
                print(
                    f"Ошибка при добавлении нескольких записей {cls.model.__name__}: {e} "
                )
                raise e
            return new_instances

    @classmethod
    async def find_one_or_none_by_id(cls, instance_id: UUID | int) -> Optional[T]:
        print(f"Поиск одной записи {cls.model.__name__} с ID: {instance_id}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model).where(cls.model.id == instance_id)
                result = await session.execute(query)
                record = result.scalar_one_or_none()
                if record:
                    print(f"Запись {cls.model.__name__} c ID: {instance_id} - Найдена")
                else:
                    print(
                        f"Запись {cls.model.__name__} c ID: {instance_id} - Не найдена"
                    )
                return record
            except SQLAlchemyError as e:
                print(
                    f"Ошибка при поиске записи {cls.model.__name__} c ID: {instance_id}"
                )
                raise e

    @classmethod
    async def find_one_or_none_by_filter(cls, filters: BaseModel) -> T | None:
        filters_dict = filters.model_dump(exclude_unset=True)
        print(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filters_dict}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filters_dict)
                result = await session.execute(query)
                record = result.scalar_one_or_none()
                if record:
                    print(f"Запись найдена по фильтрам: {filters_dict}")
                else:
                    print(f"Запись не найдена по фильтрам: {filters_dict}")
                return record
            except SQLAlchemyError as e:
                print(
                    f"Ошибка при поиске записи {cls.model.__name__} по фильтрам: {filters_dict}"
                )
                raise e

    @classmethod
    async def find_all_by_filter(cls, filters: BaseModel) -> list[T] | None:
        filters_dict = filters.model_dump(exclude_unset=True)
        print(f"Поиск всех записей {cls.model.__name__} по фильтрам: {filters_dict}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filters_dict)
                result = await session.execute(query)
                records = result.scalars().all()
                print(f"Найдено {len(records)} записей")
                print(records)
                return records
            except SQLAlchemyError as e:
                print(f"Ошибка при поиске всех записей по фильтрам: {filters_dict}")
                raise e

    @classmethod
    async def find_all(cls) -> list[T] | None:
        print(f"Поиск всех записей {cls.model.__name__}")
        async with async_session_maker() as session:
            try:
                query = select(cls.model)  # type: ignore
                result = await session.execute(query)
                records = result.scalars().all()
                print(records)
                print(f"Найдено {len(records)} записей")
                return records
            except SQLAlchemyError as e:
                print(f"Ошибка при поиске всех записей {cls.model.__name__}")
                raise e

    @classmethod
    async def update_instance(
        cls,
        instance_id: UUID,
        values: BaseModel,
    ) -> None:
        values_dict = values.model_dump(exclude_none=True)
        print(
            f"""Обновление записи {cls.model.__name__} с ID: {instance_id}
            Параметры: {values_dict}"""
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
                print(f"Запись {cls.model.__name__} с ID: {instance_id} - Обновлена")
            except SQLAlchemyError as e:
                print(f"Ошибка при обновлении записи: {e}")
                await session.rollback()
                raise e

    @classmethod
    async def delete_by_id(cls, instance_id: UUID | int) -> None:
        print(f"Удаление записей {cls.model.__name__} по ID: {instance_id}")
        if not instance_id:
            print(f"Не указан ID записи для удаления")
            raise ValueError("Не указан ID записи для удаления")

        async with async_session_maker() as session:
            try:
                query = delete(cls.model).where(cls.model.id == instance_id)
                await session.execute(query)
                await session.commit()
                print(f"Запись {cls.model.__name__} с ID: {instance_id} - Удалена")
            except SQLAlchemyError as e:
                print(
                    f"Ошибка при удалении записи {cls.model.__name__} с ID: {instance_id}"
                )
                raise e

    @classmethod
    async def delete_all(cls) -> None:
        print(f"Удаление всех записей {cls.model.__name__}")
        async with async_session_maker() as session:
            try:
                query = delete(cls.model)
                await session.execute(query)
                await session.commit()
                print(f"Все записи {cls.model.__name__} - Удалены")
            except SQLAlchemyError as e:
                print(f"Ошибка при удалении всех запиcей {cls.model.__name__}")
                raise e
