from app.models.cable import Cable
from app.repositories.base import BaseRepository


class CableRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = Cable
