from sqlalchemy import Column, String, Date, func, TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid

class LawyerRegistration1(Base):
    __tablename__ = "lawyerRegistration1"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    linkedin_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    photo = Column(String, nullable=False) 
    short_note = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))
    code_id = Column(String, unique=True, index=True, nullable=False)


    rejection_reason = Column(String, nullable=True)  

    created_datetime = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_datetime = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    profile = relationship("LawyerRegistration2", back_populates="lawyer", uselist=False)
    registration3 = relationship("LawyerRegistration3", back_populates="lawyer", uselist=False)
    registration4 = relationship("LawyerRegistration4", back_populates="lawyer", uselist=False)
    registration5 = relationship("LawyerRegistration5", back_populates="lawyer")
    registration6 = relationship("LawyerRegistration6", back_populates="lawyer", uselist=False)
