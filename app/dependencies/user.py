from fastapi import Depends

from app.repositories.user import UserRepository
from app.service.user_service import UserService


def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)