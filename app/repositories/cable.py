from datetime import date

from sqlalchemy import and_, extract, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models.cable import Cable
from app.repositories.base import BaseRepository
from app.core.logger import repository_log as logger


class CableRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = Cable

    async def cables_to_service_in(self, date: date) -> list[Cable] | None:
        logger.info(
            f"Find records where next_service <= {date.month}.{date.year}",
            extra={
                "model": self.model.__name__,
                "date": date,
            },
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
                records = result.unique().scalars().all()
                if records:
                    logger.info(
                        "Records - Found",
                        extra={
                            "model": self.model.__name__,
                            "count": len(records),
                        },
                    )
                else:
                    logger.info(
                        f"Records where next_service <= {date.month}.{date.year} - Not Found",
                        extra={
                            "model": self.model.__name__,
                            "dete": date,
                        },
                    )
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = "Database Exc"
                else:
                    msg = "Unknown Exc"
                msg += f": Cannot find records where next_service <= {date.month}.{date.year}"
                extra = {
                    "model": self.model.__name__,
                    "date": date,
                }
                logger.error(msg, extra=extra, exc_info=True)
                raise e
            return records
