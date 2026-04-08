from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.submission import Submission
from app.models.error_log import ErrorLog
from app.schemas.code import SubmissionCreate, SubmissionResponse
from app.services.diagnosis_service import DiagnosisService
from app.config import settings

router = APIRouter()

@router.post("/submit", response_model=SubmissionResponse)
async def submit_code(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    diagnosis_service: DiagnosisService = Depends(DiagnosisService)
):
    """
    Submits code for diagnosis and execution.
    """
    # Run full diagnosis
    result = diagnosis_service.diagnose(submission.code, submission.test_code)
    
    # Save submission to database
    db_submission = Submission(
        user_id=submission.user_id,
        assignment_id=submission.assignment_id,
        code=submission.code,
        error_type=result["error_type"],
        hint=result["hint"],
        is_correct=result["is_correct"]
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Save error log for ML/Diagnosis refinement
    error_log = ErrorLog(
        submission_id=db_submission.id,
        static_report={"issues": result["static_issues"]},
        dynamic_output=result["dynamic_output"],
        predicted_label=result["error_type"]
    )
    db.add(error_log)
    db.commit()
    
    # Return result to student
    return {
        "id": db_submission.id,
        "user_id": db_submission.user_id,
        "assignment_id": db_submission.assignment_id,
        "code": db_submission.code,
        "error_type": db_submission.error_type,
        "hint": db_submission.hint,
        "is_correct": db_submission.is_correct,
        "static_issues": result["static_issues"],
        "dynamic_output": result["dynamic_output"],
        "dynamic_error": result["dynamic_error"]
    }
