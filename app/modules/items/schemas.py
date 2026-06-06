import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    price: Decimal = Field(ge=0, decimal_places=2)
    stock: int = Field(ge=0, default=0)
    category_id: uuid.UUID | None = None
    provider_id: uuid.UUID | None = None
    image_url: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    price: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    category_id: uuid.UUID | None = None
    provider_id: uuid.UUID | None = None
    image_url: str | None = None


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    org_id: uuid.UUID
    category_id: uuid.UUID | None
    provider_id: uuid.UUID | None
    image_url: str | None
    name: str
    price: Decimal
    stock: int
    created_at: datetime
