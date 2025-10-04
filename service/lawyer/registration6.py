from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.lawyer.registration1 import LawyerRegistration1
from models.lawyer.registration6 import LawyerRegistration6
from schemas.lawyer.registration6 import (
    LawyerRegistration6Create,
    LawyerRegistration6Update
)


# -------------------------
# Create LawyerRegistration6
# -------------------------
def create_lawyer_registration6(db: Session, data: LawyerRegistration6Create):
    # ✅ 1. Validate lawyer_id exists in LawyerRegistration1
    lawyer = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == data.lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lawyer with id {data.lawyer_id} not found"
        )

    # ✅ 2. Get lawyer's code_id
    lawyer_code_id = lawyer.code_id

    # ✅ 3. Check if registration6 already exists
    existing_entry = db.query(LawyerRegistration6).filter(LawyerRegistration6.lawyer_id == data.lawyer_id).first()

    if existing_entry:
        # 🔄 Update existing record
        existing_entry.professional_associations = data.professional_associations
        existing_entry.certifications = [cert.dict() for cert in data.certifications] if data.certifications else None
        existing_entry.awards = [award.dict() for award in data.awards] if data.awards else None
        existing_entry.publications = [pub.dict() for pub in data.publications] if data.publications else None

        existing_entry.code_id = lawyer_code_id  # ✅ update code_id

        db.commit()
        db.refresh(existing_entry)
        return existing_entry

    # ➕ Create new record
    new_entry = LawyerRegistration6(
        lawyer_id=data.lawyer_id,
        professional_associations=data.professional_associations,
        certifications=[cert.dict() for cert in data.certifications] if data.certifications else None,
        awards=[award.dict() for award in data.awards] if data.awards else None,
        publications=[pub.dict() for pub in data.publications] if data.publications else None,
        code_id=lawyer_code_id  # ✅ assign code_id automatically
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry




# -------------------------
# Get LawyerRegistration6 by ID
# -------------------------
def get_lawyer_registration6(db: Session, id: str):
    record = db.query(LawyerRegistration6).filter(LawyerRegistration6.id == id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {id} not found"
        )
    return record


# -------------------------
# Update LawyerRegistration6
# -------------------------
def update_lawyer_registration6(db: Session, id: str, data: LawyerRegistration6Update):
    record = db.query(LawyerRegistration6).filter(LawyerRegistration6.id == id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {id} not found"
        )

    if data.professional_associations is not None:
        record.professional_associations = data.professional_associations
    if data.certifications is not None:
        record.certifications = [cert.dict() for cert in data.certifications]
    if data.awards is not None:
        record.awards = [award.dict() for award in data.awards]
    if data.publications is not None:
        record.publications = [pub.dict() for pub in data.publications]

    db.commit()
    db.refresh(record)
    return record

