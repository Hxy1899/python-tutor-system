from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SubmissionCreate(BaseModel):
    user_id: int
    assignment_id: int
    code: str
    test_code: Optional[str] = ""

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    assignment_id: int
    code: str
    error_type: str
    hint: str
    is_correct: bool
    static_issues: Optional[List[Dict[str, Any]]] = []
    dynamic_output: Optional[str] = ""
    dynamic_error: Optional[str] = ""
