from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Submission, ErrorLog
from app.schemas.code import SubmissionCreate, SubmissionResponse
from app.services.diagnosis_service import DiagnosisService
from app.config import settings

router = APIRouter()

@router.post("/submit", response_model=SubmissionResponse)
async def submit_code(
    submission: SubmissionCreate,
    diagnosis_service: DiagnosisService = Depends(DiagnosisService)
):
    """
    Submits code for diagnosis and execution.
    """
    # Run full diagnosis
    result = diagnosis_service.diagnose(submission.code, submission.test_code)
    
    # Return result to student
    return {
        "id": 1, # Mock ID for now
        "user_id": submission.user_id,
        "assignment_id": submission.assignment_id,
        "code": submission.code,
        "error_type": result["error_type"],
        "hint": result["hint"],
        "is_correct": result["is_correct"],
        "static_issues": result["static_issues"],
        "dynamic_output": result["dynamic_output"],
        "dynamic_error": result["dynamic_error"]
    }
