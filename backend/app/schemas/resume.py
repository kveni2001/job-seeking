from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ParsedContactInfo(BaseModel):
    """Extracted contact details from resume."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    location: Optional[str] = None


class ParsedEducationItem(BaseModel):
    """Extracted education entry."""
    institution: str = Field(..., description="University or educational institution name")
    degree: Optional[str] = Field(None, description="Degree or qualification (e.g. B.S., M.S.)")
    field_of_study: Optional[str] = Field(None, description="Field of study or major")
    start_year: Optional[int] = None
    end_year: Optional[int] = None


class ParsedExperienceItem(BaseModel):
    """Extracted work experience entry."""
    company: str = Field(..., description="Company or organization name")
    title: str = Field(..., description="Job role or title")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None


class ResumeParsedData(BaseModel):
    """Structured data extracted from resume by the parser."""
    contact_info: Optional[ParsedContactInfo] = None
    summary: Optional[str] = Field(None, description="Candidate summary or objective statement")
    skills: List[str] = Field(default_factory=list, description="Extracted skills and technologies")
    education: List[ParsedEducationItem] = Field(default_factory=list)
    experience: List[ParsedExperienceItem] = Field(default_factory=list)
    raw_text: Optional[str] = Field(None, description="Extracted raw text content")


class ResumeBase(BaseModel):
    """Base resume metadata."""
    file_name: str = Field(..., description="Original filename of the uploaded resume PDF")
    title: Optional[str] = Field(None, max_length=150, description="User-friendly title (e.g. 'Backend Focused')")
    is_primary: bool = Field(default=False, description="Whether this is the user's primary/default resume")


class ResumeCreate(ResumeBase):
    """Payload to record an uploaded resume."""
    file_path: str = Field(..., description="Relative storage path of the uploaded file")
    file_size_bytes: Optional[int] = Field(None, ge=0, description="File size in bytes")


class ResumeUpdate(BaseModel):
    """Payload to update resume metadata."""
    title: Optional[str] = Field(None, max_length=150)
    is_primary: Optional[bool] = None
    extracted_skills: Optional[List[str]] = None


class ResumeResponse(ResumeBase):
    """Response schema for a user resume."""
    id: UUID = Field(..., description="Resume UUID")
    user_id: UUID = Field(..., description="User UUID who owns this resume")
    file_path: str = Field(..., description="File storage path")
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes")
    extracted_skills: List[str] = Field(default_factory=list, description="Parsed skills")
    parsed_data: Optional[Dict[str, Any]] = Field(default=None, description="JSON payload of extracted resume sections")
    created_at: datetime = Field(..., description="Upload timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ResumeUploadResponse(BaseModel):
    """Response wrapper returned after resume PDF upload and parsing."""
    message: str = Field(default="Resume uploaded and parsed successfully")
    resume: ResumeResponse


class SkillMatchRequest(BaseModel):
    """Request to match a resume against a target job description."""
    resume_id: UUID = Field(..., description="Resume UUID to evaluate")
    job_description: str = Field(..., min_length=20, description="Raw job description text")


class SkillMatchResponse(BaseModel):
    """Results of matching resume skills with job requirements."""
    resume_id: UUID
    match_score_percentage: float = Field(..., ge=0.0, le=100.0, description="Matching score out of 100")
    matching_skills: List[str] = Field(default_factory=list, description="Skills present in both resume and job")
    missing_skills: List[str] = Field(default_factory=list, description="Required skills absent in resume")
