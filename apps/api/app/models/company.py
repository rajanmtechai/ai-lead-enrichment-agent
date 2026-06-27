from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(255), default="Unknown", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    pricing: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    hiring_signals: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    funding: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    recent_news: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    tech_stack: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    competitors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    buying_signals: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    pain_points: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    outreach_angles: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    icp_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()"))

    executives = relationship("Executive", back_populates="company", cascade="all, delete-orphan")
    artifacts = relationship("ResearchArtifact", back_populates="company", cascade="all, delete-orphan")
    drafts = relationship("OutreachDraft", back_populates="company", cascade="all, delete-orphan")


class Executive(Base):
    __tablename__ = "executives"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    seniority: Mapped[str] = mapped_column(String(100), default="mid", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    company = relationship("Company", back_populates="executives")


class ResearchArtifact(Base):
    __tablename__ = "research_artifacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    embedding_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    company = relationship("Company", back_populates="artifacts")