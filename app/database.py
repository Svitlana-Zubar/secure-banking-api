from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://svitlanazubar@localhost/secure_banking"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    blind=engine,
    autoflush=False,
    autocommint=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()