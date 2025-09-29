from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from config.db.session import get_db
from models.lawyer.registration1 import LawyerRegistration1
from models.lawyer.registration2 import LawyerRegistration2
from models.lawyer.registration3 import LawyerRegistration3
from models.lawyer.registration4 import LawyerRegistration4
from models.lawyer.registration5 import LawyerRegistration5
from models.lawyer.registration6 import LawyerRegistration6


from schemas.lawyer.registration2 import LawyerRegistration2Create
from schemas.lawyer.registration3 import LawyerRegistration3Create
from schemas.lawyer.registration4 import LawyerRegistration4Create
from schemas.lawyer.registration6 import LawyerRegistration6Create

get_all_router = APIRouter(
     prefix="/get-all-details",
    tags=["Get Lawyer Details"]
) 



@get_all_router.get("/lawyers/all-details/{lawyer_id}")
def get_lawyer_full_profile(lawyer_id: str, db: Session = Depends(get_db)):
    lawyer = (
        db.query(LawyerRegistration1)
        .options(
            joinedload(LawyerRegistration1.profile),
            joinedload(LawyerRegistration1.registration3),
            joinedload(LawyerRegistration1.registration4),
            joinedload(LawyerRegistration1.registration5),
            joinedload(LawyerRegistration1.registration6),
        )
        .filter(LawyerRegistration1.id == lawyer_id)
        .first()
    )

    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")

    return {
        # LawyerRegistration1
        "id": lawyer.id,
        "full_name": lawyer.full_name,
        "gender": lawyer.gender,
        "dob": lawyer.dob,
        "email": lawyer.email,
        "phone_number": lawyer.phone_number,
        "hashed_password": lawyer.hashed_password,
        "linkedin_url": lawyer.linkedin_url,
        "website_url": lawyer.website_url,
        "short_note": lawyer.short_note,
        "photo": lawyer.photo,
        "is_verified": lawyer.is_verified,

        "rejection_reason": lawyer.rejection_reason,
        "created_datetime": lawyer.created_datetime,
        "updated_datetime": lawyer.updated_datetime,

        # LawyerRegistration2 (profile)
        "profile": lawyer.profile and {
            "id": lawyer.profile.id,
            "lawyer_id": lawyer.profile.lawyer_id,
            "bio": lawyer.profile.bio,
            "years_of_experience": lawyer.profile.years_of_experience,
            "bar_details": lawyer.profile.bar_details,
            "languages_spoken": lawyer.profile.languages_spoken,
            "education": lawyer.profile.education,
            "created_datetime": lawyer.profile.created_datetime,
            "updated_datetime": lawyer.profile.updated_datetime,
        },

        # LawyerRegistration3
        "registration3": lawyer.registration3 and {
            "id": lawyer.registration3.id,
            "lawyer_id": lawyer.registration3.lawyer_id,
            "practice_area": lawyer.registration3.practice_area,
            "court_admitted_to": lawyer.registration3.court_admitted_to,
            "active_since": lawyer.registration3.active_since,
            "work_experience": lawyer.registration3.work_experience,
            "created_datetime": lawyer.registration3.created_datetime,
            "updated_datetime": lawyer.registration3.updated_datetime,
        },

        # LawyerRegistration4
        "registration4": lawyer.registration4 and {
            "id": lawyer.registration4.id,
            "lawyer_id": lawyer.registration4.lawyer_id,
            "office_image": lawyer.registration4.office_image,
            "case_results": lawyer.registration4.case_results,
            "created_datetime": lawyer.registration4.created_datetime,
            "updated_datetime": lawyer.registration4.updated_datetime,
        },

        # LawyerRegistration5 (list of addresses)
        "registration5": [
            {
                "id": reg5.id,
                "lawyer_id": reg5.lawyer_id,
                "street_address": reg5.street_address,
                "city": reg5.city,
                "state": reg5.state,
                "zip_code": reg5.zip_code,
                "calendly_link": reg5.calendly_link,
                "working_hours": reg5.working_hours,
                "latitude":reg5.latitude,
                "longitude":reg5.longitude,                
                "created_datetime": reg5.created_datetime,
                "updated_datetime": reg5.updated_datetime,
            }
            for reg5 in lawyer.registration5
        ],

        # LawyerRegistration6
        "registration6": lawyer.registration6 and {
            "id": lawyer.registration6.id,
            "lawyer_id": lawyer.registration6.lawyer_id,
            "professional_associations": lawyer.registration6.professional_associations,
            "certifications": lawyer.registration6.certifications,
            "awards": lawyer.registration6.awards,
            "publications": lawyer.registration6.publications,
            "created_datetime": lawyer.registration6.created_datetime,
            "updated_datetime": lawyer.registration6.updated_datetime,
        },
    }





