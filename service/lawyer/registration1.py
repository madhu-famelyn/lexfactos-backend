from sqlalchemy.orm import Session
from fastapi import UploadFile
from models.lawyer.registration1 import LawyerRegistration1
from schemas.lawyer.registration1 import LawyerCreate, LawyerUpdate
from service.s3_service import upload_to_s3
from utils.hashing import Hash  


def create_lawyer(db: Session, lawyer_data: LawyerCreate, photo: UploadFile):
    if lawyer_data.password != lawyer_data.confirm_password:
        raise ValueError("Passwords do not match")

    photo_url = upload_to_s3(photo, folder="lawyers")

    new_lawyer = LawyerRegistration1(
        full_name=lawyer_data.full_name,
        gender=lawyer_data.gender,
        dob=lawyer_data.dob,
        email=lawyer_data.email,
        phone_number=lawyer_data.phone_number,
        hashed_password=Hash.bcrypt(lawyer_data.password),
        linkedin_url=lawyer_data.linkedin_url,
        website_url=lawyer_data.website_url,
        photo=photo_url,
        short_note=lawyer_data.short_note,
    )

    db.add(new_lawyer)
    db.commit()
    db.refresh(new_lawyer)
    return new_lawyer


# READ (by ID)
def get_lawyer(db: Session, lawyer_id: str):
    return db.query(LawyerRegistration1).filter(LawyerRegistration1.id == lawyer_id).first()


# UPDATE
def update_lawyer(db: Session, lawyer_id: str, update_data: LawyerUpdate, photo=None):
    lawyer = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == lawyer_id).first()
    if not lawyer:
        return None

    # Update fields
    for key, value in update_data.dict(exclude_unset=True).items():
        if key == "password" and value:
            setattr(lawyer, "hashed_password", Hash.bcrypt(value))
        elif key != "photo":
            setattr(lawyer, key, value)

    # Update photo
    if photo:
        if isinstance(photo, UploadFile):
            photo_url = upload_to_s3(photo, folder="lawyers")
            lawyer.photo = photo_url
        elif isinstance(photo, str):
            lawyer.photo = photo  # direct URL

    db.commit()
    db.refresh(lawyer)
    return lawyer
