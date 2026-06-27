from pydantic import BaseModel, ConfigDict, Field


class ResearchRequest(BaseModel):
    query: str = Field(min_length=2)


class ExecutiveRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    title: str
    email: str | None = None
    linkedin_url: str | None = None
    seniority: str


class OutreachDraftRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: str
    status: str
    subject_lines: list
    content: dict
    notes: str
    crm_sync_status: str


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    domain: str
    name: str
    industry: str
    description: str
    pricing: dict
    hiring_signals: dict
    funding: dict
    recent_news: list
    tech_stack: list
    competitors: list
    buying_signals: list
    pain_points: list
    outreach_angles: list
    icp_score: float
    executives: list[ExecutiveRead]
    drafts: list[OutreachDraftRead]


class CompanyProfileResponse(BaseModel):
    company: CompanyRead
    insights: dict


class ApproveDraftRequest(BaseModel):
    notes: str = ""


class SyncResponse(BaseModel):
    draft_id: int
    provider: str
    status: str
    response: dict