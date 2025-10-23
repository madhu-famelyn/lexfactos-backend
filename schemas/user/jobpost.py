# schemas/user/job_post.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobPostBase(BaseModel):
    jobTitle: Optional[str] = None
    jobType: Optional[str] = None
    practiceArea: Optional[str] = None
    specialization: Optional[str] = None
    experienceLevel: Optional[str] = None
    jobDescription: Optional[str] = None
    location: Optional[str] = None
    workMode: Optional[str] = None
    contactInfo: Optional[str] = None


class JobPostCreate(JobPostBase):
    user_id: str
    jobTitle: str
    jobType: str


class JobPostUpdate(JobPostBase):
    status: Optional[bool] = None


class JobPostUpdateStatus(BaseModel):
    status: bool


class JobPostUpdateVerified(BaseModel):
    verified: bool  # ✅ separate schema for verified update


class JobPostGet(JobPostBase):
    id: str
    user_id: str
    status: bool
    verified: bool  # ✅ include verified in output
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
