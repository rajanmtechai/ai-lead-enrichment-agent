from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyRead

router = APIRouter(prefix="/companies")


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Company:
    company = db.query(Company).filter(Company.id == company_id).one_or_none()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company