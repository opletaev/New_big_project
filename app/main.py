from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from redis import asyncio as aioredis

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.cables import router as cable_router
from app.api.endpoints.users import router as user_router
from app.api.endpoints.debug import router as debug_router
from app.api.endpoints.transactions import router as transaction_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(cable_router)
app.include_router(transaction_router)
app.include_router(debug_router)
