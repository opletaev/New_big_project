from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.dependencies import debug_user_service, user_service
from app.services.debug import DebugUserService
from app.services.user import UserService
from app.tasks.tasks import pg_backup


router = APIRouter(
    prefix="/debug",
    tags=["Отладка"],
)


@router.post("/create_test_users", name="Создать тестовых пользователей (5)")
async def create_test_users(
    user_service: Annotated[UserService, Depends(user_service)],
    debug_user_service: Annotated[DebugUserService, Depends(debug_user_service)],
):
    await debug_user_service.create_users_from_dicts()
    return await user_service.get_all_users()


@router.delete("/delete_all_users", name="Удалить всех пользователей")
async def delete_all_users(
    debug_user_service: Annotated[DebugUserService, Depends(debug_user_service)],
):
    return await debug_user_service.delete_all_users()


@router.get("/pg_backup_test", summary="Тестовый бэкап БД через Celery")
def pg_backup_test() -> bool:
    pg_backup.delay()
    return True
