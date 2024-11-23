import re
import uuid

from pydantic import (
    BaseModel, ConfigDict, Field, field_validator,
)

from app.models.user import DivisionEnum


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PHONE_MATCH_PATTERN = re.compile(r"^[0-9()+\-]+$")

class SShowUser(BaseModel):
    user_id: uuid.UUID
    surname: str
    name: str
    patronymic: str
    factory_employee_id: int
    division: str
    phone_number: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    
class SCreateUser(BaseModel):
    factory_employee_id: int = Field(
        title="Табельный номер",
        examples=["12345"]
        )
    password: str = Field(
        title="Пароль",
        examples=["Super-Secret-Password"]
        )
    surname: str = Field(
        title="Фамилия",
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        examples=["Пупкин"],
        )
    name: str = Field(
        title="Имя",
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        examples=["Васян"],
        )
    patronymic: str = Field(
        title="Отчество",
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        examples=["Инакентич"],
        )
    division: DivisionEnum
    phone_number: str = Field(
        title="Рабочий телефон",
        max_length=16,
        pattern=PHONE_MATCH_PATTERN,
        examples=["8(800)555-35-35"],
        )
    
    
    @field_validator("name", "surname", "patronymic")
    @classmethod
    def titled_field(cls, value) -> str:
        return value.title()
    

class SDeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID
     
    
class SUpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID
    
    
class SUpdateUserRequest(BaseModel):
    password: str = Field(
        title="Пароль",
        examples=["New-Super-Secret-Password"]
        )
    phone_number: str = Field(
        title="Рабочий телефон",
        max_length=16,
        pattern=PHONE_MATCH_PATTERN,
        examples=["8(800)555-35-35"],
        )
    division: DivisionEnum
        