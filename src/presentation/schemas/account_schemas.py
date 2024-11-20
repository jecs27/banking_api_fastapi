from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, validator
from src.infrastructure.models.account import AccountType, AccountStatus
from enum import Enum

class Currency(str, Enum):
    # Mexican Peso
    MXN = "MXN"
    # United States Dollar
    USD = "USD" 
    # Euro
    EUR = "EUR"
    # British Pound Sterling
    GBP = "GBP"
    # Japanese Yen
    JPY = "JPY"
    # Canadian Dollar
    CAD = "CAD"

class AccountBase(BaseModel):
    account_type: AccountType
    currency: Currency = Field(default=Currency.MXN)

    @validator('currency')
    def validate_currency(cls, v):
        if v not in Currency:
            raise ValueError('Invalid currency')
        return v

class AccountCreate(AccountBase):
    email: str
    pass

class AccountUpdate(BaseModel):
    status: Optional[AccountStatus]

class AccountResponse(BaseModel):
    id: int
    balance: float
    currency: str
    status: AccountStatus
    created_at: datetime
    last_transaction_date: Optional[datetime]

    class Config:
        from_attributes = True

class AccountBalance(BaseModel):
    balance: Decimal = Field(..., ge=0)
    currency: Currency = Field(..., min_length=3, max_length=3)