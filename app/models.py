from pydantic import BaseModel
from typing import Optional, List, Dict

class Resume(BaseModel):
    text: str
    skills: Optional[List[str]] = None
    experience: Optional[List[str]] = None
    projects: Optional[List[str]] = None

class UserPreferences(BaseModel):
    role: List[str]
    experience_level: str
    tech_stack: Optional[List[str]] = None
    locations: Optional[List[str]] = None

class ResumeUploadRequest(BaseModel):
    resume: Resume
    preferences: UserPreferences