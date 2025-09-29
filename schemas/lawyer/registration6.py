from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# -------------------------
# Nested Schemas
# -------------------------
class Certification(BaseModel):
    title: str
    issuer: str
    year: int


class Award(BaseModel):
    name: str
    organization: str
    year: int


class Publication(BaseModel):
    title: str
    year: int
    link: Optional[str] = None
    description: Optional[str] = None


# -------------------------
# Base Schema
# -------------------------
class LawyerRegistration6Base(BaseModel):
    lawyer_id: str
    professional_associations: Optional[str] = None
    certifications: Optional[List[Certification]] = None
    awards: Optional[List[Award]] = None
    publications: Optional[List[Publication]] = None


# -------------------------
# Create Schema
# -------------------------
class LawyerRegistration6Create(LawyerRegistration6Base):
    pass


# -------------------------
# Update Schema
# -------------------------
class LawyerRegistration6Update(BaseModel):
    professional_associations: Optional[str] = None
    certifications: Optional[List[Certification]] = None
    awards: Optional[List[Award]] = None
    publications: Optional[List[Publication]] = None


# -------------------------
# Read / Response Schema
# -------------------------
class LawyerRegistration6Read(LawyerRegistration6Base):
    id: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True
