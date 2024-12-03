from datetime import date

from sqlalchemy import and_, extract, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models.cable import Cable
from app.repositories.base import BaseRepository


class CableRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = Cable

    async def cables_to_service_in(self, date: date) -> list[Cable] | None:
        print(
            f"Поиск записей {self.model.__name__}, где next_service <= {date.month}.{date.year}"
        )
        async with async_session_maker() as session:
            try:
                query = select(Cable).where(
                    and_(
                        extract("MONTH", Cable.next_service) <= date.month,
                        extract("YEAR", Cable.next_service) <= date.year,
                    ),
                )
                result = await session.execute(query)
                records = result.scalars().all()
                if records:
                    print(
                        f"Записи {self.model.__name__}, где next_service <= {date.month}.{date.year} - Найдены"
                    )
                else:
                    print(
                        f"Записи {self.model.__name__}, где next_service <= {date.month}.{date.year} - Не найдены"
                    )
            except SQLAlchemyError as e:
                print(
                    f"Ошибка при поиске записи {self.model.__name__}, где next_service <= {date.month}.{date.year}"
                )
                raise e
            return records
