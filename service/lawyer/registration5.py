from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.lawyer.registration1 import LawyerRegistration1
from models.lawyer.registration5 import LawyerRegistration5
from schemas.lawyer.registration5 import (
    LawyerRegistration5Create,
    LawyerRegistration5Update,
)


def create_registration5(db: Session, registration_data: LawyerRegistration5Create):
    # ✅ Check if lawyer exists
    lawyer = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == registration_data.lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lawyer with id {registration_data.lawyer_id} not found",
        )

    # ✅ Check if Registration5 already exists
    existing = db.query(LawyerRegistration5).filter(LawyerRegistration5.lawyer_id == registration_data.lawyer_id).first()

    if existing:
        # 🔄 Update existing record
        for field, value in registration_data.dict().items():
            setattr(existing, field, value)

        db.commit()
        db.refresh(existing)
        return existing

    # ➕ Create new record
    new_reg5 = LawyerRegistration5(**registration_data.dict())
    db.add(new_reg5)
    db.commit()
    db.refresh(new_reg5)
    return new_reg5



def get_registration5_by_id(db: Session, reg5_id: str):
    reg5 = db.query(LawyerRegistration5).filter(LawyerRegistration5.id == reg5_id).first()
    if not reg5:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LawyerRegistration5 with id {reg5_id} not found",
        )
    return reg5


def update_registration5(db: Session, reg5_id: str, update_data: LawyerRegistration5Update):
    reg5 = db.query(LawyerRegistration5).filter(LawyerRegistration5.id == reg5_id).first()
    if not reg5:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LawyerRegistration5 with id {reg5_id} not found",
        )

    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(reg5, key, value)

    db.commit()
    db.refresh(reg5)
    return reg5


