from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from ..db.session import Base

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    code = Column(Text)
    error_type = Column(String(50))
    hint = Column(Text)
    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
