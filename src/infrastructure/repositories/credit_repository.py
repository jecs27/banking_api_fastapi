from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.models.credit import Credit, CreditStatus
from src.presentation.schemas.credit_schemas import CreditCreate, CreditUpdate

class CreditRepository:
    DEFAULT_ANNUAL_INTEREST_RATE = 12.0
    MONTHS_PER_YEAR = 12
    PERCENTAGE_DIVISOR = 100
    DECIMAL_PLACES = 2

    def __init__(self, db: Session):
        self.db = db

    def create(self, credit_data: CreditCreate, user_id: int) -> Credit:
        try:
            credit_dict = credit_data.model_dump()
            if credit_dict.get('interest_rate') is None:
                credit_dict['interest_rate'] = self.DEFAULT_ANNUAL_INTEREST_RATE
            if credit_dict.get('monthly_payment') is None:
                from decimal import Decimal
                amount = Decimal(str(credit_dict['amount']))
                interest_rate = Decimal(str(credit_dict['interest_rate']))
                term_months = credit_dict['term_months']
                
                # Calculate monthly payment using amortization formula
                monthly_rate = interest_rate / Decimal(str(self.MONTHS_PER_YEAR)) / Decimal(str(self.PERCENTAGE_DIVISOR))
                
                if monthly_rate == 0:
                    credit_dict['monthly_payment'] = amount / Decimal(term_months)
                else:
                    numerator = monthly_rate * (1 + monthly_rate) ** term_months
                    denominator = (1 + monthly_rate) ** term_months - 1
                    monthly_payment = amount * (numerator / denominator)
                    credit_dict['monthly_payment'] = Decimal(round(monthly_payment, self.DECIMAL_PLACES))
            if credit_dict.get('remaining_amount') is None:
                credit_dict['remaining_amount'] = credit_dict['amount']

            db_credit = Credit(
                user_id=user_id,
                **credit_dict
            )
            self.db.add(db_credit)
            self.db.commit()
            self.db.refresh(db_credit)
            return db_credit
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error creating credit: {str(e)}")

    def get_by_id(self, credit_id: int) -> Optional[Credit]:
        return self.db.query(Credit).filter(Credit.id == credit_id).first()

    def get_by_user_id(self, user_id: int) -> List[Credit]:
        return self.db.query(Credit).filter(Credit.user_id == user_id).all()

    def update(self, credit_id: int, credit_data: CreditUpdate) -> Optional[Credit]:
        db_credit = self.get_by_id(credit_id)
        if db_credit:
            for key, value in credit_data.model_dump(exclude_unset=True).items():
                setattr(db_credit, key, value)
            self.db.commit()
            self.db.refresh(db_credit)
        return db_credit

    def delete(self, credit_id: int) -> bool:
        db_credit = self.get_by_id(credit_id)
        if db_credit:
            self.db.delete(db_credit)
            self.db.commit()
            return True
        return False