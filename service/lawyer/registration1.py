from sqlalchemy.orm import Session
from fastapi import UploadFile
from models.lawyer.registration1 import LawyerRegistration1
from schemas.lawyer.registration1 import LawyerCreate, LawyerUpdate
from service.s3_service import upload_to_s3
from utils.hashing import Hash  


from sqlalchemy import desc

def generate_next_code_id(db: Session) -> str:
    """
    Generate the next code_id in the sequence IN0001, IN0002, ...
    Finds the highest existing code_id and increments it.
    """
    last_lawyer = (
        db.query(LawyerRegistration1)
        .filter(LawyerRegistration1.code_id.like("IN%"))
        .order_by(desc(LawyerRegistration1.code_id))
        .first()
    )

    if not last_lawyer or not last_lawyer.code_id:
        return "IN0001"

    last_code = last_lawyer.code_id  # e.g., IN0020
    try:
        num_part = int(last_code.replace("IN", ""))
    except ValueError:
        num_part = 0

    next_num = num_part + 1
    return f"IN{next_num:04d}"


def create_lawyer(db: Session, lawyer_data: LawyerCreate, photo: UploadFile):
    if lawyer_data.password != lawyer_data.confirm_password:
        raise ValueError("Passwords do not match")

    photo_url = upload_to_s3(photo, folder="lawyers")

    # 👇 Generate next code_id automatically
    new_code_id = generate_next_code_id(db)

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
        code_id=new_code_id,   # ✅ auto-generated here
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
