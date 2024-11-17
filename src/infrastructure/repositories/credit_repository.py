from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.models.credit import Credit, CreditStatus
from src.presentation.schemas.credit_schemas import CreditCreate, CreditUpdate

class CreditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, credit_data: CreditCreate, user_id: int) -> Credit:
        db_credit = Credit(
            user_id=user_id,
            **credit_data.model_dump()
        )
        self.db.add(db_credit)
        self.db.commit()
        self.db.refresh(db_credit)
        return db_credit

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