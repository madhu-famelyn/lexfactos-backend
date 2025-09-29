from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, text, func
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid


class LawyerRegistration5(Base):
    __tablename__ = "lawyerRegistration5"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    lawyer_id = Column(String, ForeignKey("lawyerRegistration1.id"), nullable=False, unique=True) 


    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    calendly_link = Column(String, nullable=True)  
    working_hours = Column(String, nullable=True)    
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

    lawyer = relationship("LawyerRegistration1", back_populates="registration5")
