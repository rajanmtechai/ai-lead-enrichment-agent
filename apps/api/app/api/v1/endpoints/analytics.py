from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.rate_limit import limiter
from app.db.session import get_db
from app.models.company import Company
from app.models.draft import OutreachDraft
from app.models.user import User
from app.schemas.analytics import AnalyticsOverview

router = APIRouter(prefix="/analytics")


@router.get("/overview", response_model=AnalyticsOverview)
@limiter.limit("30/minute")
def overview(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> AnalyticsOverview:
    companies = db.query(func.count(Company.id)).scalar() or 0
    drafts = db.query(func.count(OutreachDraft.id)).scalar() or 0
    approved = db.query(func.count(OutreachDraft.id)).filter(OutreachDraft.status == "approved").scalar() or 0
    synced = db.query(func.count(OutreachDraft.id)).filter(OutreachDraft.crm_sync_status == "queued").scalar() or 0
    return AnalyticsOverview(companies=companies, drafts=drafts, approved=approved, synced=synced)