from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import ApplicationStatus, WorkMode


class ApplicationBase(BaseModel):
    """Base fields for job application tracking."""
    job_title: str = Field(..., max_length=255, description="Position or title applied for")
    company_name: str = Field(..., max_length=255, description="Employer / company name")
    job_url: Optional[str] = Field(None, description="Original posting URL")
    job_description: Optional[str] = Field(None, description="Job description or requirements summary")
    location: Optional[str] = Field(None, max_length=255, description="Job location (city, state, country)")
    work_mode: Optional[WorkMode] = Field(default=WorkMode.REMOTE, description="Work mode: REMOTE, HYBRID, ONSITE")
    salary_range: Optional[str] = Field(None, max_length=100, description="Advertised compensation range")
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED, description="Current tracking status")
    applied_at: Optional[datetime] = Field(None, description="Date/time when applied (defaults to now if omitted)")
    notes: Optional[str] = Field(None, description="Personal interview notes or application details")


class ApplicationCreate(ApplicationBase):
    """Payload to record a new job application."""
    resume_id: Optional[UUID] = Field(None, description="Resume ID used for this application")
    job_fingerprint: Optional[str] = Field(None, max_length=64, description="SHA-256 fingerprint for deduplication")


class ApplicationUpdate(BaseModel):
    """Payload to update an existing application."""
    job_title: Optional[str] = Field(None, max_length=255)
    company_name: Optional[str] = Field(None, max_length=255)
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=255)
    work_mode: Optional[WorkMode] = None
    salary_range: Optional[str] = Field(None, max_length=100)
    status: Optional[ApplicationStatus] = None
    applied_at: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    response_received_at: Optional[datetime] = None
    salary_offered: Optional[str] = Field(None, max_length=100)
    resume_id: Optional[UUID] = None
    notes: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    """Quick update for application stage/status."""
    status: ApplicationStatus = Field(..., description="New application status")
    notes: Optional[str] = Field(None, description="Optional note regarding this status change")
    interview_date: Optional[datetime] = Field(None, description="Interview scheduled datetime if applicable")


class ApplicationResponse(ApplicationBase):
    """Full application response schema."""
    id: UUID = Field(..., description="Unique application UUID")
    user_id: UUID = Field(..., description="User UUID who submitted this application")
    resume_id: Optional[UUID] = Field(None, description="Resume UUID used")
    job_fingerprint: Optional[str] = Field(None, description="SHA-256 deduplication fingerprint")
    interview_date: Optional[datetime] = Field(None, description="Upcoming or past interview datetime")
    response_received_at: Optional[datetime] = Field(None, description="Timestamp when company first responded")
    salary_offered: Optional[str] = Field(None, description="Final or offered compensation")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ApplicationFilter(BaseModel):
    """Query filter parameters for listing applications."""
    status: Optional[ApplicationStatus] = None
    work_mode: Optional[WorkMode] = None
    company_name: Optional[str] = None
    search_query: Optional[str] = Field(None, description="Free text search across job title, company, notes")
    applied_after: Optional[datetime] = None
    applied_before: Optional[datetime] = None


class ApplicationBulkCreate(BaseModel):
    """Payload to insert multiple applications at once (e.g. from crawler / automated pipeline)."""
    applications: List[ApplicationCreate] = Field(..., min_length=1, max_length=100)


class ApplicationBulkCreateResponse(BaseModel):
    """Response summary for bulk creation."""
    total_received: int
    total_created: int
    total_duplicates_skipped: int
    created_ids: List[UUID]
