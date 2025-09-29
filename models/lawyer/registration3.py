from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, JSON, Text, text, func
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid


class LawyerRegistration3(Base):
    __tablename__ = "lawyerRegistration3"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    lawyer_id = Column(String, ForeignKey("lawyerRegistration1.id"), nullable=False, unique=True)

    practice_area = Column(String, nullable=False)
    court_admitted_to = Column(String, nullable=False)
    active_since = Column(Integer, nullable=False)
    work_experience = Column(
        JSON,
        nullable=False
    )  
    code_id = Column(String, unique=True, index=True, nullable=False)
 # Example: {"total_years": 10, "previous_firms": ["Firm A", "Firm B"]}


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

    lawyer = relationship("LawyerRegistration1", back_populates="registration3")
