from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from decimal import Decimal
from enum import Enum


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class AccountCreate(BaseModel):
    pass

class AccountResponse(BaseModel):
    id: int
    user_id: int
    account_number: str
    sort_code: str
    balance: Decimal
    currency: str
    created_at: datetime

class TransactionType(Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"

class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Decimal = Field(gt=0)
    currency: str
    description: str

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    type: TransactionType
    amount: Decimal
    currency: str
    description: str
    created_at: datetime
