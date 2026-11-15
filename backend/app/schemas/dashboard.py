from datetime import date, datetime
from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import ApplicationStatus, WorkMode


class StatusCount(BaseModel):
    """Aggregated count for a specific status."""
    status: ApplicationStatus
    count: int = Field(..., ge=0)


class WorkModeCount(BaseModel):
    """Aggregated count for a work mode."""
    work_mode: WorkMode
    count: int = Field(..., ge=0)


class DailyApplicationCount(BaseModel):
    """Application volume by day for chart trends."""
    date: date
    count: int = Field(..., ge=0)


class RecentApplicationItem(BaseModel):
    """Compact summary of an application for dashboard feeds."""
    id: UUID
    job_title: str
    company_name: str
    status: ApplicationStatus
    work_mode: Optional[WorkMode] = None
    applied_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardStatsResponse(BaseModel):
    """Consolidated analytics data for the user dashboard."""
    total_applications: int = Field(..., ge=0, description="Total all-time applications")
    applications_today: int = Field(..., ge=0, description="Applications submitted today")
    applications_this_week: int = Field(..., ge=0, description="Applications submitted in current 7-day window")
    applications_this_month: int = Field(..., ge=0, description="Applications submitted in current 30-day window")
    status_counts: Dict[ApplicationStatus, int] = Field(
        default_factory=dict,
        description="Counts breakdown by application status"
    )
    work_mode_counts: Dict[WorkMode, int] = Field(
        default_factory=dict,
        description="Counts breakdown by work mode"
    )
    recent_applications: List[RecentApplicationItem] = Field(
        default_factory=list,
        description="Most recent 5-10 applications"
    )
    application_trends: List[DailyApplicationCount] = Field(
        default_factory=list,
        description="Application counts for the last 30 days"
    )
    response_rate_percentage: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage of applications that received any company response"
    )
    interview_rate_percentage: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage of applications that progressed to interview"
    )
    active_resumes_count: int = Field(
        default=0,
        ge=0,
        description="Count of uploaded resumes for user"
    )

    model_config = ConfigDict(from_attributes=True)
