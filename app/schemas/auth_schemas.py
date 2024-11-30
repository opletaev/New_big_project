from typing import Annotated
from pydantic import BaseModel, Field


class AuthDTO(BaseModel):
    factory_employee_id: Annotated[
        int,
        Field(
            title="Табельный номер",
        ),
    ]
    password: str


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
