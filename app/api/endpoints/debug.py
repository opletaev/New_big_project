from fastapi import APIRouter

from app.repositories.debug import create_users_from_dicts, delete_users


router = APIRouter(
    prefix="/debug",
    tags=["Отладка"],
)

@router.post("/create_test_users")
async def create_test_users():
    return await create_users_from_dicts()


@router.delete("/delete_all_users")
async def delete_all_users():
    return await delete_users()