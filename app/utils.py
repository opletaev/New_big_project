from datetime import UTC, datetime, timedelta
from fastapi import HTTPException, Request
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_token(request: Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            # Описать исключение
            raise HTTPException(
                status_code=401, detail="Access token is missing."
            )
        return token


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
    
    
def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)
    
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)