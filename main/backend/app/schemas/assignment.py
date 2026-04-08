from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    test_code: Optional[str] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(AssignmentBase):
    title: Optional[str] = None

class AssignmentInDBBase(AssignmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Assignment(AssignmentInDBBase):
    pass
