from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_authenticated
from app.db.session import get_db
from app.modules.inventory_movements.schemas import MovementCreate, MovementRead
from app.modules.inventory_movements.service import create_movement, list_movements
from app.modules.users.models import User

router = APIRouter(prefix="/inventory-movements", tags=["inventory-movements"])


@router.get("", response_model=list[MovementRead])
def get_movements(db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    if current_user.role == "root":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Root must specify org")
    return list_movements(db, current_user.org_id)


@router.post("", response_model=MovementRead, status_code=status.HTTP_201_CREATED)
def post_movement(payload: MovementCreate, db: Session = Depends(get_db), current_user: User = Depends(require_authenticated)):
    if current_user.role == "root":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Root must specify org")
    return create_movement(db, payload, current_user.id, current_user.org_id)
