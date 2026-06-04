import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProviderCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    tel: str | None = Field(default=None, max_length=30)


class ProviderUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    tel: str | None = Field(default=None, max_length=30)


class ProviderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    tel: str | None
    created_at: datetime
