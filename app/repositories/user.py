from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = User
