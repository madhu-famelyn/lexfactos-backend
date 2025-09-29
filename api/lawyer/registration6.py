from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from config.db.session import get_db
from schemas.lawyer.registration6 import (
    LawyerRegistration6Create,
    LawyerRegistration6Update,
    LawyerRegistration6Read
)
from service.lawyer.registration6 import (
    create_lawyer_registration6,
    get_lawyer_registration6,
    update_lawyer_registration6
)

lawyer_registration6_router = APIRouter(
    prefix="/lawyers/registration6",
    tags=["Lawyer Registration 6"]
)


# -------------------------
# Create a new record
# -------------------------
@lawyer_registration6_router.post("/", response_model=LawyerRegistration6Read, status_code=status.HTTP_201_CREATED)
def create_registration6(data: LawyerRegistration6Create, db: Session = Depends(get_db)):
    return create_lawyer_registration6(db, data)


# -------------------------
# Get a record by ID
# -------------------------
@lawyer_registration6_router.get("/{id}", response_model=LawyerRegistration6Read)
def read_registration6(id: str, db: Session = Depends(get_db)):
    return get_lawyer_registration6(db, id)


# -------------------------
# Update a record by ID
# -------------------------
@lawyer_registration6_router.put("/{id}", response_model=LawyerRegistration6Read)
def update_registration6(id: str, data: LawyerRegistration6Update, db: Session = Depends(get_db)):
    return update_lawyer_registration6(db, id, data)
