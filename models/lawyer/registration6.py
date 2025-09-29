from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, func, text, JSON
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid


class LawyerRegistration6(Base):
    __tablename__ = "lawyerRegistration6"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    lawyer_id = Column(String, ForeignKey("lawyerRegistration1.id"), nullable=False)

    professional_associations = Column(String, nullable=True)
    certifications = Column(JSON, nullable=True)
    awards = Column(JSON, nullable=True)
    publications = Column(JSON, nullable=True)
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

    # Relationship back to LawyerRegistration1
    lawyer = relationship("LawyerRegistration1", back_populates="registration6")
