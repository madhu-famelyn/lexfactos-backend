from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.lawyer.registration2 import LawyerRegistration2
from models.lawyer.registration1 import LawyerRegistration1
from schemas.lawyer.registration2 import (
    LawyerRegistration2Create,
    LawyerRegistration2Update,
    LawyerRegistration2Read,
)



def create_lawyer_profile(db: Session, data: LawyerRegistration2Create) -> LawyerRegistration2:
    # ✅ 1. Check if lawyer exists in lawyerRegistration1
    lawyer = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == data.lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer ID not found in lawyerRegistration1"
        )

    # ✅ 2. Extract code_id from LawyerRegistration1
    lawyer_code_id = lawyer.code_id

    # ✅ 3. Check if profile already exists
    existing_profile = db.query(LawyerRegistration2).filter(LawyerRegistration2.lawyer_id == data.lawyer_id).first()

    if existing_profile:
        # 🔄 Update existing profile
        existing_profile.bio = data.bio
        existing_profile.years_of_experience = data.years_of_experience
        existing_profile.bar_details = [bar.dict() for bar in data.bar_details]
        existing_profile.languages_spoken = data.languages_spoken
        existing_profile.education = [edu.dict() for edu in data.education]
        existing_profile.code_id = lawyer_code_id  # ✅ update code_id as well

        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        # ➕ Create new profile
        new_profile = LawyerRegistration2(
            lawyer_id=data.lawyer_id,
            bio=data.bio,
            years_of_experience=data.years_of_experience,
            bar_details=[bar.dict() for bar in data.bar_details],
            languages_spoken=data.languages_spoken,
            education=[edu.dict() for edu in data.education],
            code_id=lawyer_code_id  # ✅ added here
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile





def get_profile_by_lawyer_id(db: Session, lawyer_id: str) -> LawyerRegistration2:
    profile = db.query(LawyerRegistration2).filter(LawyerRegistration2.lawyer_id == lawyer_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found for this lawyer")
    return profile



def update_lawyer_profile(db: Session, profile_id: str, update_data: LawyerRegistration2Update) -> LawyerRegistration2:
    profile = db.query(LawyerRegistration2).filter(LawyerRegistration2.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lawyer profile not found")

    update_data_dict = update_data.dict(exclude_unset=True)

    # ✅ Convert nested Pydantic objects to dict
    if "bar_details" in update_data_dict and update_data_dict["bar_details"] is not None:
        update_data_dict["bar_details"] = [bar.dict() for bar in update_data_dict["bar_details"]]

    if "education" in update_data_dict and update_data_dict["education"] is not None:
        update_data_dict["education"] = [edu.dict() for edu in update_data_dict["education"]]

    for key, value in update_data_dict.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


