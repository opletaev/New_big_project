import re
from typing import Annotated, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.models.user import DivisionEnum, UserRoleEnun


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PHONE_MATCH_PATTERN = re.compile(r"^[0-9()+\-]+$")


class SUserAuthData(BaseModel):
    factory_employee_id: int
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class SCreateUser(BaseModel):
    factory_employee_id: Annotated[int, Field(
        title="Табельный номер",
        examples=["12345"],
    )]
    password: Annotated[str, Field(
        title="Пароль",
        min_length=8,
        examples=["Super-Secret-Password"],
    )]


class SUserData(BaseModel):
    surname: Annotated[str, Field(
        title="Фамилия",
        min_length=2,
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        examples=["Пупкин"],
    )]
    name: Annotated[str, Field(
        title="Имя",
        min_length=3,
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        examples=["Васян"],
    )]
    patronymic: Annotated[str, Field(
        title="Отчество",
        min_length=5,
        max_length=25,
        pattern=LETTER_MATCH_PATTERN,
        examples=["Инакентич"],
    )]
    division: DivisionEnum
    phone_number: Annotated[str, Field(
        title="Рабочий телефон",
        min_length=5,
        max_length=16,
        pattern=PHONE_MATCH_PATTERN,
        examples=["8(800)555-35-35", "04-51"],
    )]
    is_active: Annotated[bool, Field(
        default=True,
    )]
    role: Annotated[UserRoleEnun, Field(
        default="Пользователь",
    )]

    @field_validator("name", "surname", "patronymic")
    @classmethod
    def titled_field(cls, value) -> str:
        return value.title()


class SAllUserData(BaseModel):
    factory_employee_id: int
    hashed_password: str
    profile: SUserData

    model_config = ConfigDict(from_attributes=True)


class SUpdatedUserResponse(BaseModel):
    updated_user_id: UUID


class SUpdateUserProfileRequest(BaseModel):
    phone_number: Annotated[Optional[str], Field(
        title="Рабочий телефон",
        min_length=5,
        max_length=16,
        pattern=PHONE_MATCH_PATTERN,
        examples=["8(800)555-35-35", "04-51"],
        default=None,
    )]
    division: Annotated[Optional[DivisionEnum], Field(
        default=None,
    )]

    model_config = ConfigDict(from_attributes=True)


class SUpdateUserPasswordRequest(BaseModel):
    password: Annotated[Optional[str], Field(
        title="Пароль",
        min_length=8,
        examples=["Super-Secret-Password"],
    )]

    model_config = ConfigDict(from_attributes=True)


class SDeleteUserResponse(BaseModel):
    deleted_user_id: UUID
