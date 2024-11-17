from decimal import Decimal
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from infrastructure.repositories.credit_repository import CreditRepository
from infrastructure.models.credit import Credit, CreditStatus
from presentation.schemas.credit_schemas import CreditCreate, CreditUpdate

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

    def create_credit(self, credit_data: CreditCreate, user_id: int) -> Credit:
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
        credit_dict['interest_rate'] = interest_rate
        credit_dict['monthly_payment'] = monthly_payment
        credit_dict['remaining_amount'] = credit_data.amount
        
        return self.repository.create(CreditCreate(**credit_dict), user_id)

    def get_credit(self, credit_id: int, user_id: int) -> Credit:
        credit = self.repository.get_by_id(credit_id)
        if not credit:
            raise HTTPException(status_code=404, detail="Credit not found")
        if credit.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this credit")
        return credit

    def get_user_credits(self, user_id: int) -> List[Credit]:
        return self.repository.get_by_user_id(user_id)

    def update_credit_status(self, credit_id: int, user_id: int, status: CreditStatus) -> Credit:
        credit = self.get_credit(credit_id, user_id)
        update_data = CreditUpdate(status=status)
        return self.repository.update(credit_id, update_data)