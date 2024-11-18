from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from src.infrastructure.models.credit import CreditStatus

class CreditBase(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Loan amount requested")
    term_months: int = Field(..., gt=0, le=60, description="Loan term in months")
    purpose: str = Field(..., min_length=3, max_length=255)

class CreditCreate(CreditBase):
    pass

class CreditUpdate(BaseModel):
    status: Optional[CreditStatus]
    approved_at: Optional[datetime]
    interest_rate: Optional[Decimal] = Field(None, gt=0, le=100)

class CreditResponse(CreditBase):
    id: int
    user_id: int
    status: CreditStatus
    interest_rate: Decimal
    monthly_payment: Decimal
    created_at: datetime
    approved_at: Optional[datetime]
    next_payment_date: Optional[datetime]
    remaining_amount: Optional[Decimal]

    class Config:
        from_attributes = True