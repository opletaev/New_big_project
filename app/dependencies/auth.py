from fastapi import Depends

from app.repositories.user import UserRepository
from app.usecases.auth_usecase import AuthUsecase
from app.usecases.user_usecase import UserUsecase

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_usecase(user_repository: UserRepository = Depends(get_user_repository)) -> UserUsecase:
    return UserUsecase(user_repository)

def get_auth_usecase(user_usecase: UserUsecase = Depends(get_user_usecase)) -> AuthUsecase:
    return AuthUsecase(user_usecase)