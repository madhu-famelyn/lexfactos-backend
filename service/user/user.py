from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from passlib.context import CryptContext
import uuid
from models.user.user import User
from schemas.user.user import UserCreate, UserResponse
from service.s3_service import upload_to_s3

# ✅ Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Safely hash the plain password.
    bcrypt only supports up to 72 bytes; truncate longer ones to avoid errors.
    """
    if len(password.encode("utf-8")) > 72:
        password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(password)


def create_user(db: Session, user_data: UserCreate, photo: UploadFile | None) -> UserResponse:
    """Create a new user with hashed password and uploaded photo."""

    # ✅ Check if email exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # ✅ Check if mobile exists
    existing_mobile = db.query(User).filter(User.mobile_number == user_data.mobile_number).first()
    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered",
        )

    # ✅ Upload photo to S3 (if provided)
    photo_url = None
    if photo:
        try:
            photo_url = upload_to_s3(photo, folder="users")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Photo upload failed: {str(e)}",
            )

    # ✅ Create User object
    new_user = User(
        id=str(uuid.uuid4()),
        full_name=user_data.full_name,
        email=user_data.email,
        mobile_number=user_data.mobile_number,
        hashed_password=get_password_hash(user_data.password),
        photo=photo_url,
    )

    # ✅ Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)
