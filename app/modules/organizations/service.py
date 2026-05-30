import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.organizations.models import Organization
from app.modules.organizations.schemas import OrgCreate, OrgUpdate


def list_orgs(db: Session) -> list[Organization]:
    return db.query(Organization).order_by(Organization.name).all()


def get_org(db: Session, org_id: uuid.UUID) -> Organization | None:
    return db.get(Organization, org_id)


def create_org(db: Session, payload: OrgCreate) -> Organization:
    org = Organization(name=payload.name.strip())
    db.add(org)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Organization name already exists")
    db.refresh(org)
    return org


def update_org(db: Session, org: Organization, payload: OrgUpdate) -> Organization:
    org.name = payload.name.strip()
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Organization name already exists")
    db.refresh(org)
    return org


def delete_org(db: Session, org: Organization) -> None:
    db.delete(org)
    db.commit()
