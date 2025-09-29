from fastapi import APIRouter, Depends, UploadFile, File, Form,HTTPException
import json
from sqlalchemy.orm import Session
from config.db.session import get_db
from schemas.lawyer.registration4 import (
    LawyerRegistration4Create,
    LawyerRegistration4Update,
    LawyerRegistration4Out
)


from service.lawyer.registration4 import (
    create_lawyer_registration4,
    get_lawyer_registration4,
    get_lawyer_registration4_by_lawyer,
    get_all_lawyer_registration4,
    update_lawyer_registration4,
)

lawyer_registration4_router = APIRouter(
    prefix="/lawyers/registration4",
    tags=["Lawyer Registration 4"]
)


# ✅ Create LawyerRegistration4
@lawyer_registration4_router.post("/", response_model=LawyerRegistration4Out)
def create_lawyer4(
    lawyer_id: str = Form(...),
    case_results: str = Form(None), 
    office_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        # ✅ Build schema object
        lawyer_data = LawyerRegistration4Create(
            lawyer_id=lawyer_id,
            case_results=json.loads(case_results) if case_results else None
        )
        return create_lawyer_registration4(db, lawyer_data, office_image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ Get LawyerRegistration4 by record ID
@lawyer_registration4_router.get("/{lawyer4_id}", response_model=LawyerRegistration4Out)
def read_lawyer4(lawyer4_id: str, db: Session = Depends(get_db)):
    db_lawyer4 = get_lawyer_registration4  (db, lawyer4_id)
    if not db_lawyer4:
        raise HTTPException(status_code=404, detail="LawyerRegistration4 not found")
    return db_lawyer4


# ✅ Get LawyerRegistration4 by Lawyer ID
@lawyer_registration4_router.get("/by-lawyer/{lawyer_id}", response_model=LawyerRegistration4Out)
def read_lawyer4_by_lawyer(lawyer_id: str, db: Session = Depends(get_db)):
    db_lawyer4 = get_lawyer_registration4_by_lawyer(db, lawyer_id)
    if not db_lawyer4:
        raise HTTPException(status_code=404, detail="No registration4 found for this lawyer")
    return db_lawyer4


# ✅ Get all LawyerRegistration4
@lawyer_registration4_router.get("/", response_model=list[LawyerRegistration4Out])
def read_all_lawyers4(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_lawyer_registration4(db, skip=skip, limit=limit)


# ✅ Update LawyerRegistration4
@lawyer_registration4_router.put("/{lawyer4_id}", response_model=LawyerRegistration4Out)
def update_lawyer4(lawyer4_id: str, data: LawyerRegistration4Update, db: Session = Depends(get_db)):
    db_lawyer4 = update_lawyer_registration4(db, lawyer4_id, data)
    if not db_lawyer4:
        raise HTTPException(status_code=404, detail="LawyerRegistration4 not found")
    return db_lawyer4


