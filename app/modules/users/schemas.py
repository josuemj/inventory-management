from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.users.models import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    role: UserRole
    company_id: int | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int | None
    full_name: str
    username: str
    role: UserRole
    created_at: datetime
