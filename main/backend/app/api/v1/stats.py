from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.submission import Submission
from app.models.user import User, UserRole
from app.models.assignment import Assignment
from app.schemas.stats import OverallStats, ErrorDistribution

router = APIRouter()

@router.get("/overall", response_model=OverallStats)
def get_overall_stats(db: Session = Depends(get_db)) -> Any:
    """
    Get overall system stats for teachers.
    """
    total_students = db.query(User).filter(User.role == UserRole.STUDENT).count()
    total_assignments = db.query(Assignment).count()
    total_submissions = db.query(Submission).count()
    
    # Error distribution
    error_counts = db.query(
        Submission.error_type, func.count(Submission.id)
    ).group_by(Submission.error_type).all()
    
    error_dist = [
        ErrorDistribution(error_type=row[0] if row[0] else "Unknown", count=row[1]) 
        for row in error_counts
    ]
    
    # Average correct rate
    correct_submissions = db.query(Submission).filter(Submission.is_correct == True).count()
    average_correct_rate = (correct_submissions / total_submissions) if total_submissions > 0 else 0.0
    
    return {
        "total_students": total_students,
        "total_assignments": total_assignments,
        "total_submissions": total_submissions,
        "average_correct_rate": average_correct_rate,
        "error_distribution": error_dist
    }

@router.get("/student/{student_id}")
def get_student_stats(student_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Get stats for a specific student.
    """
    student = db.query(User).filter(User.id == student_id, User.role == UserRole.STUDENT).first()
    if not student:
        return {"error": "Student not found"}
        
    submissions = db.query(Submission).filter(Submission.user_id == student_id).all()
    total = len(submissions)
    correct = len([s for s in submissions if s.is_correct])
    
    return {
        "student_name": student.name or student.username,
        "total_submissions": total,
        "correct_submissions": correct,
        "completion_rate": (correct / total) if total > 0 else 0.0,
        "submissions": submissions
    }
