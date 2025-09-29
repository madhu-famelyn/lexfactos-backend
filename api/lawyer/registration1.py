from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from schemas.lawyer.registration1 import LawyerCreate, LawyerUpdate, LawyerRead, LawyerVerificationUpdate
from models.lawyer.registration1 import LawyerRegistration1
from service.lawyer import registration1 as lawyer_service 
from config.db.session import get_db
from typing import Optional

lawyer_registration1_router = APIRouter(prefix="/lawyers", tags=["Lawyers"])


from datetime import datetime

@lawyer_registration1_router.post("/", response_model=LawyerRead)
def create_lawyer(
    full_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    gender: str = Form(None),
    dob: str = Form(None),
    linkedin_url: str = Form(None),
    website_url: str = Form(None),
    photo: UploadFile = File(...),
    short_note: str = Form(...),
    db: Session = Depends(get_db),
):
    # ✅ Convert dob to date
    parsed_dob = None
    if dob:
        try:
            parsed_dob = datetime.strptime(dob, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("DOB must be in DD-MM-YYYY format")

    # ✅ Handle empty URLs as None
    linkedin_url = linkedin_url or None
    website_url = website_url or None

    lawyer_data = LawyerCreate(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        password=password,
        confirm_password=confirm_password,
        gender=gender,
        dob=parsed_dob,
        linkedin_url=linkedin_url,
        website_url=website_url,
        short_note=short_note,
        photo="temp",  # replaced later by S3
    )
    return lawyer_service.create_lawyer(db, lawyer_data, photo)



@lawyer_registration1_router.get("/{lawyer_id}", response_model=LawyerRead)
def get_lawyer(lawyer_id: str, db: Session = Depends(get_db)):
    return lawyer_service.get_lawyer(db, lawyer_id)


@lawyer_registration1_router.put("lawyer/{lawyer_id}", response_model=LawyerRead)
def update_lawyer(
    lawyer_id: str,
    full_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    dob: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    website_url: Optional[str] = Form(None),
    photo_file: Optional[UploadFile] = File(None),
    photo_url: Optional[str] = Form(None),  # NEW: accept URL
    short_note:Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Convert DOB to date if provided
    dob_date = None
    if dob:
        dob_date = datetime.strptime(dob, "%d-%m-%Y").date()

    linkedin_url = linkedin_url if linkedin_url else None
    website_url = website_url if website_url else None
    photo = photo_url if photo_url else photo_file

    update_data = LawyerUpdate(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        password=password,
        gender=gender,
        dob=dob_date,
        linkedin_url=linkedin_url,
        website_url=website_url,
        short_note=short_note,
        photo="temp",
    )

    return lawyer_service.update_lawyer(db, lawyer_id, update_data, photo)







@lawyer_registration1_router.put("/lawyers/{lawyer_id}/verification")
def update_lawyer_verification(
    lawyer_id: str,
    payload: LawyerVerificationUpdate,
    db: Session = Depends(get_db),
):
    lawyer = db.query(LawyerRegistration1).filter(LawyerRegistration1.id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")

    lawyer.is_verified = payload.is_verified
    # Only update rejection_reason if provided
    if payload.rejection_reason is not None:
        lawyer.rejection_reason = payload.rejection_reason

    db.commit()
    db.refresh(lawyer)

    return {
        "message": "Lawyer verification status updated successfully",
        "lawyer_id": lawyer.id,
        "is_verified": lawyer.is_verified,
        "rejection_reason": lawyer.rejection_reason,
    }