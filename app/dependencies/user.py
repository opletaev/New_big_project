from fastapi import Depends

from app.repositories.profile import ProfileRepository
from app.repositories.user import UserRepository
from app.service.auth_service import AuthService
from app.service.profile_service import ProfileService
from app.service.user_service import UserService


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return AuthService(user_repository)


def get_profile_repository() -> ProfileRepository:
    return ProfileRepository()


def get_profile_service(
    profile_repository: ProfileRepository = Depends(get_profile_repository),
) -> UserService:
    return ProfileService(profile_repository)
