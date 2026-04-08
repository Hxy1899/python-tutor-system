from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..db.session import Base

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    test_code = Column(Text)  # pytest code
    created_at = Column(DateTime(timezone=True), server_default=func.now())
