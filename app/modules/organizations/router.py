import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_root
from app.db.session import get_db
from app.modules.organizations.schemas import OrgCreate, OrgRead, OrgUpdate
from app.modules.organizations.service import (
    create_org, delete_org, get_org, list_orgs, update_org,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


def _get_or_404(db: Session, org_id: uuid.UUID):
    org = get_org(db, org_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org


@router.get("", response_model=list[OrgRead])
def get_organizations(db: Session = Depends(get_db), _=Depends(require_root)):
    return list_orgs(db)


@router.post("", response_model=OrgRead, status_code=status.HTTP_201_CREATED)
def post_organization(payload: OrgCreate, db: Session = Depends(get_db), _=Depends(require_root)):
    try:
        return create_org(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{org_id}", response_model=OrgRead)
def get_organization(org_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_root)):
    return _get_or_404(db, org_id)


@router.put("/{org_id}", response_model=OrgRead)
def put_organization(org_id: uuid.UUID, payload: OrgUpdate, db: Session = Depends(get_db), _=Depends(require_root)):
    org = _get_or_404(db, org_id)
    try:
        return update_org(db, org, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(org_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_root)):
    org = _get_or_404(db, org_id)
    delete_org(db, org)
