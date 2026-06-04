import uuid

from sqlalchemy.orm import Session

from app.modules.providers.models import Provider
from app.modules.providers.schemas import ProviderCreate, ProviderUpdate


def list_providers(db: Session) -> list[Provider]:
    return db.query(Provider).order_by(Provider.name).all()


def get_provider(db: Session, provider_id: uuid.UUID) -> Provider | None:
    return db.get(Provider, provider_id)


def create_provider(db: Session, payload: ProviderCreate) -> Provider:
    provider = Provider(name=payload.name.strip(), tel=payload.tel)
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


def update_provider(db: Session, provider: Provider, payload: ProviderUpdate) -> Provider:
    if payload.name is not None:
        provider.name = payload.name.strip()
    if payload.tel is not None:
        provider.tel = payload.tel
    db.commit()
    db.refresh(provider)
    return provider


def delete_provider(db: Session, provider: Provider) -> None:
    db.delete(provider)
    db.commit()
