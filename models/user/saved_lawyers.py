from sqlalchemy import Column, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid


class SavedLawyer(Base):
    __tablename__ = "saved_lawyers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lawyer_id = Column(String, ForeignKey("lawyerRegistration1.id", ondelete="CASCADE"), nullable=False)

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



    user = relationship("User", back_populates="saved_lawyers")
    lawyer = relationship("LawyerRegistration1", back_populates="saved_by_users")

    __table_args__ = (UniqueConstraint("user_id", "lawyer_id", name="uq_user_lawyer"),)