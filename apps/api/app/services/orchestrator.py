from fastapi import HTTPException, status
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.audit import ApprovalRecord, AuditLog, CrmSyncJob
from app.models.company import Company, Executive, ResearchArtifact
from app.models.draft import OutreachDraft
from app.models.user import User
from app.schemas.company import CompanyProfileResponse
from app.services.buying_signal_service import BuyingSignalService
from app.services.crm_service import CRMService
from app.services.embedding_service import EmbeddingService
from app.services.enrichment_service import EnrichmentService
from app.services.icp_service import ICPScoringService
from app.services.outreach_service import OutreachService
from app.services.research_service import ResearchService


class ResearchOrchestrator:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.research_service = ResearchService()
        self.enrichment_service = EnrichmentService()
        self.icp_service = ICPScoringService()
        self.signal_service = BuyingSignalService()
        self.outreach_service = OutreachService()
        self.embedding_service = EmbeddingService()
        self.crm_service = CRMService()

    def run(self, query: str, created_by: User | None = None) -> CompanyProfileResponse:
        snapshot = self.research_service.analyze(query)
        executives = self.enrichment_service.enrich_executives(snapshot.name, snapshot.domain)
        icp_score, reasons = self.icp_service.score(snapshot.industry, snapshot.hiring_signals, snapshot.competitors)
        buying_signals = self.signal_service.detect(snapshot.name, snapshot.hiring_signals, snapshot.funding, snapshot.recent_news)
        pain_points = ["pipeline quality", "research efficiency", "sales cycle speed"] if icp_score >= 50 else ["market education"]
        outreach_angles = [f"Lead with {pain_points[0]}", f"Anchor on {buying_signals[0]}"]
        drafts = self.outreach_service.generate(snapshot.name, [e.__dict__ for e in executives], icp_score, buying_signals, pain_points)

        company = self.db.query(Company).filter(Company.domain == snapshot.domain).one_or_none()
        if company is None:
            company = Company(
                domain=snapshot.domain,
                name=snapshot.name,
                industry=snapshot.industry,
                description=snapshot.description,
                pricing=snapshot.pricing,
                hiring_signals=snapshot.hiring_signals,
                funding=snapshot.funding,
                recent_news=snapshot.recent_news,
                tech_stack=snapshot.tech_stack,
                competitors=snapshot.competitors,
                buying_signals=buying_signals,
                pain_points=pain_points,
                outreach_angles=outreach_angles,
                icp_score=icp_score,
            )
            self.db.add(company)
            self.db.flush()
        else:
            company.name = snapshot.name
            company.industry = snapshot.industry
            company.description = snapshot.description
            company.pricing = snapshot.pricing
            company.hiring_signals = snapshot.hiring_signals
            company.funding = snapshot.funding
            company.recent_news = snapshot.recent_news
            company.tech_stack = snapshot.tech_stack
            company.competitors = snapshot.competitors
            company.buying_signals = buying_signals
            company.pain_points = pain_points
            company.outreach_angles = outreach_angles
            company.icp_score = icp_score

        self.db.query(Executive).filter(Executive.company_id == company.id).delete()
        for candidate in executives:
            self.db.add(Executive(company_id=company.id, **candidate.__dict__))

        artifact = ResearchArtifact(company_id=company.id, source="heuristic-research", artifact_type="company_profile", content={"reasons": reasons, "buying_signals": buying_signals})
        self.db.add(artifact)
        self.db.flush()
        self.embedding_service.upsert_company(company.id, f"{company.name} {company.description} {company.industry}")

        self.db.query(OutreachDraft).filter(OutreachDraft.company_id == company.id).delete()
        created_drafts: list[OutreachDraft] = []
        for draft in drafts:
            outreach_draft = OutreachDraft(company_id=company.id, kind=draft["kind"], subject_lines=draft["subject_lines"], content=draft["content"], notes=draft["notes"])
            self.db.add(outreach_draft)
            created_drafts.append(outreach_draft)

        self.db.add(AuditLog(user_id=created_by.id if created_by else None, action="research.company", entity_type="company", entity_id=str(company.id), details={"query": query}))
        self.db.commit()
        self.db.refresh(company)

        return CompanyProfileResponse(
            company=company,
            insights={
                "icp_score": icp_score,
                "buying_signals": buying_signals,
                "pain_points": pain_points,
                "recommendations": outreach_angles,
                "summary": f"{company.name} is a {company.industry} prospect with {icp_score:.0f}/100 ICP fit.",
                "signal_reasoning": reasons,
            },
        )

    def approve_draft(self, draft_id: int, user: User, notes: str = "") -> OutreachDraft:
        draft = self.db.query(OutreachDraft).filter(OutreachDraft.id == draft_id).one()
        draft.status = "approved"
        draft.approved_at = datetime.now(timezone.utc)
        approval = ApprovalRecord(draft_id=draft_id, user_id=user.id, notes=notes)
        self.db.add(approval)
        self.db.add(AuditLog(user_id=user.id, action="draft.approve", entity_type="draft", entity_id=str(draft_id), details={"notes": notes}))
        self.db.commit()
        self.db.refresh(draft)
        return draft

    def sync_draft(self, draft_id: int, provider: str = "hubspot") -> dict:
        draft = self.db.query(OutreachDraft).filter(OutreachDraft.id == draft_id).one()
        if draft.status != "approved":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Draft must be approved before CRM sync")
        response = self.crm_service.sync(provider, {"kind": draft.kind, "content": draft.content})
        job = CrmSyncJob(draft_id=draft_id, provider=provider, status=response["status"], payload={"kind": draft.kind}, response=response)
        draft.crm_sync_status = response["status"]
        self.db.add(job)
        self.db.add(AuditLog(user_id=None, action="crm.sync", entity_type="draft", entity_id=str(draft_id), details=response))
        self.db.commit()
        return {"draft_id": draft_id, "provider": provider, "status": response["status"], "response": response}