@get_all_router.get("/lawyers/all")
def get_all_lawyers(db: Session = Depends(get_db)):
    lawyers = (
        db.query(LawyerRegistration1)
        .options(
            joinedload(LawyerRegistration1.profile),
            joinedload(LawyerRegistration1.registration3),
            joinedload(LawyerRegistration1.registration4),
            joinedload(LawyerRegistration1.registration5),
            joinedload(LawyerRegistration1.registration6),
        )
        .all()
    )

    if not lawyers:
        raise HTTPException(status_code=404, detail="No lawyers found")

    return [
        {
            "id": lawyer.id,
            "full_name": lawyer.full_name,
            "gender": lawyer.gender,
            "dob": lawyer.dob,
            "email": lawyer.email,
            "phone_number": lawyer.phone_number,
            "linkedin_url": lawyer.linkedin_url,
            "website_url": lawyer.website_url,
            "short_note": lawyer.short_note,
            "photo": lawyer.photo,
            "is_verified": lawyer.is_verified,
            "rejection_reason": lawyer.rejection_reason,
            "created_datetime": lawyer.created_datetime,
            "updated_datetime": lawyer.updated_datetime,

            "profile": lawyer.profile and {
                "bio": lawyer.profile.bio,
                "years_of_experience": lawyer.profile.years_of_experience,
                "bar_details": lawyer.profile.bar_details,
                "languages_spoken": lawyer.profile.languages_spoken,
                "education": lawyer.profile.education,
            },

            "registration3": lawyer.registration3 and {
                "practice_area": lawyer.registration3.practice_area,
                "court_admitted_to": lawyer.registration3.court_admitted_to,
                "active_since": lawyer.registration3.active_since,
                "work_experience": lawyer.registration3.work_experience,
            },

            "registration4": lawyer.registration4 and {
                "office_image": lawyer.registration4.office_image,
                "case_results": lawyer.registration4.case_results,
            },

            "registration5": [
                {
                    "street_address": reg5.street_address,
                    "city": reg5.city,
                    "state": reg5.state,
                    "zip_code": reg5.zip_code,
                    "calendly_link": reg5.calendly_link,
                    "working_hours": reg5.working_hours,
                    "latitude":reg5.latitude,
                    "longitude":reg5.longitude,
                }
                for reg5 in lawyer.registration5
            ],

            "registration6": lawyer.registration6 and {
                "professional_associations": lawyer.registration6.professional_associations,
                "certifications": lawyer.registration6.certifications,
                "awards": lawyer.registration6.awards,
                "publications": lawyer.registration6.publications,
            }
        }
        for lawyer in lawyers
    ]












@get_all_router.get("/lawyers/verified")
def get_verified_lawyers(db: Session = Depends(get_db)):
    lawyers = (
        db.query(LawyerRegistration1)
        .options(
            joinedload(LawyerRegistration1.profile),
            joinedload(LawyerRegistration1.registration3),
            joinedload(LawyerRegistration1.registration4),
            joinedload(LawyerRegistration1.registration5),
            joinedload(LawyerRegistration1.registration6),
        )
        .filter(LawyerRegistration1.is_verified == True)
        .all()
    )

    if not lawyers:
        raise HTTPException(status_code=404, detail="No verified lawyers found")

    return [
        {
            "id": lawyer.id,
            "full_name": lawyer.full_name,
            "gender": lawyer.gender,
            "dob": lawyer.dob,
            "email": lawyer.email,
            "phone_number": lawyer.phone_number,
            "linkedin_url": lawyer.linkedin_url,
            "website_url": lawyer.website_url,
            "short_note": lawyer.short_note,
            "short_note" : lawyer.short_note,
            "photo": lawyer.photo,
            "is_verified": lawyer.is_verified,
            "rejection_reason": lawyer.rejection_reason,
            "created_datetime": lawyer.created_datetime,
            "updated_datetime": lawyer.updated_datetime,

            "profile": lawyer.profile and {
                "bio": lawyer.profile.bio,
                "years_of_experience": lawyer.profile.years_of_experience,
                "bar_details": lawyer.profile.bar_details,
                "languages_spoken": lawyer.profile.languages_spoken,
                "education": lawyer.profile.education,
            },

            "registration3": lawyer.registration3 and {
                "practice_area": lawyer.registration3.practice_area,
                "court_admitted_to": lawyer.registration3.court_admitted_to,
                "active_since": lawyer.registration3.active_since,
                "work_experience": lawyer.registration3.work_experience,
            },

            "registration4": lawyer.registration4 and {
                "office_image": lawyer.registration4.office_image,
                "case_results": lawyer.registration4.case_results,
            },

            "registration5": [
                {
                    "street_address": reg5.street_address,
                    "city": reg5.city,
                    "state": reg5.state,
                    "zip_code": reg5.zip_code,
                    "calendly_link": reg5.calendly_link,
                    "working_hours": reg5.working_hours,
                    "latitude":reg5.latitude,
                    "longitude":reg5.longitude,
                }
                for reg5 in lawyer.registration5
            ],

            "registration6": lawyer.registration6 and {
                "professional_associations": lawyer.registration6.professional_associations,
                "certifications": lawyer.registration6.certifications,
                "awards": lawyer.registration6.awards,
                "publications": lawyer.registration6.publications,
            }
        }
        for lawyer in lawyers
    ]















