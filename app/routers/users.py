from fastapi import APIRouter, Depends
from app.schemas import UserCreate
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/users")

@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user.email

