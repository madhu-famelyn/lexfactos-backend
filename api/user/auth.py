from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db.session import get_db
from schemas.user.auth import LoginRequest, TokenResponse
from service.user.auth import authenticate_user
from service.user.google_auth import login_or_register_google_user
import logging

# ✅ Configure logger
logger = logging.getLogger("auth_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    User login with email & password
    """
    logger.info(f"Login attempt for email: {login_data.email}")

    try:
        response = authenticate_user(db, login_data)
        logger.info(f"Login successful for email: {login_data.email}")
        return response

    except Exception as e:
        logger.error(f"Login failed for {login_data.email}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")



# Google login endpoint
@auth_router.post("/google")
def google_login(credential: dict, db: Session = Depends(get_db)):
    """
    Login or register using Google ID token
    Frontend sends: { "credential": "<Google ID token>" }
    """
    token = credential.get("credential")
    if not token:
        raise HTTPException(status_code=400, detail="Missing Google credential")

    try:
        logger.info("Google login attempt")
        return login_or_register_google_user(db, token)
    except Exception as e:
        logger.error(f"Google login failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
