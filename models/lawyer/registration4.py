from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, JSON, text, func
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid


class LawyerRegistration4(Base):
    __tablename__ = "lawyerRegistration4"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    lawyer_id = Column(String, ForeignKey("lawyerRegistration1.id"), nullable=False, unique=True)

    office_image = Column(String, nullable=False) 
    case_results = Column(JSON, nullable=True) 
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

    lawyer = relationship("LawyerRegistration1", back_populates="registration4")
