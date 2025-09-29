from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base schema (common fields)
class LawyerRegistration5Base(BaseModel):
    lawyer_id: str
    street_address: str
    city: str
    state: str
    zip_code: str
    calendly_link: Optional[str] = None
    working_hours: Optional[str] = None  # e.g., "Mon-Fri: 9AM-6PM"


# Create schema
class LawyerRegistration5Create(LawyerRegistration5Base):
    pass


# Update schema
class LawyerRegistration5Update(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    calendly_link: Optional[str] = None
    working_hours: Optional[str] = None


# Response / Read schema
class LawyerRegistration5Out(LawyerRegistration5Base):
    id: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True



class LawyerRegistration5Read(LawyerRegistration5Out):
    pass
