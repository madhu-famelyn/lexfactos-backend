from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config.db.session import get_db
from schemas.lawyer.registration3 import (
    LawyerRegistration3Create,
    LawyerRegistration3Update,
    LawyerRegistration3Read,
)
from service.lawyer.registration3 import (
    create_lawyer_registration3,
    get_registration3_by_lawyer_id,
    update_lawyer_registration3,
)

lawyer_registration3_router = APIRouter(
    prefix="/lawyer-registration3",
    tags=["Lawyer Registration 3"]
)


# -------------------
# Create a new LawyerRegistration3 profile
# -------------------
@lawyer_registration3_router.post("/", response_model=LawyerRegistration3Read, status_code=status.HTTP_201_CREATED)
def create_profile(data: LawyerRegistration3Create, db: Session = Depends(get_db)):
    return create_lawyer_registration3(db, data)


# -------------------
# Get a LawyerRegistration3 profile by lawyer_id
# -------------------
@lawyer_registration3_router.get("/{lawyer_id}", response_model=LawyerRegistration3Read)
def read_profile(lawyer_id: str, db: Session = Depends(get_db)):
    return get_registration3_by_lawyer_id(db, lawyer_id)


# -------------------
# Update a LawyerRegistration3 profile
# -------------------
@lawyer_registration3_router.put("/{profile_id}", response_model=LawyerRegistration3Read)
def update_profile(profile_id: str, update_data: LawyerRegistration3Update, db: Session = Depends(get_db)):
    return update_lawyer_registration3(db, profile_id, update_data)
