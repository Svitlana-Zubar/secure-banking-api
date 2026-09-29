from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.security import hash_password, password_hash
from app.models import User

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