@get_all_router.get("/lawyers/unverified")
def get_unverified_lawyers(db: Session = Depends(get_db)):
    lawyers = (
        db.query(LawyerRegistration1)
        .options(
            joinedload(LawyerRegistration1.profile),
            joinedload(LawyerRegistration1.registration3),
            joinedload(LawyerRegistration1.registration4),
            joinedload(LawyerRegistration1.registration5),
            joinedload(LawyerRegistration1.registration6),
        )
        .filter(LawyerRegistration1.is_verified == False)
        .all()
    )

    if not lawyers:
        raise HTTPException(status_code=404, detail="No unverified lawyers found")

    return [
        {
            "id": lawyer.id,
            "full_name": lawyer.full_name,
            "gender": lawyer.gender,
            "dob": lawyer.dob,
            "email": lawyer.email,
            "phone_number": lawyer.phone_number,
            "linkedin_url": lawyer.linkedin_url,
            "website_url": lawyer.website_url,
            "short_note": lawyer.short_note,
            "photo": lawyer.photo,
            "is_verified": lawyer.is_verified,
            "rejection_reason": lawyer.rejection_reason,
            "created_datetime": lawyer.created_datetime,
            "updated_datetime": lawyer.updated_datetime,
            "profile": lawyer.profile and {
                "bio": lawyer.profile.bio,
                "years_of_experience": lawyer.profile.years_of_experience,
                "bar_details": lawyer.profile.bar_details,
                "languages_spoken": lawyer.profile.languages_spoken,
                "education": lawyer.profile.education,
            },

            "registration3": lawyer.registration3 and {
                "practice_area": lawyer.registration3.practice_area,
                "court_admitted_to": lawyer.registration3.court_admitted_to,
                "active_since": lawyer.registration3.active_since,
                "work_experience": lawyer.registration3.work_experience,
            },

            "registration4": lawyer.registration4 and {
                "office_image": lawyer.registration4.office_image,
                "case_results": lawyer.registration4.case_results,
            },

            "registration5": [
                {
                    "street_address": reg5.street_address,
                    "city": reg5.city,
                    "state": reg5.state,
                    "zip_code": reg5.zip_code,
                    "calendly_link": reg5.calendly_link,
                    "working_hours": reg5.working_hours,
                    "latitude":reg5.latitude,
                    "longitude":reg5.longitude,
                }
                for reg5 in lawyer.registration5
            ],

            "registration6": lawyer.registration6 and {
                "professional_associations": lawyer.registration6.professional_associations,
                "certifications": lawyer.registration6.certifications,
                "awards": lawyer.registration6.awards,
                "publications": lawyer.registration6.publications,
            }
        }
        for lawyer in lawyers
    ]









@get_all_router.get("/lawyers/rejected")
def get_rejected_lawyers(db: Session = Depends(get_db)):
    lawyers = (
        db.query(LawyerRegistration1)
        .options(
            joinedload(LawyerRegistration1.profile),
            joinedload(LawyerRegistration1.registration3),
            joinedload(LawyerRegistration1.registration4),
            joinedload(LawyerRegistration1.registration5),
            joinedload(LawyerRegistration1.registration6),
        )
        .filter(
            LawyerRegistration1.is_verified == False,
            LawyerRegistration1.rejection_reason.isnot(None),
            LawyerRegistration1.rejection_reason != ""   # ✅ exclude empty strings
        )
        .all()
    )

    if not lawyers:
        raise HTTPException(status_code=404, detail="No rejected lawyers found")

    return [
        {
            "id": lawyer.id,
            "full_name": lawyer.full_name,
            "gender": lawyer.gender,
            "dob": lawyer.dob,
            "email": lawyer.email,
            "phone_number": lawyer.phone_number,
            "linkedin_url": lawyer.linkedin_url,
            "website_url": lawyer.website_url,
            "short_note": lawyer.short_note,
            "photo": lawyer.photo,
            "is_verified": lawyer.is_verified,
            "rejection_reason": lawyer.rejection_reason,
            "created_datetime": lawyer.created_datetime,
            "updated_datetime": lawyer.updated_datetime,
            "profile": lawyer.profile and {
                "bio": lawyer.profile.bio,
                "years_of_experience": lawyer.profile.years_of_experience,
                "bar_details": lawyer.profile.bar_details,
                "languages_spoken": lawyer.profile.languages_spoken,
                "education": lawyer.profile.education,
            },

            "registration3": lawyer.registration3 and {
                "practice_area": lawyer.registration3.practice_area,
                "court_admitted_to": lawyer.registration3.court_admitted_to,
                "active_since": lawyer.registration3.active_since,
                "work_experience": lawyer.registration3.work_experience,
            },

            "registration4": lawyer.registration4 and {
                "office_image": lawyer.registration4.office_image,
                "case_results": lawyer.registration4.case_results,
            },

            "registration5": [
                {
                    "street_address": reg5.street_address,
                    "city": reg5.city,
                    "state": reg5.state,
                    "zip_code": reg5.zip_code,
                    "calendly_link": reg5.calendly_link,
                    "working_hours": reg5.working_hours,
                    "latitude":reg5.latitude,
                    "longitude":reg5.longitude,
                }
                for reg5 in lawyer.registration5
            ],

            "registration6": lawyer.registration6 and {
                "professional_associations": lawyer.registration6.professional_associations,
                "certifications": lawyer.registration6.certifications,
                "awards": lawyer.registration6.awards,
                "publications": lawyer.registration6.publications,
            }
        }
        for lawyer in lawyers
    ]




