from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from config.db.session import get_db
from models.user.postjobs import JobPost  # Import your JobPost model

# ===========================================================
# ✅ Router Setup
# ===========================================================
get_all_jobs_router = APIRouter(prefix="/jobs", tags=["Jobs"])

# ===========================================================
# ✅ SCHEMA
# ===========================================================
class JobPostOut(BaseModel):
    id: str
    user_id: Optional[str]
    jobTitle: str
    jobType: Optional[str]
    practiceArea: Optional[str]
    specialization: Optional[str]
    experienceLevel: Optional[str]
    jobDescription: Optional[str]
    location: Optional[str]
    workMode: Optional[str]
    contactInfo: Optional[str]
    status: Optional[bool] = False
    verified: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ===========================================================
# ✅ SERVICE FUNCTION
# ===========================================================
def get_filtered_jobs(
    db: Session,
    title: Optional[str] = None,
    city: Optional[str] = None,
    role: Optional[str] = None,
    most_recent: bool = False,
    skip: int = 0,
    limit: int = 50,
    verified: Optional[bool] = None,
    status: Optional[bool] = None,
):
    """
    Fetch job posts with optional filters and sorting.
    Supports filtering by title, location (city), role, verified, and status.
    """
    try:
        query = db.query(JobPost)

        # Apply filters
        if title:
            query = query.filter(JobPost.jobTitle.ilike(f"%{title}%"))
        if city:
            query = query.filter(JobPost.location.ilike(f"%{city}%"))
        if role:
            query = query.filter(JobPost.practiceArea.ilike(f"%{role}%"))
        if verified is not None:
            query = query.filter(JobPost.verified == verified)
        if status is not None:
            query = query.filter(JobPost.status == status)

        # Sorting
        if most_recent:
            query = query.order_by(JobPost.created_at.desc())
        else:
            query = query.order_by(JobPost.created_at.asc())

        jobs = query.offset(skip).limit(limit).all()
        return jobs

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching job posts")

# ===========================================================
# ✅ ROUTE
# ===========================================================
@get_all_jobs_router.get("/", response_model=List[JobPostOut])
def get_all_jobs(
    title: Optional[str] = Query(None, description="Search by job title"),
    city: Optional[str] = Query(None, description="Filter by city (uses 'location' field)"),
    role: Optional[str] = Query(None, description="Filter by role/practice area"),
    most_recent: Optional[bool] = Query(False, description="Sort by most recent jobs"),
    verified: Optional[bool] = Query(None, description="Filter by verified status"),
    status: Optional[bool] = Query(None, description="Filter by job active/inactive status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db),
):
    """
    ✅ Fetch all jobs or filter by title, location, role, verified, or status.
    Supports pagination and sorting by most recent or oldest.
    """
    jobs = get_filtered_jobs(
        db=db,
        title=title,
        city=city,
        role=role,
        most_recent=most_recent,
        verified=verified,
        status=status,
        skip=skip,
        limit=limit,
    )

    return [
        JobPostOut(
            id=job.id,
            user_id=job.user_id,
            jobTitle=job.jobTitle,
            jobType=job.jobType,
            practiceArea=job.practiceArea,
            specialization=job.specialization,
            experienceLevel=job.experienceLevel,
            jobDescription=job.jobDescription,
            location=job.location,
            workMode=job.workMode,
            contactInfo=job.contactInfo,
            status=job.status,
            verified=job.verified,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]
