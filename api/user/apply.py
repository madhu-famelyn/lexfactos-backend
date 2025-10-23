# src/routers/job_application_router.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from config.db.session import get_db
from service.user.apply import (
    apply_job_service,
    get_applications_by_job_service,
    get_applications_by_user_service,
    update_job_application_status
)
from schemas.user.apply import JobApplicationOut, JobApplicationUpdateStatus
from typing import List





job_application_router = APIRouter(prefix="/job-applications", tags=["Job Applications"])

# ============================
# ✅ Apply Job (with resume upload to S3)
# ============================
@job_application_router.post("/", response_model=JobApplicationOut)
async def apply_job(
    job_id: str = Form(...),
    user_id: str = Form(...),
    applicant_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(None),
    cover_letter: str = Form(None),
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Apply for a job (Lawyer portal)
    Accepts multipart/form-data including resume file.
    The resume is uploaded to S3 and the URL is stored in the database.
    """
    try:
        job_app = apply_job_service(
            db=db,
            job_id=job_id,
            user_id=user_id,
            applicant_name=applicant_name,
            email=email,
            mobile_number=mobile_number,
            resume_file=resume_file,
            cover_letter=cover_letter
        )
        return job_app
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================
# ✅ Get Applications by Job ID
# ============================
@job_application_router.get("/job/{job_id}", response_model=List[JobApplicationOut])
def get_applications_by_job(job_id: str, db: Session = Depends(get_db)):
    """
    Get all applications for a specific job using job ID
    """
    try:
        return get_applications_by_job_service(db=db, job_id=job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================
# ✅ Get Applications by User ID
# ============================
@job_application_router.get("/user/{user_id}", response_model=List[JobApplicationOut])
def get_applications_by_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get all applications made by a specific user using user ID
    """
    try:
        return get_applications_by_user_service(db=db, user_id=user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





@job_application_router.put("/{job_application_id}/status", response_model=JobApplicationOut)
def update_status(
    job_application_id: str,
    status_data: JobApplicationUpdateStatus,
    db: Session = Depends(get_db),
):
    """
    Update the rating status of a job application (Good fit, Maybe, Not a fit, Not decided)
    """
    updated_app = update_job_application_status(db, job_application_id, status_data)
    return updated_app