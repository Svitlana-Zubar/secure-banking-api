from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserLogin
from app.security import verify_password, create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.email == user.email)
    )
    if not existing_user or not verify_password(
            password=user.password, hashed_password=existing_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(existing_user.id)

    return {"access_token": access_token,
            "token_type": "bearer"}