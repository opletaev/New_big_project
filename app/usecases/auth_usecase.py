from datetime import UTC, datetime
from uuid import UUID

from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from app.core.config import settings
from app.repositories.user import UserRepository
from app.schemas.auth_schemas import SAuthUser
from app.usecases.user_usecase import UserUsecase
from app.utils import get_token, verify_password


class AuthUsecase:
    def __init__(self, user_usecase: UserUsecase):
        self.user_usecase = user_usecase
    
    async def check_user(
        self, 
        body: SAuthUser,
        ) -> UUID:
        user = await self.user_usecase.get_user_info_by_factory_employee_id(
            factory_employee_id=body.factory_employee_id,
            )
        if not user or not verify_password(
            body.password,
            user.hashed_password,
            ):
            # Описать исключение
            raise HTTPException
        return user.id
    
    
    def get_user_id (token: str = Depends(get_token)) -> UUID:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, settings.ALGORITHM
            )
        except JWTError as jwt_error:
            print(f"JWT error: {jwt_error}")
            # Описать исключение
            raise HTTPException
        
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < datetime.now(UTC).toordinal()):
            # Описать исключение
            raise HTTPException

        user_id: UUID = payload.get("sub")
        if not user_id:
            # Описать исключение
            raise HTTPException
        return user_id
    