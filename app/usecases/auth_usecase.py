from datetime import UTC, datetime, timedelta
from urllib.request import Request
from uuid import UUID

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.repositories.user_repo import UserRepository
from app.schemas.auth_schemas import SAuthUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUsecase:
    
    async def login_user(self, body: SAuthUser):
    # Дописать, что возвращает функция
        print(body.factory_employee_id, type(body.factory_employee_id))
        user = await UserRepository().get_user_by_factory_employee_id(body.factory_employee_id)
        if not user or not verify_password(
            body.password,
            user.hashed_password,
            ):
            return None
        return user
    
    def get_token(request: Request):
        token = request.cookies.get("access_token")
        if not token:
            # Описать исключение
            raise HTTPException
        return token
    
    def get_user_id (token: str = Depends(get_token)):
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
    
    ##### Возможно, нужно вынести в другой файл #####
      
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM,
        )    
    return encoded_jwt
    
def get_hashed_password(password: str):
    return pwd_context.hash(password)
    
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
    