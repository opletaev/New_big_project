from app.models.user import User
from app.repository.base import BaseRepository


class UserRepository(BaseRepository):  # (AbstractRepository[SUser]):
    model = User
