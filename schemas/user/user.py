from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ----------- Base Schema -----------
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str
    photo: Optional[str] = None  # file path or URL


# ----------- Create Schema -----------
class UserCreate(UserBase):
    password: str   # plain password (will be hashed before storing)


# ----------- Response Schema -----------
class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # ✅ Pydantic v2 replacement for orm_mode
