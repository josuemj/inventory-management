from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.companies.models import Company
from app.modules.users.models import User, UserRole
from app.modules.users.schemas import UserCreate


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


def create_user(db: Session, payload: UserCreate) -> User:
    role = payload.role
    company_id = payload.company_id

    if role == UserRole.SUPERADMIN and company_id is not None:
        raise ValueError("Superadmin must not have company_id")
    if role in (UserRole.ADMIN, UserRole.EMPLOYEE) and company_id is None:
        raise ValueError("Admin and employee require company_id")
    if company_id is not None:
        company = db.query(Company).filter(Company.id == company_id).first()
        if company is None:
            raise ValueError("company_id does not exist")

    user = User(
        company_id=company_id,
        full_name=payload.full_name.strip(),
        username=payload.username.strip().lower(),
        password=hash_password(payload.password),
        role=role.value,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Username already exists or data violates constraints") from exc
    db.refresh(user)
    return user
