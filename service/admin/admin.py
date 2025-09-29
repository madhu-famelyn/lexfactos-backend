from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import uuid
import os
from dotenv import load_dotenv

from models.admin.admin import Admin
from schemas.admin.admin import AdminCreate, AdminResponse

# Load env variables
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------- Password & Auth Utils -------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------- Admin CRUD -------------------
def create_admin(db: Session, admin_data: AdminCreate) -> AdminResponse:
    # Check if email exists
    if db.query(Admin).filter(Admin.email == admin_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if mobile exists
    if db.query(Admin).filter(Admin.mobile_number == admin_data.mobile_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )

    new_admin = Admin(
        id=str(uuid.uuid4()),
        full_name=admin_data.full_name,
        email=admin_data.email,
        mobile_number=admin_data.mobile_number,
        hashed_password=get_password_hash(admin_data.password)
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return AdminResponse.from_orm(new_admin)


def authenticate_admin(db: Session, email: str, password: str) -> str:
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Return JWT token
    return create_access_token({"sub": admin.id})
