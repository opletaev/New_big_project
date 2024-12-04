from datetime import date

from sqlalchemy import and_, extract, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models.cable import Cable
from app.repositories.base import BaseRepository
from app.logger import logger


class CableRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = Cable

    async def cables_to_service_in(self, date: date) -> list[Cable] | None:
        logger.info(
            f"Find {self.model.__name__} records where next_service <= {date.month}.{date.year}"
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
                    logger.info(f"{len(records)} {self.model.__name__} records - Found")
                else:
                    logger.info(
                        f"{self.model.__name__} records where next_service <= {date.month}.{date.year} - Not Found"
                    )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += f": Cannot find record where next_service <= {date.month}.{date.year}"
                extra = {
                    "model": self.model.__name__,
                    "date": date,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return records
