import re
from typing import Optional
import uuid

from fastapi import HTTPException
from pydantic import (
    BaseModel, 
    ValidationInfo, 
    field_validator, 
    constr
    )

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
  

class SShowUser(BaseModel):
    user_id: uuid.UUID
    factory_employee_id: int
    work_phone: str
    name: str
    surname: str
    patronymic: str
    division: str
    is_active: bool
    
    
class SCreateUser(BaseModel):
    factory_employee_id: int
    work_phone: str
    password: str
    name: str
    surname: str
    patronymic: str
    division: str    
    
    
    @field_validator("name", "surname", "patronymic")
    @classmethod
    def validate_name(cls, value, info: ValidationInfo) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail=f"{info.field_name} should contains only letters"
            )
        return value


class SDeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID
     
    
class SUpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID
    
    
class SUpdateUserRequest(BaseModel):
    work_phone: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    division: Optional[str]
    
    @field_validator("name", "surname", "patronymic")
    @classmethod
    def validate_name(cls, value, info: ValidationInfo) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail=f"{info.field_name} should contains only letters"
            )
        return value
    

class SToken(BaseModel):
    access_token: str
    token_type: str