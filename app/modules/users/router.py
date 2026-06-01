import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_root, require_authenticated, require_root
from app.db.session import get_db
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate
from app.modules.users.service import create_user, delete_user, get_user, list_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


def _get_or_404(db: Session, user_id: uuid.UUID) -> User:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def _assert_access(requesting_user: User, target_user: User):
    if requesting_user.role == "root":
        return
    if requesting_user.role == "admin" and requesting_user.org_id == target_user.org_id:
        return
    if requesting_user.id == target_user.id:
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


@router.get("", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    return list_users(db, current_user)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def post_user(payload: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    try:
        return create_user(db, payload, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    target = _get_or_404(db, user_id)
    _assert_access(current_user, target)
    return target


@router.put("/{user_id}", response_model=UserRead)
def put_user(user_id: uuid.UUID, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    target = _get_or_404(db, user_id)
    _assert_access(current_user, target)
    return update_user(db, target, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_root)):
    target = _get_or_404(db, user_id)
    if target.role == "root":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete root user")
    _assert_access(current_user, target)
    delete_user(db, target)
