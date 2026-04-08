from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from ..db.session import Base

class ErrorLog(Base):
    __tablename__ = "error_logs"
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    static_report = Column(JSON)
    dynamic_output = Column(Text)
    predicted_label = Column(String(50))
