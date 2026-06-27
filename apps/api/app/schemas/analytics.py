from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    companies: int
    drafts: int
    approved: int
    synced: int