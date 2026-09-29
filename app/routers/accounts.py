from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import secrets

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import Account
from app.schemas import AccountResponse, AccountCreate

accounts_router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@accounts_router.get("/me", response_model=list[AccountResponse])
def get_my_accounts(
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    my_accounts = db.scalars(select(Account).where(Account.user_id == user_id)).all()
    return my_accounts

@accounts_router.post("/", response_model=AccountResponse, status_code=201)
def create_account(
        account: AccountCreate,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    for attempt in range(3):
        new_account = Account(
            user_id = user_id,
            account_number = generate_account_number(),
            sort_code="00-00-00",
            currency=account.currency
        )
        db.add(new_account)

        try:
            db.commit()
            db.refresh(new_account)
            return new_account
        except IntegrityError as error:
            db.rollback()
            sqlstate = getattr(error.orig, "sqlstate", None)
            constraint = getattr(
                getattr(error.orig, "diag", None),
                "constraint_name",
                None
            )
            if sqlstate == "23505" and constraint == "accounts_account_number_key":
                continue
            raise
    raise HTTPException(
        status_code=503,
        detail="Unable to generate a unique account number. Please try again."
    )

def generate_account_number() -> str:
    account_number = secrets.randbelow(100_000_000)
    return f"{account_number:08d}"