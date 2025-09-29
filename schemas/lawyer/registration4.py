from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class CaseResult(BaseModel):
    title: str
    outcome: str
    summary: str
    court: Optional[str] = None
    year: Optional[int] = None  



class LawyerRegistration4Base(BaseModel):
    lawyer_id: str
    case_results: Optional[List[CaseResult]] = None



class LawyerRegistration4Create(LawyerRegistration4Base):
    pass



class LawyerRegistration4Out(LawyerRegistration4Base):
    id: str
    office_image: Optional[str] = None

    class Config:
        orm_mode = True


class LawyerRegistration4Update(BaseModel):
    office_image: Optional[str] = None
    case_results: Optional[List[CaseResult]] = None



class LawyerRegistration4OutExtended(LawyerRegistration4Base):
    id: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True
