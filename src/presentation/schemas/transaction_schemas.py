from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from src.infrastructure.models.transaction import TransactionType, TransactionStatus

class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Transaction amount")
    description: Optional[str] = Field(None, max_length=255)

class DepositCreate(TransactionBase):
    pass

class WithdrawalCreate(TransactionBase):
    pass

class TransferCreate(TransactionBase):
    destination_account_number: str = Field(..., min_length=12, max_length=12)

class TransactionResponse(TransactionBase):
    id: int
    transaction_type: TransactionType
    status: TransactionStatus
    reference_number: str
    account_id: int
    destination_account_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True