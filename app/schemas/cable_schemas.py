from datetime import date
import re
from typing import Annotated, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.models.cable import CableStatusEnum


CHARS_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z0-9 \-]+$")


class AddCableDTO(BaseModel):
    index: Annotated[
        str,
        Field(
            title="Индекс",
            min_length=2,
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["00А000"],
        ),
    ]
    group: Annotated[
        str,
        Field(
            title="Группа",
            min_length=2,
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["0001"],
        ),
    ]
    assembly: Annotated[
        str,
        Field(
            title="Сборка",
            min_length=2,
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["0002"],
        ),
    ]
    factory_number: Annotated[
        str,
        Field(
            title="Зав.№",
            min_length=2,
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["Б003"],
        ),
    ]
    last_service: Annotated[
        date,
        Field(title="Дата проверки"),
    ]
    next_service: Annotated[
        date,
        Field(title="Дата след. проверки"),
    ]
    status: Annotated[
        CableStatusEnum,
        Field(
            title="Статус",
            min_length=2,
            pattern=CHARS_MATCH_PATTERN,
        ),
    ]

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class IssuedToDTO(BaseModel):
    factory_employee_id: int


class CableDTO(AddCableDTO):
    id: UUID
    issued_to: list[IssuedToDTO]

    @computed_field(title="Полная маркировка")
    def cable_name(self) -> str:
        return f"{self.index}.{self.group}.{self.assembly} {self.factory_number}"


class FindCableDTO(BaseModel):
    index: Annotated[
        Optional[str],
        Field(
            title="Индекс",
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["00А000"],
            default=None,
        ),
    ]
    group: Annotated[
        Optional[str],
        Field(
            title="Группа",
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["0001"],
            default=None,
        ),
    ]
    assembly: Annotated[
        Optional[str],
        Field(
            title="Сборка",
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["0002"],
            default=None,
        ),
    ]
    factory_number: Annotated[
        Optional[str],
        Field(
            title="Зав.№",
            max_length=10,
            pattern=CHARS_MATCH_PATTERN,
            examples=["Б003"],
            default=None,
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class UpdateCableDTO(BaseModel):
    last_service: Annotated[
        date,
        Field(title="Дата проверки"),
    ]
    next_service: Annotated[
        date,
        Field(title="Дата след. проверки"),
    ]
