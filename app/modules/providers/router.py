import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_root, require_authenticated
from app.db.session import get_db
from app.modules.providers.models import Provider
from app.modules.providers.schemas import ProviderCreate, ProviderRead, ProviderUpdate
from app.modules.providers.service import (
    create_provider, delete_provider, get_provider, list_providers, update_provider,
)

router = APIRouter(prefix="/providers", tags=["providers"])


def _get_or_404(db: Session, provider_id: uuid.UUID) -> Provider:
    p = get_provider(db, provider_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return p


@router.get("", response_model=list[ProviderRead])
def get_providers(db: Session = Depends(get_db), _=Depends(require_authenticated)):
    return list_providers(db)


@router.post("", response_model=ProviderRead, status_code=status.HTTP_201_CREATED)
def post_provider(payload: ProviderCreate, db: Session = Depends(get_db), _=Depends(require_admin_or_root)):
    return create_provider(db, payload)


@router.get("/{provider_id}", response_model=ProviderRead)
def get_provider_by_id(provider_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_authenticated)):
    return _get_or_404(db, provider_id)


@router.put("/{provider_id}", response_model=ProviderRead)
def put_provider(provider_id: uuid.UUID, payload: ProviderUpdate, db: Session = Depends(get_db), _=Depends(require_admin_or_root)):
    p = _get_or_404(db, provider_id)
    return update_provider(db, p, payload)


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider_endpoint(provider_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(require_admin_or_root)):
    p = _get_or_404(db, provider_id)
    delete_provider(db, p)
