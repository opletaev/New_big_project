from fastapi import Depends

from app.repositories.user import UserRepository
from app.usecases.auth_usecase import AuthUsecase


def get_user_repository() -> UserRepository:
    return UserRepository()

def get_auth_usecase(repo: UserRepository = Depends(get_user_repository)) -> AuthUsecase:
    return AuthUsecase(repo)