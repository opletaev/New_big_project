from fastapi import APIRouter

from app.service.debug import DebugUserService
from app.tasks.tasks import pg_backup


router = APIRouter(
    prefix="/debug",
    tags=["Отладка"],
)


@router.post("/create_test_users", name="Создать тестовых пользователей (5)")
async def create_test_users():
    return await DebugUserService().create_users_from_dicts()


@router.delete("/delete_all_users", name="Удалить всех пользователей")
async def delete_all_users():
    return await DebugUserService().delete_all_users()


@router.get("/pg_backup_test", summary="Тестовый бэкап БД через Celery")
def pg_backup_test() -> bool:
    pg_backup.delay()
    return True
