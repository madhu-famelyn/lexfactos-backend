from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from service.user.jobpost import (
    create_job_post,
    update_job_post,
    update_job_post_status,
    get_job_posts_by_user_id,
    get_job_post_by_id,
    update_job_verified_status
)
from schemas.user.jobpost import JobPostCreate, JobPostUpdate, JobPostUpdateStatus, JobPostGet, JobPostUpdateVerified
from config.db.session import get_db
from datetime import datetime

post_job_router = APIRouter(tags=["Post Job"])

@post_job_router.post("/job-posts/", response_model=JobPostGet)
def create_job(job_post: JobPostCreate, db: Session = Depends(get_db)):
    """
    Creates a new job post.
    - Requires job_post details.
    - Returns the created job post with details like status, creation date, etc.
    """
    return create_job_post(db, job_post)

@post_job_router.put("/job-posts/{job_post_id}", response_model=JobPostGet)
def update_job(
    job_post_id: str, job_post: JobPostUpdate, db: Session = Depends(get_db)
):
    """
    Updates a job post by job_post_id.
    - Only fields that are updated will be modified.
    - Returns the updated job post.
    """
    return update_job_post(db, job_post_id, job_post)

@post_job_router.patch("/job-posts/{job_post_id}/status", response_model=JobPostGet)
def update_status(
    job_post_id: str, status: JobPostUpdateStatus, db: Session = Depends(get_db)
):
    """
    Updates the status of a job post (active/inactive).
    - Takes the new status (True/False).
    - Returns the job post with updated status.
    """
    return update_job_post_status(db, job_post_id, status)

@post_job_router.get("/job-posts/", response_model=List[JobPostGet])
def get_jobs_by_user(user_id: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    job_posts = get_job_posts_by_user_id(db, user_id, skip, limit)
    
    for job in job_posts:
        if job.updated_at is None:
            job.updated_at = datetime.now()  # Set to current datetime if it's None
    
    return job_posts


@post_job_router.get("/job-posts/{job_post_id}", response_model=JobPostGet)
def get_job(job_post_id: str, db: Session = Depends(get_db)):
    job_post = get_job_post_by_id(db, job_post_id)
    if job_post.updated_at is None:
        job_post.updated_at = datetime.utcnow()  # Set it to current time
    return job_post




@post_job_router.put("/{job_id}/verified", response_model=JobPostGet)
def change_verified_status(
    job_id: str,
    verified_data: JobPostUpdateVerified,
    db: Session = Depends(get_db)
):
    """
    Update the verified status of a job post.
    """
    job = update_job_verified_status(db, job_id, verified_data.verified)
    return job