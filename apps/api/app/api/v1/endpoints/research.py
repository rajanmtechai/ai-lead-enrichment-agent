from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.rate_limit import limiter
from app.db.session import get_db
from app.models.user import User
from app.schemas.company import CompanyProfileResponse, ResearchRequest
from app.services.orchestrator import ResearchOrchestrator

router = APIRouter(prefix="/research")


@router.post("/company", response_model=CompanyProfileResponse)
@limiter.limit("20/minute")
def research_company(request: Request, payload: ResearchRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> CompanyProfileResponse:
    orchestrator = ResearchOrchestrator(db)
    return orchestrator.run(payload.query, created_by=current_user)