from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, func, ForeignKey, text
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid

class LawyerRegistration2(Base):
    __tablename__ = "lawyerRegistration2"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    lawyer_id = Column(String, ForeignKey("lawyerRegistration1.id"), nullable=False, unique=True)
    bio = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    bar_details = Column(JSON, nullable=False) 
    languages_spoken = Column(String, nullable=False)
    education = Column(JSON, nullable=False)
    code_id = Column(String, unique=True, index=True, nullable=False)

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

    lawyer = relationship("LawyerRegistration1", back_populates="profile")
