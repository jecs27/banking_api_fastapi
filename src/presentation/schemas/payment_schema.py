from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED" 
    FAILED = "FAILED"
    REVERSED = "REVERSED"
    OVERDUE = "OVERDUE"

class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime
    credit_id: int

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    status: Optional[PaymentStatus] = None

class PaymentInDB(PaymentBase):
    id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    transaction_id: Optional[int] = None

    class Config:
        orm_mode = True

class Payment(PaymentInDB):
    pass
