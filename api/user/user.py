from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.orm import Session
from config.db.session import get_db

from schemas.user.user import UserCreate, UserResponse
from service.user.user import create_user



user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/signup", response_model=UserResponse)
async def signup_user(
    full_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Signup user with photo upload (stored on S3)
    """

    # ✅ Build a Pydantic model instead of dict
    user_data = UserCreate(
        full_name=full_name,
        email=email,
        mobile_number=mobile_number,
        password=password,
        photo=None  # will be set inside service after upload
    )

    return create_user(db, user_data, photo)


