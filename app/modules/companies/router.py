from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.companies.schemas import CompanyCreate, CompanyRead
from app.modules.companies.service import create_company, list_companies


router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyRead])
def get_companies(db: Session = Depends(get_db)) -> list[CompanyRead]:
    return list_companies(db)


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def post_company(payload: CompanyCreate, db: Session = Depends(get_db)) -> CompanyRead:
    try:
        return create_company(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
