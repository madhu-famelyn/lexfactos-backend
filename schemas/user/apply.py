from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import enum


class RatingEnum(str, enum.Enum):
    GOOD_FIT = "Good fit"
    MAYBE = "Maybe"
    NOT_A_FIT = "Not a fit"
    NOT_DECIDED = "Not decided"


class JobApplicationUpdateStatus(BaseModel):
    rate: RatingEnum


class JobApplicationCreate(BaseModel):
    job_id: str
    user_id: str 
    applicant_name: str
    email: EmailStr
    mobile_number: Optional[str] = None
    resume_url: str
    cover_letter: Optional[str] = None


class JobApplicationOut(BaseModel):
    id: str
    job_id: str
    user_id: str
    applicant_name: str
    email: EmailStr
    mobile_number: Optional[str] = None
    resume_url: str
    cover_letter: Optional[str] = None
    applied_at: datetime
    rate: RatingEnum                     # ✅ Added here
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