@get_all_router.get("/lawyers/search")
def search_lawyers(
    practice_area: Optional[str] = Query(None, description="Filter by practice area"),
    location: Optional[str] = Query(None, description="Filter by state or city"),
    db: Session = Depends(get_db)
):
    query = (
        db.query(LawyerRegistration1)
        .options(
            joinedload(LawyerRegistration1.profile),
            joinedload(LawyerRegistration1.registration3),
            joinedload(LawyerRegistration1.registration4),
            joinedload(LawyerRegistration1.registration5),
            joinedload(LawyerRegistration1.registration6),
        )
    )

    # Filter by practice area (registration3.practice_area contains CSV string)
    if practice_area:
        query = query.filter(LawyerRegistration1.registration3.has(
            LawyerRegistration1.registration3.property.mapper.class_.practice_area.ilike(f"%{practice_area}%")
        ))

    # Filter by location (state or city in registration5)
    if location:
        query = query.filter(
            LawyerRegistration1.registration5.any(
                (LawyerRegistration1.registration5.property.mapper.class_.state.ilike(f"%{location}%")) |
                (LawyerRegistration1.registration5.property.mapper.class_.city.ilike(f"%{location}%"))
            )
        )

    lawyers = query.all()

    if not lawyers:
        raise HTTPException(status_code=404, detail="No lawyers found")

    return [
        {
            "id": lawyer.id,
            "full_name": lawyer.full_name,
            "gender": lawyer.gender,
            "dob": lawyer.dob,
            "email": lawyer.email,
            "phone_number": lawyer.phone_number,
            "linkedin_url": lawyer.linkedin_url,
            "website_url": lawyer.website_url,
            "short_note": lawyer.short_note,
            "photo": lawyer.photo,
            "is_verified": lawyer.is_verified,
            "rejection_reason": lawyer.rejection_reason,
            "created_datetime": lawyer.created_datetime,
            "updated_datetime": lawyer.updated_datetime,

            "profile": lawyer.profile and {
                "bio": lawyer.profile.bio,
                "years_of_experience": lawyer.profile.years_of_experience,
                "bar_details": lawyer.profile.bar_details,
                "languages_spoken": lawyer.profile.languages_spoken,
                "education": lawyer.profile.education,
            },

            "registration3": lawyer.registration3 and {
                "practice_area": lawyer.registration3.practice_area,
                "court_admitted_to": lawyer.registration3.court_admitted_to,
                "active_since": lawyer.registration3.active_since,
                "work_experience": lawyer.registration3.work_experience,
            },

            "registration4": lawyer.registration4 and {
                "office_image": lawyer.registration4.office_image,
                "case_results": lawyer.registration4.case_results,
            },

            "registration5": [
                {
                    "street_address": reg5.street_address,
                    "city": reg5.city,
                    "state": reg5.state,
                    "zip_code": reg5.zip_code,
                    "calendly_link": reg5.calendly_link,
                    "working_hours": reg5.working_hours,
                    "latitude":reg5.latitude,
                    "longitude":reg5.longitude,
                }
                for reg5 in lawyer.registration5
            ],

            "registration6": lawyer.registration6 and {
                "professional_associations": lawyer.registration6.professional_associations,
                "certifications": lawyer.registration6.certifications,
                "awards": lawyer.registration6.awards,
                "publications": lawyer.registration6.publications,
            }
        }
        for lawyer in lawyers
    ]