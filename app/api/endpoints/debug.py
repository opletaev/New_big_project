from fastapi import APIRouter

from app.service.debug_service import DebugUserService


router = APIRouter(
    prefix="/debug",
    tags=["Отладка"],
)


@router.post("/create_test_users")
async def create_test_users():
    return await DebugUserService().create_users_from_dicts()


@router.delete("/delete_all_users")
async def delete_all_users():
    return await DebugUserService().delete_all_users()
