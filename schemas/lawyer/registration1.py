from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import date, datetime



# ==============
# Base Schema
# ==============
class LawyerBase(BaseModel):
    full_name: str
    gender: Optional[str] = None
    dob: Optional[date] = None
    email: EmailStr
    phone_number: str
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None
    photo: str
    short_note:str


# ==============
# Create Schema
# ==============
class LawyerCreate(LawyerBase):
    password: str
    confirm_password: str   # used only for validation, not stored in DB


# ==============
# Update Schema
# ==============
class LawyerUpdate(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None
    photo: Optional[str] = None
    password: Optional[str] = None
    short_note:str




class LawyerVerificationUpdate(BaseModel):
    is_verified: bool
    rejection_reason: Optional[str] = None



# ==============
# Read Schema
# ==============
class LawyerRead(LawyerBase):
    id: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True
