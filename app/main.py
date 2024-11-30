from fastapi import FastAPI

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.cables import router as cable_router
from app.api.endpoints.users import router as user_router
from app.api.endpoints.debug import router as debug_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(cable_router)
app.include_router(debug_router)
