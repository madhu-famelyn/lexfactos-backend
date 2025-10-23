from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    Boolean,
    Date,
    ForeignKey,
    DateTime,
    func,
    TIMESTAMP,
    Enum,
)
from sqlalchemy.orm import relationship
from config.db.session import Base
from datetime import datetime
import uuid
import enum


class RatingEnum(str, enum.Enum):
    GOOD_FIT = "Good fit"
    MAYBE = "Maybe"
    NOT_A_FIT = "Not a fit"
    NOT_DECIDED = "Not decided"


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    job_id = Column(String, ForeignKey("job_posts.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    applicant_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile_number = Column(String, nullable=True)
    resume_url = Column(String, nullable=False)
    cover_letter = Column(String, nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow)

    rate = Column(Enum(RatingEnum, name="ratingenum"), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    job = relationship("JobPost", backref="applications")
    user = relationship("User", backref="job_applications")
