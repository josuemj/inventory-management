import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChangeLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    org_id: uuid.UUID
    user_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    field: str
    old_value: str | None
    new_value: str | None
    changed_at: datetime
