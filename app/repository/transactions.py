from app.models.transaction import Transaction
from app.repository.base import BaseRepository


class TransactionRepository(BaseRepository):
    model = Transaction
