from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    name = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    test_code = Column(Text)  # pytest code
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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

class ErrorLog(Base):
    __tablename__ = "error_logs"
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    static_report = Column(JSON)
    dynamic_output = Column(Text)
    predicted_label = Column(String(50))
