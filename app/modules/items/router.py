import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_root, require_authenticated
from app.db.session import get_db
from app.modules.items.models import Item
from app.modules.items.schemas import ItemCreate, ItemRead, ItemUpdate
from app.modules.items.service import create_item, delete_item, get_item, list_items, update_item
from app.modules.users.models import User

router = APIRouter(prefix="/items", tags=["items"])


def _get_or_404(db: Session, item_id: uuid.UUID) -> Item:
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


def _assert_org(current_user: User, item: Item):
    if current_user.role != "root" and item.org_id != current_user.org_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


@router.get("", response_model=list[ItemRead])
def get_items(db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    if current_user.role == "root":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Root must specify org")
    return list_items(db, current_user.org_id)


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def post_item(payload: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    if current_user.role == "root":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Root must specify org")
    return create_item(db, payload, current_user.org_id)


@router.get("/{item_id}", response_model=ItemRead)
def get_item_by_id(item_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    item = _get_or_404(db, item_id)
    _assert_org(current_user, item)
    return item


@router.put("/{item_id}", response_model=ItemRead)
def put_item(item_id: uuid.UUID, payload: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    item = _get_or_404(db, item_id)
    _assert_org(current_user, item)
    return update_item(db, item, payload, current_user.id)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(item_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    item = _get_or_404(db, item_id)
    _assert_org(current_user, item)
    delete_item(db, item)
