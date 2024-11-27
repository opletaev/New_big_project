from fastapi import Depends

from app.repositories.user import UserRepository
from app.service.auth_service import AuthService
from app.service.user_service import UserService


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
    user_usecase: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_usecase)
