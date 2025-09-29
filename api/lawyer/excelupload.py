# upload_lawyers_excel.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from config.db.session import get_db
from models.lawyer.registration1 import LawyerRegistration1
from models.lawyer.registration2 import LawyerRegistration2
from models.lawyer.registration3 import LawyerRegistration3
from models.lawyer.registration4 import LawyerRegistration4
from models.lawyer.registration5 import LawyerRegistration5
from models.lawyer.registration6 import LawyerRegistration6

import pandas as pd
import uuid
from typing import Dict, Any

excel_router = APIRouter(prefix="/lawyers", tags=["Lawyers"])


@excel_router.post("/upload-excel/")
async def upload_lawyers_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a single Excel file containing lawyer data for tables LawyerRegistration1..6.
    Each row = one lawyer (all tables linked with code_id).
    """

    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")

    try:
        # Load Excel
        df = pd.read_excel(file.file)

        required_columns = [
            "code_id",
            # LawyerRegistration1
            "full_name", "gender", "dob", "email", "phone_number", "password", "linkedin_url",
            "website_url", "photo", "short_note",
            # LawyerRegistration2
            "bio", "years_of_experience", "bar_details", "languages_spoken", "education",
            # LawyerRegistration3
            "practice_area", "court_admitted_to", "active_since", "work_experience",
            # LawyerRegistration4
            "office_image", "case_results",
            # LawyerRegistration5
            "street_address", "city", "state", "zip_code", "latitude", "longitude",
            "calendly_link", "working_hours",
            # LawyerRegistration6
            "professional_associations", "certifications", "awards", "publications",
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required columns: {missing}")

        report = []

        for _, row in df.iterrows():
            code_id = str(row["code_id"]).strip()

            # ✅ Check if already exists in LawyerRegistration1
            reg1 = db.query(LawyerRegistration1).filter_by(code_id=code_id).first()

            if reg1:
                lawyer_id = reg1.id
                action = "updated"
            else:
                lawyer_id = str(uuid.uuid4())
                reg1 = LawyerRegistration1(
                    id=lawyer_id,
                    code_id=code_id,
                    full_name=row["full_name"],
                    gender=row.get("gender"),
                    dob=row.get("dob"),
                    email=row["email"],
                    phone_number=row["phone_number"],
                    hashed_password=row["password"],  # ⚠️ hash in real-world!
                    linkedin_url=row.get("linkedin_url"),
                    website_url=row.get("website_url"),
                    photo=row["photo"],
                    short_note=row["short_note"],
                )
                db.add(reg1)
                action = "inserted"

            # ✅ Registration2
            reg2 = db.query(LawyerRegistration2).filter_by(code_id=code_id).first()
            if not reg2:
                reg2 = LawyerRegistration2(code_id=code_id, lawyer_id=lawyer_id)
                db.add(reg2)
            reg2.bio = row["bio"]
            reg2.years_of_experience = row["years_of_experience"]
            reg2.bar_details = eval(row["bar_details"]) if row.get("bar_details") else {}
            reg2.languages_spoken = row["languages_spoken"]
            reg2.education = eval(row["education"]) if row.get("education") else []

            # ✅ Registration3
            reg3 = db.query(LawyerRegistration3).filter_by(code_id=code_id).first()
            if not reg3:
                reg3 = LawyerRegistration3(code_id=code_id, lawyer_id=lawyer_id)
                db.add(reg3)
            reg3.practice_area = row["practice_area"]
            reg3.court_admitted_to = row["court_admitted_to"]
            reg3.active_since = row["active_since"]
            reg3.work_experience = eval(row["work_experience"]) if row.get("work_experience") else []

            # ✅ Registration4
            reg4 = db.query(LawyerRegistration4).filter_by(code_id=code_id).first()
            if not reg4:
                reg4 = LawyerRegistration4(code_id=code_id, lawyer_id=lawyer_id)
                db.add(reg4)
            reg4.office_image = row["office_image"]
            reg4.case_results = eval(row["case_results"]) if row.get("case_results") else []

            # ✅ Registration5
            reg5 = db.query(LawyerRegistration5).filter_by(code_id=code_id).first()
            if not reg5:
                reg5 = LawyerRegistration5(code_id=code_id, lawyer_id=lawyer_id)
                db.add(reg5)
            reg5.street_address = row["street_address"]
            reg5.city = row["city"]
            reg5.state = row["state"]
            reg5.latitude = row["latitude"]
            reg5.longitude = row["longitude"]
            reg5.zip_code = row["zip_code"]
            reg5.calendly_link = row.get("calendly_link")
            reg5.working_hours = row.get("working_hours")

            # ✅ Registration6
            reg6 = db.query(LawyerRegistration6).filter_by(code_id=code_id).first()
            if not reg6:
                reg6 = LawyerRegistration6(code_id=code_id, lawyer_id=lawyer_id)
                db.add(reg6)
            reg6.professional_associations = row.get("professional_associations")
            reg6.certifications = eval(row["certifications"]) if row.get("certifications") else []
            reg6.awards = eval(row["awards"]) if row.get("awards") else []
            reg6.publications = eval(row["publications"]) if row.get("publications") else []

            db.commit()

            report.append({
                "code_id": code_id,
                "lawyer_id": lawyer_id,
                "status": "success",
                "action": action
            })

        return {"message": "Excel processed successfully", "report": report}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
