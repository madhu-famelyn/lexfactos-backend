from sqlalchemy import Column, String, Boolean, TIMESTAMP, func, text
from config.db.session import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    full_name = Column(String, nullable=True)   # Google may give only name
    email = Column(String, unique=True, index=True, nullable=False)
    mobile_number = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)  # nullable for Google users
    photo = Column(String, nullable=True) 

    auth_provider = Column(String, default="email")  # "email" or "google"

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
