from pydantic import BaseModel, Field


class SAuthUser(BaseModel):
    factory_employee_id: int = Field(
        title="Табельный номер",
        )
    password: str
    
    
class SToken(BaseModel):
    access_token: str
    token_type: str