from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Token, UserLogin, UserCreate, User as UserSchema
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), 
    user_in: UserLogin = None
) -> Any:
    """
    Get access token for login
    """
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserSchema)
def register(
    db: Session = Depends(get_db),
    user_in: UserCreate = None
) -> Any:
    """
    Create new user
    """
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )
    
    db_user = User(
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        name=user_in.name,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
