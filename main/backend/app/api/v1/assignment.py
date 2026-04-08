from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, Assignment as AssignmentSchema

router = APIRouter()

@router.get("/", response_model=List[AssignmentSchema])
def read_assignments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve assignments.
    """
    assignments = db.query(Assignment).offset(skip).limit(limit).all()
    return assignments

@router.post("/", response_model=AssignmentSchema)
def create_assignment(
    *,
    db: Session = Depends(get_db),
    assignment_in: AssignmentCreate
) -> Any:
    """
    Create new assignment.
    """
    assignment = Assignment(
        title=assignment_in.title,
        description=assignment_in.description,
        test_code=assignment_in.test_code
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("/{id}", response_model=AssignmentSchema)
def read_assignment(
    *,
    db: Session = Depends(get_db),
    id: int
) -> Any:
    """
    Get assignment by ID.
    """
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/{id}", response_model=AssignmentSchema)
def update_assignment(
    *,
    db: Session = Depends(get_db),
    id: int,
    assignment_in: AssignmentUpdate
) -> Any:
    """
    Update an assignment.
    """
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    update_data = assignment_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(assignment, field, update_data[field])
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{id}", response_model=AssignmentSchema)
def delete_assignment(
    *,
    db: Session = Depends(get_db),
    id: int
) -> Any:
    """
    Delete an assignment.
    """
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return assignment
