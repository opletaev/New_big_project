from fastapi import FastAPI

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.users import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)