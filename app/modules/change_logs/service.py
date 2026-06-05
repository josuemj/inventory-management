import uuid

from sqlalchemy.orm import Session

from app.modules.change_logs.models import ChangeLog


def list_change_logs(db: Session, org_id: uuid.UUID, entity_id: uuid.UUID | None = None) -> list[ChangeLog]:
    q = db.query(ChangeLog).filter(ChangeLog.org_id == org_id)
    if entity_id:
        q = q.filter(ChangeLog.entity_id == entity_id)
    return q.order_by(ChangeLog.changed_at.desc()).all()


def record_change(
    db: Session,
    org_id: uuid.UUID,
    user_id: uuid.UUID,
    entity_type: str,
    entity_id: uuid.UUID,
    field: str,
    old_value: str | None,
    new_value: str | None,
) -> None:
    log = ChangeLog(
        org_id=org_id,
        user_id=user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        field=field,
        old_value=old_value,
        new_value=new_value,
    )
    db.add(log)
