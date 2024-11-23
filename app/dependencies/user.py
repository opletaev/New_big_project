from fastapi import Depends

from app.repositories.user import UserRepository
from app.usecases.user_usecase import UserUsecase


def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_usecase(repo: UserRepository = Depends(get_user_repository)) -> UserUsecase:
    return UserUsecase(repo)