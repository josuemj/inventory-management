import uuid

from sqlalchemy.orm import Session

from app.modules.categories.models import Category
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate


def list_categories(db: Session, org_id: uuid.UUID) -> list[Category]:
    return db.query(Category).filter(Category.org_id == org_id).order_by(Category.name).all()


def get_category(db: Session, category_id: uuid.UUID) -> Category | None:
    return db.get(Category, category_id)


def create_category(db: Session, payload: CategoryCreate, org_id: uuid.UUID) -> Category:
    cat = Category(org_id=org_id, name=payload.name.strip())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def update_category(db: Session, cat: Category, payload: CategoryUpdate) -> Category:
    cat.name = payload.name.strip()
    db.commit()
    db.refresh(cat)
    return cat


def delete_category(db: Session, cat: Category) -> None:
    db.delete(cat)
    db.commit()
