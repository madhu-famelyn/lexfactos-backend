from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ----------- Base Schema -----------
class AdminBase(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str


# ----------- Create Schema -----------
class AdminCreate(AdminBase):
    password: str  



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ----------- Response Schema -----------
class AdminResponse(AdminBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  
