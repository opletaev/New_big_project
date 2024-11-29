from typing import Annotated
from pydantic import BaseModel, Field


class SAuth(BaseModel):
    factory_employee_id: Annotated[int, Field(
        title="Табельный номер",
    )]
    password: str


class SToken(BaseModel):
    access_token: str
    token_type: str
