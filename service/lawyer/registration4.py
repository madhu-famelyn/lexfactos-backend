from sqlalchemy.orm import Session
from models.lawyer.registration4 import LawyerRegistration4
from models.lawyer.registration1 import LawyerRegistration1
from schemas.lawyer.registration4 import (
    LawyerRegistration4Create,
    LawyerRegistration4Update
)
from fastapi import UploadFile, File, HTTPException
from service.s3_service import upload_to_s3



def create_lawyer_registration4(db: Session, lawyer_data: LawyerRegistration4Create, office_image: UploadFile = None):
    # ✅ Check if lawyer_id exists in LawyerRegistration1
    lawyer_exists = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == lawyer_data.lawyer_id).first()
    if not lawyer_exists:
        raise ValueError(f"Lawyer with id {lawyer_data.lawyer_id} does not exist")

    # ✅ Upload image to S3 (if provided)
    office_image_url = None
    if office_image:
        office_image_url = upload_to_s3(office_image, folder="lawyers")

    # ✅ Check if registration4 already exists
    existing_entry = db.query(LawyerRegistration4).filter(LawyerRegistration4.lawyer_id == lawyer_data.lawyer_id).first()

    if existing_entry:
        # 🔄 Update existing entry
        if office_image_url:
            existing_entry.office_image = office_image_url
        existing_entry.case_results = [case.dict() for case in lawyer_data.case_results] if lawyer_data.case_results else None

        db.commit()
        db.refresh(existing_entry)
        return existing_entry

    # ➕ Create new record
    db_lawyer4 = LawyerRegistration4(
        lawyer_id=lawyer_data.lawyer_id,
        office_image=office_image_url,
        case_results=[case.dict() for case in lawyer_data.case_results] if lawyer_data.case_results else None,
    )
    db.add(db_lawyer4)
    db.commit()
    db.refresh(db_lawyer4)
    return db_lawyer4



# Get LawyerRegistration4 by ID
def get_lawyer_registration4(db: Session, lawyer4_id: str):
    return db.query(LawyerRegistration4).filter(LawyerRegistration4.id == lawyer4_id).first()


# Get LawyerRegistration4 by Lawyer ID
def get_lawyer_registration4_by_lawyer(db: Session, lawyer_id: str):
    return db.query(LawyerRegistration4).filter(LawyerRegistration4.lawyer_id == lawyer_id).first()


# Get all LawyerRegistration4
def get_all_lawyer_registration4(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LawyerRegistration4).offset(skip).limit(limit).all()


# Update LawyerRegistration4
def update_lawyer_registration4(db: Session, lawyer4_id: str, update_data: LawyerRegistration4Update):
    db_lawyer4 = db.query(LawyerRegistration4).filter(LawyerRegistration4.id == lawyer4_id).first()
    if not db_lawyer4:
        return None

    if update_data.office_image is not None:
        db_lawyer4.office_image = update_data.office_image

    if update_data.case_results is not None:
        db_lawyer4.case_results = [case.dict() for case in update_data.case_results]

    db.commit()
    db.refresh(db_lawyer4)
    return db_lawyer4


