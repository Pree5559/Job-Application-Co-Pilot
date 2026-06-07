# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ApplicationStatusUpdate(BaseModel):
    status: str

class RegenerateRequest(BaseModel):
    section: str

class DraftResponse(BaseModel):
    fit_analysis: Optional[str] = None
    resume_rewrite: Optional[str] = None
    cover_letter: Optional[str] = None
    interview_qa: Optional[str] = None
    ats_score: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    id: int
    job_title: str
    company: str
    jd_text: str
    jd_url: Optional[str] = None
    resume_sections: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class ApplicationDetailResponse(ApplicationResponse):
    original_resume_text: str
    drafts: Optional[DraftResponse] = None

    class Config:
        from_attributes = True