# src/Service/job_application_service.py

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.user.apply import JobApplication
from models.user.postjobs import JobPost
from models.user.user import User
from datetime import datetime
import uuid
from schemas.user.apply import JobApplicationUpdateStatus


# Import your S3 upload function
from service.s3_service import upload_to_s3  # <- your S3 helper file

# ============================
# ✅ Service: Apply Job
def apply_job_service(
    db: Session,
    job_id: str,
    user_id: str,
    applicant_name: str,
    email: str,
    mobile_number: str = None,
    resume_file: UploadFile = None,
    cover_letter: str = None
):
    # Check if job exists
    job = db.query(JobPost).filter(JobPost.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not resume_file:
        raise HTTPException(status_code=400, detail="Resume file is required")

    # Upload resume to S3
    resume_url = upload_to_s3(resume_file, folder="resumes")

    # ✅ Create job application with default rate
    job_app = JobApplication(
        job_id=job_id,
        user_id=user_id,
        applicant_name=applicant_name,
        email=email,
        mobile_number=mobile_number,
        resume_url=resume_url,
        cover_letter=cover_letter,
        applied_at=datetime.utcnow(),
        rate="Not decided"  # ✅ set default value
    )

    db.add(job_app)
    db.commit()
    db.refresh(job_app)
    return job_app


# ============================
# ✅ Service: Get Applications by Job ID
# ============================
def get_applications_by_job_service(db: Session, job_id: str):
    applications = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
    if not applications:
        raise HTTPException(status_code=404, detail="No applications found for this job")
    return applications


# ============================
# ✅ Service: Get Applications by User ID
# ============================
def get_applications_by_user_service(db: Session, user_id: str):
    applications = db.query(JobApplication).filter(JobApplication.user_id == user_id).all()
    if not applications:
        raise HTTPException(status_code=404, detail="No applications found for this user")
    return applications





def update_job_application_status(
    db: Session, job_application_id: str, status_data: JobApplicationUpdateStatus
):
    job_app = db.query(JobApplication).filter(JobApplication.id == job_application_id).first()

    if not job_app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found"
        )

    job_app.rate = status_data.rate
    db.commit()
    db.refresh(job_app)
    return job_app