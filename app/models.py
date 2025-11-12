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

class JobPosting(BaseModel):
    job_id: str
    company: str
    title: str
    url: str
    description: str
    location: str
    requirements: List[str]
    tech_stack: List[str]

class Recommendation(BaseModel):
    job: JobPosting
    relevance_score: float
    explanation: str
    matched_skills: List[str]
    resume_references: List[str]

class AgentThought(BaseModel):
    step: int
    thought: str
    action: str
    observation: str

class ResumeUploadRequest(BaseModel):
    resume: Resume
    preferences: UserPreferences

class ParseEmailRequest(BaseModel):
    email_text: str

class ParseEmailResponse(BaseModel):
    jobs: List[Dict[str, str]]
    count: int
    unique_companies: int

class ParsedJob(BaseModel):
    company: str
    title: str

class AgentStep(BaseModel):
    step_number: int
    thought: str
    action: str
    action_input: str
    observation: str
    
class JobScrapingResult(BaseModel):
    success: bool
    job_id: Optional[str] = None
    company: str
    title: str
    url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    requirements: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    error: Optional[str] = None
    agent_steps: List[AgentStep] = []

class BatchScrapeRequest(BaseModel):
    jobs: List[ParsedJob]
    
class BatchScrapeResponse(BaseModel):
    total_jobs: int
    successful: int
    failed: int
    results: List[JobScrapingResult]