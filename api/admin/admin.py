from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from config.db.session import get_db

from schemas.admin.admin import AdminCreate, AdminResponse, TokenResponse
from service.admin.admin import create_admin, authenticate_admin

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ------------------- Admin Signup -------------------
@admin_router.post("/signup", response_model=AdminResponse)  # ✅ Use AdminResponse
def admin_signup(
    full_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    admin_data = AdminCreate(
        full_name=full_name,
        email=email,
        mobile_number=mobile_number,
        password=password
    )
    return create_admin(db, admin_data)


# ------------------- Admin Login -------------------
@admin_router.post("/login", response_model=TokenResponse)
def admin_login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Admin login to get JWT token
    """
    token = authenticate_admin(db, email, password)
    return {"access_token": token, "token_type": "bearer"}
