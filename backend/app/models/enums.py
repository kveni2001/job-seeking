from enum import Enum


class WorkMode(str, Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"


class ApplicationStatus(str, Enum):
    SAVED = "SAVED"
    APPLYING = "APPLYING"
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    OFFERED = "OFFERED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class ExperienceLevel(str, Enum):
    INTERNSHIP = "INTERNSHIP"
    ENTRY = "ENTRY"
    MID = "MID"
    SENIOR = "SENIOR"
    LEAD = "LEAD"
    EXECUTIVE = "EXECUTIVE"
