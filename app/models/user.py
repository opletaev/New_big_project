import uuid
from sqlalchemy import (
    UUID, Column, DateTime, String, Boolean, Integer
    )
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4().hex)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    factory_employee_id = Column(Integer, nullable=False, unique=True)
    division = Column(String, nullable=False)
    work_phone = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
    role = Column(String, nullable=False)
    