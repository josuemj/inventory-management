import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MovementCreate(BaseModel):
    item_id: uuid.UUID
    movement_type: str = Field(pattern="^(add|sale|dispatch|adjustment)$")
    quantity: int = Field(gt=0)
    note: str | None = None


class MovementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    item_id: uuid.UUID
    user_id: uuid.UUID
    movement_type: str
    quantity: int
    note: str | None
    created_at: datetime
