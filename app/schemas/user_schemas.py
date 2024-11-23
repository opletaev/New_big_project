import re
from typing import Optional
import uuid

from fastapi import HTTPException
from pydantic import (
    BaseModel, Field, field_validator,
)

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PHONE_MATCH_PATTERN = re.compile(r"^[0-9()+\-]+$")

class SShowUser(BaseModel):
    user_id: uuid.UUID
    surname: str
    name: str
    patronymic: str
    factory_employee_id: int
    division: str
    work_phone: str
    is_active: bool
    
    
class SCreateUser(BaseModel):
    factory_employee_id: int = Field(
        title="Табельный номер",
        )
    surname: str = Field(
        title="Фамилия",
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        )
    name: str = Field(
        title="Имя",
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        )
    patronymic: str = Field(
        title="Отчество",
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        )
    division: str = Field(
        title="Подразлеление",
        max_length=25,
        )
    work_phone: str = Field(
        title="Рабочий телефон",
        max_length=16,
        pattern=PHONE_MATCH_PATTERN,
        )
    password: str   
    
    
    @field_validator("name", "surname", "patronymic")
    @classmethod
    def titled_field(cls, value) -> str:
        return value.title()
    

class SDeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID
     
    
class SUpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID
    
    
class SUpdateUserRequest(BaseModel):
    work_phone: str = Field(
        title="Рабочий телефон",
        max_length=16,
        pattern=PHONE_MATCH_PATTERN,
        )
    division: str
        

class SToken(BaseModel):
    access_token: str
    token_type: str