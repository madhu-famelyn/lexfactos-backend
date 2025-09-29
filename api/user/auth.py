from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db.session import get_db

from schemas.user.auth import LoginRequest, TokenResponse
from service.user.auth import authenticate_user
from service.user.google_auth import login_or_register_google_user


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    User login with email & password
    """
    return authenticate_user(db, login_data)







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
        return login_or_register_google_user(db, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))