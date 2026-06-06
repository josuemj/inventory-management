import uuid

from sqlalchemy.orm import Session

from app.modules.change_logs.service import record_change
from app.modules.items.models import Item
from app.modules.items.schemas import ItemCreate, ItemUpdate


def list_items(db: Session, org_id: uuid.UUID) -> list[Item]:
    return db.query(Item).filter(Item.org_id == org_id).order_by(Item.name).all()


def get_item(db: Session, item_id: uuid.UUID) -> Item | None:
    return db.get(Item, item_id)


def create_item(db: Session, payload: ItemCreate, org_id: uuid.UUID) -> Item:
    item = Item(
        org_id=org_id,
        name=payload.name.strip(),
        price=payload.price,
        stock=payload.stock,
        category_id=payload.category_id,
        provider_id=payload.provider_id,
        image_url=payload.image_url,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item: Item, payload: ItemUpdate, user_id: uuid.UUID) -> Item:
    tracked_fields = ("name", "price", "stock", "category_id", "provider_id")
    for field in tracked_fields:
        new_val = getattr(payload, field)
        if new_val is not None:
            old_val = getattr(item, field)
            if str(old_val) != str(new_val):
                record_change(
                    db,
                    org_id=item.org_id,
                    user_id=user_id,
                    entity_type="item",
                    entity_id=item.id,
                    field=field,
                    old_value=str(old_val) if old_val is not None else None,
                    new_value=str(new_val),
                )
                setattr(item, field, new_val)
    if payload.image_url is not None:
        item.image_url = payload.image_url
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: Item) -> None:
    db.delete(item)
    db.commit()
