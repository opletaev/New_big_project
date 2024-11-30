import re
from typing import Annotated, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.models.profile import DivisionEnum
from app.models.user import UserRoleEnun


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PHONE_MATCH_PATTERN = re.compile(r"^[0-9()+\-]+$")


class UserDTO(BaseModel):
    factory_employee_id: Annotated[
        int,
        Field(
            title="Табельный номер",
            examples=["12345"],
        ),
    ]
    role: Annotated[
        UserRoleEnun,
        Field(
            default="Пользователь",
        ),
    ]
    is_active: Annotated[
        bool,
        Field(
            default=True,
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class RegisterUserDTO(UserDTO):
    password: Annotated[
        str,
        Field(
            title="Пароль",
            min_length=8,
            examples=["Super-Secret-Password"],
        ),
    ]


class CreateUserDTO(UserDTO):
    hashed_password: str


class UserDataDTO(BaseModel):
    surname: Annotated[
        str,
        Field(
            title="Фамилия",
            min_length=2,
            max_length=25,
            pattern=LETTER_MATCH_PATTERN,
            examples=["Пупкин"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            title="Имя",
            min_length=3,
            max_length=25,
            pattern=LETTER_MATCH_PATTERN,
            examples=["Васян"],
        ),
    ]
    patronymic: Annotated[
        str,
        Field(
            title="Отчество",
            min_length=5,
            max_length=25,
            pattern=LETTER_MATCH_PATTERN,
            examples=["Инакентич"],
        ),
    ]
    division: DivisionEnum
    phone_number: Annotated[
        str,
        Field(
            title="Рабочий телефон",
            min_length=5,
            max_length=16,
            pattern=PHONE_MATCH_PATTERN,
            examples=["8(800)555-35-35", "04-51"],
        ),
    ]

    @field_validator("name", "surname", "patronymic")
    @classmethod
    def titled_field(cls, value) -> str:
        return value.title()


class AllUserDataDTO(CreateUserDTO):
    profile: UserDataDTO

    model_config = ConfigDict(from_attributes=True)


class UpdatedUserResponseDTO(BaseModel):
    updated_user_id: UUID


class UpdateUserProfileRequestDTO(BaseModel):
    phone_number: Annotated[
        Optional[str],
        Field(
            title="Рабочий телефон",
            min_length=5,
            max_length=16,
            pattern=PHONE_MATCH_PATTERN,
            examples=["8(800)555-35-35", "04-51"],
            default=None,
        ),
    ]
    division: Annotated[
        Optional[DivisionEnum],
        Field(
            default=None,
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class UpdateUserPasswordRequestDTO(BaseModel):
    password: Annotated[
        Optional[str],
        Field(
            title="Пароль",
            min_length=8,
            examples=["Super-Secret-Password"],
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class DeleteUserResponseDTO(BaseModel):
    deleted_user_id: UUID
