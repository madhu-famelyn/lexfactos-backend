from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from models.user.postjobs import JobPost
from schemas.user.jobpost import JobPostCreate, JobPostUpdate, JobPostUpdateStatus
from typing import List
from models.user.user import User
from datetime import datetime


def create_job_post(db: Session, job_post_create: JobPostCreate) -> JobPost:
    try:
        # Fetch user details to dynamically assign contact info
        user = db.query(User).filter(User.id == job_post_create.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Build contact info dynamically
        contact_info_parts = []
        if user.mobile_number:
            contact_info_parts.append(f"Mobile: {user.mobile_number}")
        if user.email:
            contact_info_parts.append(f"Email: {user.email}")
        contact_info = " | ".join(contact_info_parts)

        # Explicitly set created_at and updated_at
        now = datetime.utcnow()

        # Create JobPost
        new_job_post = JobPost(
            user_id=job_post_create.user_id,
            jobTitle=job_post_create.jobTitle,
            jobType=job_post_create.jobType,
            practiceArea=job_post_create.practiceArea,
            specialization=job_post_create.specialization,
            experienceLevel=job_post_create.experienceLevel,
            jobDescription=job_post_create.jobDescription,
            location=job_post_create.location,
            workMode=job_post_create.workMode,
            contactInfo=contact_info,
            status=True,
            created_at=now,
            updated_at=now
        )

        db.add(new_job_post)
        db.commit()
        db.refresh(new_job_post)
        return new_job_post

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating job post: {str(e)}")


# 2. Update an existing JobPost
def update_job_post(db: Session, job_post_id: str, job_post_update: JobPostUpdate) -> JobPost:
    try:
        db_job_post = db.query(JobPost).filter(JobPost.id == job_post_id).first()
        if not db_job_post:
            raise HTTPException(status_code=404, detail="Job post not found")

        for field, value in job_post_update.dict(exclude_unset=True).items():
            setattr(db_job_post, field, value)

        # Always update the updated_at timestamp
        db_job_post.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_job_post)
        return db_job_post

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating job post: {str(e)}")


# 3. Update the status of a JobPost (Activate/Deactivate)
def update_job_post_status(db: Session, job_post_id: str, status_update: JobPostUpdateStatus) -> JobPost:
    try:
        db_job_post = db.query(JobPost).filter(JobPost.id == job_post_id).first()
        if not db_job_post:
            raise HTTPException(status_code=404, detail="Job post not found")

        db_job_post.status = status_update.status
        db_job_post.updated_at = datetime.utcnow()  # Ensure updated_at is set

        db.commit()
        db.refresh(db_job_post)
        return db_job_post

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating job post status: {str(e)}")


# 4. Get all JobPosts by user_id
def get_job_posts_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 10):
    try:
        job_posts = (
            db.query(JobPost)
            .filter(JobPost.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return job_posts

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job posts: {str(e)}")


# 5. Get a single JobPost by ID
def get_job_post_by_id(db: Session, job_post_id: str) -> JobPost:
    try:
        db_job_post = db.query(JobPost).filter(JobPost.id == job_post_id).first()
        if not db_job_post:
            raise HTTPException(status_code=404, detail="Job post not found")
        return db_job_post

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job post: {str(e)}")






def update_job_verified_status(db: Session, job_id: str, verified: bool):
    job = db.query(JobPost).filter(JobPost.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.verified = verified
    db.commit()
    db.refresh(job)
    return job