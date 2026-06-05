import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_root
from app.db.session import get_db
from app.modules.change_logs.schemas import ChangeLogRead
from app.modules.change_logs.service import list_change_logs
from app.modules.users.models import User

router = APIRouter(prefix="/change-logs", tags=["change-logs"])


@router.get("", response_model=list[ChangeLogRead])
def get_change_logs(
    entity_id: uuid.UUID | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_root),
):
    org_id = current_user.org_id
    if current_user.role == "root":
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Root must filter by org via query param")
    return list_change_logs(db, org_id, entity_id)
