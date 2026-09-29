from alembic.util import status
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.security import hash_password
from app.models import User
from app.dependencies import get_current_user_id

users_router = APIRouter(prefix="/users")

@users_router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(select(User).where(User.email == user.email))
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)
    new_user = User(password_hash=hashed_password, first_name = user.first_name, last_name = user.last_name, email = user.email)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered."
        )
    db.refresh(new_user)
    return new_user

@users_router.get("/me", response_model=UserResponse)
def get_me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
