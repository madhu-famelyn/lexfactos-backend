from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
from models.user.user import User
from service.user.auth import create_access_token
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def login_or_register_google_user(db: Session, token: str):
    """
    Verify Google ID token, create user if not exists, return JWT
    """
    if not GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID is not set in environment variables")

    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo.get("email")
        full_name = idinfo.get("name")
        picture = idinfo.get("picture")

        if not email:
            raise ValueError("Email not found in Google token")

        # Check if user exists
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # Create new Google user
            user = User(
                id=str(uuid.uuid4()),
                full_name=full_name,
                email=email,
                photo=picture,
                auth_provider="google"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Issue JWT token (reuse your normal JWT function)
        access_token = create_access_token({"sub": user.id})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise e
