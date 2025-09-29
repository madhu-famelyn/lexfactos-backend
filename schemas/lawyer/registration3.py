from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# -------------------

# -------------------
class WorkExperienceDetail(BaseModel):
    company_name: str
    role: str
    duration: str
    description: Optional[str] = None 


class LawyerRegistration3Create(BaseModel):
    lawyer_id: str
    practice_area: str
    court_admitted_to: str
    active_since: int
    work_experience: List[WorkExperienceDetail] 



# -------------------
# Update Schema
# -------------------
class LawyerRegistration3Update(BaseModel):
    practice_area: Optional[str] = None
    court_admitted_to: Optional[str] = None
    active_since: Optional[int] = None
    work_experience: Optional[List[WorkExperienceDetail]] = None
    # description: Optional[str] = None            # lawyer’s overall description


# -------------------
# Read / Response Schema
# -------------------
class LawyerRegistration3Read(BaseModel):
    id: str
    lawyer_id: str
    practice_area: str
    court_admitted_to: str
    active_since: int
    work_experience: List[WorkExperienceDetail]
    # description: Optional[str] = None
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        from_attributes = True  # allows ORM objects to work with Pydantic
