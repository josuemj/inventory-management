import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_root, require_authenticated
from app.db.session import get_db
from app.modules.categories.models import Category
from app.modules.categories.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.modules.categories.service import (
    create_category, delete_category, get_category, list_categories, update_category,
)
from app.modules.users.models import User

router = APIRouter(prefix="/categories", tags=["categories"])


def _get_or_404(db: Session, category_id: uuid.UUID) -> Category:
    cat = get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return cat


def _assert_org(current_user: User, cat: Category):
    if current_user.role != "root" and cat.org_id != current_user.org_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


@router.get("", response_model=list[CategoryRead])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    org_id = current_user.org_id
    if current_user.role == "root":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Specify org via /organizations/{id}/categories")
    return list_categories(db, org_id)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def post_category(payload: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    org_id = current_user.org_id
    if current_user.role == "root":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Root must specify org")
    return create_category(db, payload, org_id)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    cat = _get_or_404(db, category_id)
    _assert_org(current_user, cat)
    return cat


@router.put("/{category_id}", response_model=CategoryRead)
def put_category(category_id: uuid.UUID, payload: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    cat = _get_or_404(db, category_id)
    _assert_org(current_user, cat)
    return update_category(db, cat, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_endpoint(category_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    cat = _get_or_404(db, category_id)
    _assert_org(current_user, cat)
    delete_category(db, cat)
