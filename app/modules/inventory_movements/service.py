import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.inventory_movements.models import InventoryMovement
from app.modules.inventory_movements.schemas import MovementCreate
from app.modules.items.models import Item


def list_movements(db: Session, org_id: uuid.UUID) -> list[InventoryMovement]:
    return (
        db.query(InventoryMovement)
        .join(Item, InventoryMovement.item_id == Item.id)
        .filter(Item.org_id == org_id)
        .order_by(InventoryMovement.created_at.desc())
        .all()
    )


def create_movement(db: Session, payload: MovementCreate, user_id: uuid.UUID, org_id: uuid.UUID) -> InventoryMovement:
    item: Item | None = db.get(Item, payload.item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.org_id != org_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Item not in your organization")

    if payload.movement_type in ("sale", "dispatch"):
        if item.stock < payload.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
        item.stock -= payload.quantity
    elif payload.movement_type == "add":
        item.stock += payload.quantity
    # adjustment: no automatic stock change, caller controls via item update

    movement = InventoryMovement(
        item_id=payload.item_id,
        user_id=user_id,
        movement_type=payload.movement_type,
        quantity=payload.quantity,
        note=payload.note,
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement
