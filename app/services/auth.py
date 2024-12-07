from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import Request, Response
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.exceptions.auth import (
    IncorrectTokenFormatException,
    TokenExpiredException,
    TokenIsNotPresentException,
)


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_token(cls, request: Request) -> UUID:
        token = request.cookies.get("access_token")
        if not token:
            raise TokenIsNotPresentException
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
        return user_id

    @classmethod
    def create_access_token(cls, data: dict) -> str:
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

    @classmethod
    async def logout_user(cls, response: Response) -> None:
        response.delete_cookie("access_token")

    @classmethod
    def hashed_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)
