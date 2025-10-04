from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.lawyer.registration3 import LawyerRegistration3
from models.lawyer.registration1 import LawyerRegistration1
from schemas.lawyer.registration3 import (
    LawyerRegistration3Create,
    LawyerRegistration3Update,
    LawyerRegistration3Read,
)


# -------------------
# Create a new lawyer professional profile
# -------------------



def create_lawyer_registration3(db: Session, data: LawyerRegistration3Create) -> LawyerRegistration3:
    # ✅ 1. Check if lawyer exists in lawyerRegistration1
    lawyer = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == data.lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer ID not found in lawyerRegistration1"
        )

    # ✅ 2. Get lawyer's code_id
    lawyer_code_id = lawyer.code_id

    # ✅ 3. Check if registration3 already exists for this lawyer
    existing_profile = db.query(LawyerRegistration3).filter(
        LawyerRegistration3.lawyer_id == data.lawyer_id
    ).first()

    if existing_profile:
        # 🔄 Update existing profile
        existing_profile.practice_area = data.practice_area
        existing_profile.court_admitted_to = data.court_admitted_to
        existing_profile.active_since = data.active_since

        existing_profile.work_experience = [
            {
                "company_name": we.company_name,
                "role": we.role,
                "duration": we.duration,
                "description": we.description
            }
            for we in data.work_experience
        ]

        existing_profile.code_id = lawyer_code_id  # ✅ update code_id too

        db.commit()
        db.refresh(existing_profile)
        return existing_profile

    # ➕ Create new profile
    new_profile = LawyerRegistration3(
        lawyer_id=data.lawyer_id,
        practice_area=data.practice_area,
        court_admitted_to=data.court_admitted_to,
        active_since=data.active_since,
        work_experience=[
            {
                "company_name": we.company_name,
                "role": we.role,
                "duration": we.duration,
                "description": we.description
            }
            for we in data.work_experience
        ],
        code_id=lawyer_code_id  # ✅ assign automatically
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


# -------------------
# Get lawyer registration3 profile by lawyer_id
# -------------------
def get_registration3_by_lawyer_id(db: Session, lawyer_id: str) -> LawyerRegistration3:
    profile = db.query(LawyerRegistration3).filter(LawyerRegistration3.lawyer_id == lawyer_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found for this lawyer")
    return profile


# -------------------
# Update lawyer registration3 profile
# -------------------
def update_lawyer_registration3(db: Session, profile_id: str, update_data: LawyerRegistration3Update) -> LawyerRegistration3:
    profile = db.query(LawyerRegistration3).filter(LawyerRegistration3.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lawyer registration3 profile not found")

    update_data_dict = update_data.dict(exclude_unset=True)

    # Convert nested Pydantic objects to dict
    if "work_experience" in update_data_dict and update_data_dict["work_experience"] is not None:
        update_data_dict["work_experience"] = [we.dict() for we in update_data_dict["work_experience"]]

    for key, value in update_data_dict.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
