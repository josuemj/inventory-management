from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.companies.models import Company
from app.modules.companies.schemas import CompanyCreate


def list_companies(db: Session) -> list[Company]:
    return db.query(Company).order_by(Company.id.asc()).all()


def create_company(db: Session, payload: CompanyCreate) -> Company:
    company = Company(name=payload.name.strip())
    db.add(company)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Company name already exists") from exc
    db.refresh(company)
    return company
