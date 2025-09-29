# routers/lawyer_registration2.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from config.db.session import get_db
from schemas.lawyer.registration2 import (
    LawyerRegistration2Create,
    LawyerRegistration2Update,
    LawyerRegistration2Read,
)

from service.lawyer import registration2

lawyer_registration2_router = APIRouter(prefix="/lawyer-profile", tags=["Lawyer Profile"])


# -------------------------
# Create Lawyer Profile
# -------------------------
@lawyer_registration2_router.post(
    "/",
    response_model=LawyerRegistration2Read,
    status_code=status.HTTP_201_CREATED,
)
def create_lawyer_profile(data: LawyerRegistration2Create, db: Session = Depends(get_db)):
    return registration2.create_lawyer_profile(db, data)


# -------------------------
# Get Lawyer Profile by Lawyer ID
# -------------------------
@lawyer_registration2_router.get(
    "/{lawyer_id}",
    response_model=LawyerRegistration2Read,
    status_code=status.HTTP_200_OK,
)
def get_lawyer_profile(lawyer_id: str, db: Session = Depends(get_db)):
    return registration2.get_profile_by_lawyer_id(db, lawyer_id)


# -------------------------
# Update Lawyer Profile by Profile ID
# -------------------------
@lawyer_registration2_router.put(
    "/{profile_id}",
    response_model=LawyerRegistration2Read,
    status_code=status.HTTP_200_OK,
)
def update_lawyer_profile(
    profile_id: str,
    update_data: LawyerRegistration2Update,
    db: Session = Depends(get_db),
):
    return registration2.update_lawyer_profile(db, profile_id, update_data)
