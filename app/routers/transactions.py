from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import Account, Transaction
from app.schemas import TransactionCreate, TransactionResponse, TransactionType

transactions_router = APIRouter(
    prefix="/accounts",
    tags=["Transactions"]
)

@transactions_router.post(
    "/{account_id}/transactions",
    response_model=TransactionResponse,
    status_code=201)
def create_transaction(
        account_id: int,
        transaction: TransactionCreate,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)
):
    account = db.scalar(select(Account).where(
        Account.id == account_id, Account.user_id == user_id).with_for_update())
    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    if transaction.type == TransactionType.deposit:
        account.balance += transaction.amount
    elif transaction.type == TransactionType.withdrawal:
        if transaction.amount > account.balance:
            raise HTTPException(
                status_code=400,
                detail="Insufficient balance"
            )

        account.balance -= transaction.amount

    new_transaction = Transaction(account_id=account.id,
                                  type=transaction.type.value,
                                  amount=transaction.amount,
                                  currency=account.currency,
                                  description=transaction.description)

    db.add(new_transaction)
    try:
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
    except Exception:
        db.rollback()
        raise

@transactions_router.get(
    "/{account_id}/transactions",
    status_code=200,
    response_model=list[TransactionResponse])
def return_list_of_transactions(
        account_id: int,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    account = db.scalar(select(Account).where(
        Account.id == account_id, Account.user_id == user_id))

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    transactions = db.scalars(select(Transaction).where(
        Transaction.account_id == account_id).order_by(
        Transaction.created_at.desc())).all()
    return transactions

