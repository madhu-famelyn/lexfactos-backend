from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BarDetail(BaseModel):
    bar_license_number: str
    bar_association_name: str
    state: str
    city: str


class EducationDetail(BaseModel):
    degree: str
    college_name: str
    graduation_year: int   


class LawyerRegistration2Create(BaseModel):
    lawyer_id: str
    bio: str
    years_of_experience: int
    bar_details: List[BarDetail]
    languages_spoken: str
    education: List[EducationDetail]


class LawyerRegistration2Update(BaseModel):
    bio: Optional[str] = None
    years_of_experience: Optional[int] = None
    bar_details: Optional[List[BarDetail]] = None
    languages_spoken: Optional[str] = None
    education: Optional[List[EducationDetail]] = None



class LawyerRegistration2Read(BaseModel):
    id: str
    lawyer_id: str
    bio: str
    years_of_experience: int
    bar_details: List[BarDetail]
    languages_spoken: str
    education: List[EducationDetail]
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        from_attributes = True 
