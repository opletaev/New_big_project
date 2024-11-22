from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    
    @property
    def DATABASE_URL(self):
        return f"""postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"""
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = ConfigDict(env_file='.env')
        
settings = Settings()