from pydantic import BaseModel


class SAuthUser(BaseModel):
    factory_employee_id: int
    password: str
    