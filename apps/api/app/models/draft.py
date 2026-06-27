from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OutreachDraft(Base):
    __tablename__ = "outreach_drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    executive_id: Mapped[int | None] = mapped_column(ForeignKey("executives.id", ondelete="SET NULL"), nullable=True)
    kind: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending_review", nullable=False)
    subject_lines: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    content: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    crm_sync_status: Mapped[str] = mapped_column(String(50), default="not_synced", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    company = relationship("Company", back_populates="drafts")
    executive = relationship("Executive")
    approvals = relationship("ApprovalRecord", back_populates="draft", cascade="all, delete-orphan")
    sync_jobs = relationship("CrmSyncJob", back_populates="draft", cascade="all, delete-orphan")