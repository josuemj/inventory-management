import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrgCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class OrgUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class OrgRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    created_at: datetime
