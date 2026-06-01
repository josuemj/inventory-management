import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate


def list_users(db: Session, requesting_user: User) -> list[User]:
    if requesting_user.role == "root":
        return db.query(User).order_by(User.created_at.asc()).all()
    return db.query(User).filter(User.org_id == requesting_user.org_id).order_by(User.created_at.asc()).all()


def get_user(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, payload: UserCreate, requesting_user: User) -> User:
    if payload.role == "root":
        if requesting_user.role != "root":
            raise ValueError("Only root can create root users")
        org_id = None
    elif payload.role in ("admin", "member"):
        if requesting_user.role == "root":
            if payload.org_id is None:
                raise ValueError("org_id required for admin/member")
            org_id = payload.org_id
        else:
            org_id = requesting_user.org_id
    else:
        raise ValueError("Invalid role")

    user = User(
        org_id=org_id,
        full_name=payload.full_name.strip(),
        username=payload.username.strip().lower(),
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Username already exists")
    db.refresh(user)
    return user


def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    if payload.full_name is not None:
        user.full_name = payload.full_name.strip()
    if payload.password is not None:
        user.hashed_password = hash_password(payload.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
