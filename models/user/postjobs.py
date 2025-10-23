from sqlalchemy import Column, String, Integer, Float, Text, Boolean, Date, ForeignKey, DateTime, func, TIMESTAMP
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid
from sqlalchemy.sql import func


class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    jobTitle = Column(String, nullable=False)
    jobType = Column(String, nullable=False)
    practiceArea = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    experienceLevel = Column(String, nullable=True)
    jobDescription = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    workMode = Column(String, nullable=True)
    contactInfo = Column(String, nullable=True)

    status = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="job_posts")
