# routes/lawyer/registration5.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.db.session import get_db 

from schemas.lawyer.registration5 import (
    LawyerRegistration5Create,
    LawyerRegistration5Update,
    LawyerRegistration5Read,
)
from service.lawyer import registration5

lawyer_registration5_router = APIRouter(
    prefix="/lawyers/registration5",
    tags=["Lawyer Registration Step 5"],
)


@lawyer_registration5_router.post("/", response_model=LawyerRegistration5Read, status_code=status.HTTP_201_CREATED)
def create_registration5(
    registration_data: LawyerRegistration5Create,
    db: Session = Depends(get_db),
):
    return registration5.create_registration5(db, registration_data)


@lawyer_registration5_router.get("/{reg5_id}", response_model=LawyerRegistration5Read)
def get_registration5_by_id(
    reg5_id: str,
    db: Session = Depends(get_db),
):
    return registration5.get_registration5_by_id(db, reg5_id)


@lawyer_registration5_router.put("/{reg5_id}", response_model=LawyerRegistration5Read)
def update_registration5(
    reg5_id: str,
    update_data: LawyerRegistration5Update,
    db: Session = Depends(get_db),
):
    return registration5.update_registration5(db, reg5_id, update_data)
