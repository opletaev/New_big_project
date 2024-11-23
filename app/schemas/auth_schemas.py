from pydantic import BaseModel, Field


class SAuthUser(BaseModel):
    factory_employee_id: int = Field(
        title="Табельный номер",
        )
    password: str
    