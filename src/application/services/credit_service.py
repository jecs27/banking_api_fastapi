from decimal import Decimal
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.infrastructure.repositories.credit_repository import CreditRepository
from src.infrastructure.models.credit import Credit, CreditStatus
from src.presentation.schemas.credit_schemas import CreditCreate, CreditUpdate

class CreditService:
    def __init__(self, db: Session):
        self.repository = CreditRepository(db)

    def calculate_monthly_payment(self, amount: Decimal, annual_interest_rate: Decimal, term_months: int) -> Decimal:
        """Calculate monthly payment using amortization formula"""
        monthly_rate = annual_interest_rate / Decimal(12) / Decimal(100)
        
        if monthly_rate == 0:
            return amount / Decimal(term_months)
            
        numerator = monthly_rate * (1 + monthly_rate) ** term_months
        denominator = (1 + monthly_rate) ** term_months - 1
        
        monthly_payment = amount * (numerator / denominator)
        return Decimal(round(monthly_payment, 2))

    def create_credit(self, credit_data: CreditCreate) -> Credit:
        # Set default interest rate (this could be based on credit score in the future)
        interest_rate = Decimal('12.0')  # 12% annual interest rate
        
        # Calculate monthly payment
        monthly_payment = self.calculate_monthly_payment(
            credit_data.amount,
            interest_rate,
            credit_data.term_months
        )
        # Add calculated fields to credit data
        credit_dict = credit_data.model_dump()
        credit_dict['interest_rate'] = credit_dict.get('interest_rate', interest_rate)
        credit_dict['monthly_payment'] = credit_dict.get('monthly_payment', monthly_payment)
        credit_dict['remaining_amount'] = credit_dict.get('remaining_amount', credit_data.amount)

        return self.repository.create(CreditCreate(**credit_dict))

    def get_credit(self, credit_id: int, user_id: int) -> Credit:
        credit = self.repository.get_by_id(credit_id)
        if not credit:
            raise HTTPException(status_code=404, detail="Credit not found")
        if credit.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this credit")
        return credit

    def get_credit_by_admin(self, credit_id: int) -> Credit:
        credit = self.repository.get_by_id(credit_id)
        if not credit:
            raise HTTPException(status_code=404, detail="Credit not found")
        return credit

    def get_user_credits(self, user_id: int) -> List[Credit]:
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repository.get_by_user_id(user_id)

    def update_credit_status(self, credit_id: int, status: CreditStatus) -> Credit:
        credit = self.repository.get_by_id(credit_id)
        if not credit:
            raise HTTPException(status_code=404, detail="Credit not found")
            
        if credit.status in [CreditStatus.REJECTED, CreditStatus.APPROVED]:
            raise HTTPException(
                status_code=400,
                detail="Cannot modify a credit application that has been approved or rejected"
            )

        update_data = {
            "status": status,
            "approved_at": datetime.now() if status == CreditStatus.APPROVED else None
        }
        return self.repository.update(credit_id, CreditUpdate(**update_data))