from pydantic import BaseModel
from typing import Dict, List, Any

class ErrorDistribution(BaseModel):
    error_type: str
    count: int

class StudentProgress(BaseModel):
    student_name: str
    total_submissions: int
    correct_submissions: int
    completion_rate: float

class OverallStats(BaseModel):
    total_students: int
    total_assignments: int
    total_submissions: int
    average_correct_rate: float
    error_distribution: List[ErrorDistribution]
