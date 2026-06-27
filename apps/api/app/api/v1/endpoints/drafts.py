from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.rate_limit import limiter
from app.db.session import get_db
from app.models.draft import OutreachDraft
from app.models.user import User
from app.schemas.company import ApproveDraftRequest, OutreachDraftRead, SyncResponse
from app.services.orchestrator import ResearchOrchestrator

router = APIRouter(prefix="/drafts")


@router.post("/{draft_id}/approve", response_model=OutreachDraftRead)
@limiter.limit("20/minute")
def approve_draft(request: Request, draft_id: int, payload: ApproveDraftRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> OutreachDraft:
    orchestrator = ResearchOrchestrator(db)
    return orchestrator.approve_draft(draft_id, current_user, payload.notes)


@router.post("/{draft_id}/sync", response_model=SyncResponse)
@limiter.limit("10/minute")
def sync_draft(request: Request, draft_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    orchestrator = ResearchOrchestrator(db)
    return orchestrator.sync_draft(draft_id)