from fastapi import APIRouter

from app.repositories.debug import create_users_from_dicts


router = APIRouter(
    prefix="/debug",
    tags=["Отладка"],
)

@router.post("/create_test_users")
async def create_test_users():
    return await create_users_from_dicts()