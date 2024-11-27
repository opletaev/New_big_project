from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.exceptions.auth import (
    IncorrectTokenFormatException,
    TokenExpiredException,
    TokenIsNotPresentException,
)
from app.service.user_service import UserService


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_token_from_cookie(self, request: Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            raise TokenIsNotPresentException
        return token

    def verify_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                settings.ALGORITHM,
            )
        except JWTError as jwt_error:
            print(f"JWT error: {jwt_error}")
            raise IncorrectTokenFormatException

        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < datetime.now(UTC).toordinal()):
            raise TokenExpiredException

        user_id: UUID = payload.get("sub")
        if not user_id:
            raise TokenIsNotPresentException
        return user_id  # Для отладки. Потом bool

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire.timestamp()})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
        return encoded_jwt  #  Для отладки. Потом True

    def hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
