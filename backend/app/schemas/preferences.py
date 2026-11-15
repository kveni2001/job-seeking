from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from app.models.enums import ExperienceLevel, WorkMode


class UserPreferenceBase(BaseModel):
    """Base job seeking preferences and profile tracker fields."""
    target_job_titles: List[str] = Field(
        default_factory=list,
        description="List of target job roles/titles (e.g. ['Backend Engineer', 'Python Developer'])"
    )
    preferred_locations: List[str] = Field(
        default_factory=list,
        description="Preferred job locations or cities (e.g. ['San Francisco, CA', 'Remote'])"
    )
    work_modes: List[WorkMode] = Field(
        default_factory=lambda: [WorkMode.REMOTE, WorkMode.HYBRID],
        description="Allowed work modes (REMOTE, HYBRID, ONSITE)"
    )
    min_salary: Optional[int] = Field(
        default=None,
        ge=0,
        description="Minimum acceptable annual or hourly salary"
    )
    max_salary: Optional[int] = Field(
        default=None,
        ge=0,
        description="Target maximum salary expectation"
    )
    currency: str = Field(
        default="USD",
        max_length=3,
        description="3-letter currency code (e.g. USD, EUR, INR)"
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Key skills and technologies (e.g. ['Python', 'FastAPI', 'PostgreSQL'])"
    )
    years_of_experience: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=50.0,
        description="Total professional years of experience"
    )
    experience_level: Optional[ExperienceLevel] = Field(
        default=None,
        description="Target seniority level"
    )
    notice_period_days: Optional[int] = Field(
        default=None,
        ge=0,
        description="Notice period in days"
    )
    auto_apply_enabled: bool = Field(
        default=False,
        description="Toggle automated application submission"
    )
    max_daily_applications: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Safety threshold for maximum automated applications per day"
    )
    blacklisted_companies: List[str] = Field(
        default_factory=list,
        description="Companies to exclude from matching or applying"
    )
    blacklisted_keywords: List[str] = Field(
        default_factory=list,
        description="Job title/description keywords to reject"
    )
    phone_number: Optional[str] = Field(
        default=None,
        max_length=30,
        description="Contact phone number"
    )
    linkedin_url: Optional[str] = Field(
        default=None,
        description="LinkedIn profile URL"
    )
    github_url: Optional[str] = Field(
        default=None,
        description="GitHub profile URL"
    )
    portfolio_url: Optional[str] = Field(
        default=None,
        description="Personal website or portfolio URL"
    )
    custom_notes: Optional[str] = Field(
        default=None,
        description="Additional preferences or prompts for application letter/answer generation"
    )


class UserPreferenceCreate(UserPreferenceBase):
    """Payload to create user preferences."""
    pass


class UserPreferenceUpdate(BaseModel):
    """Payload to update existing user preferences (all fields optional)."""
    target_job_titles: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    work_modes: Optional[List[WorkMode]] = None
    min_salary: Optional[int] = Field(default=None, ge=0)
    max_salary: Optional[int] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, max_length=3)
    skills: Optional[List[str]] = None
    years_of_experience: Optional[float] = Field(default=None, ge=0.0, le=50.0)
    experience_level: Optional[ExperienceLevel] = None
    notice_period_days: Optional[int] = Field(default=None, ge=0)
    auto_apply_enabled: Optional[bool] = None
    max_daily_applications: Optional[int] = Field(default=None, ge=1, le=100)
    blacklisted_companies: Optional[List[str]] = None
    blacklisted_keywords: Optional[List[str]] = None
    phone_number: Optional[str] = Field(default=None, max_length=30)
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    custom_notes: Optional[str] = None


class UserPreferenceResponse(UserPreferenceBase):
    """Response schema for user preferences."""
    id: UUID = Field(..., description="Unique preference record UUID")
    user_id: UUID = Field(..., description="Associated user UUID")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record last update timestamp")

    model_config = ConfigDict(from_attributes=True)
