from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from passlib.context import CryptContext
import uuid
from models.user.user import User
from schemas.user.user import UserCreate, UserResponse
from service.s3_service import upload_to_s3

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash plain password"""
    return pwd_context.hash(password)


def create_user(db: Session, user_data: UserCreate, photo: UploadFile) -> UserResponse:
    # ✅ Check if email exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # ✅ Check if mobile exists
    existing_mobile = db.query(User).filter(User.mobile_number == user_data.mobile_number).first()
    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )

    # ✅ Upload photo to S3
    photo_url = None
    if photo:
        photo_url = upload_to_s3(photo, folder="users")

    # ✅ Create User object
    new_user = User(
        id=str(uuid.uuid4()),
        full_name=user_data.full_name,
        email=user_data.email,
        mobile_number=user_data.mobile_number,
        hashed_password=get_password_hash(user_data.password),
        photo=photo_url
    )

    # ✅ Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)
