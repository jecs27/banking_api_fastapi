from datetime import datetime
import decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.infrastructure.models.account import Account, AccountStatus
from src.presentation.schemas.account_schemas import AccountCreate, AccountUpdate

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, account_data: AccountCreate, user_id: int, account_number: str) -> Account:
        db_account = Account(
            user_id=user_id,
            account_number=account_number,
            **account_data.model_dump()
        )
        try:
            self.db.add(db_account)
            self.db.commit()
            self.db.refresh(db_account)
            return db_account
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Account number already exists")

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_account_number(self, account_number: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.account_number == account_number).first()

    def get_by_user_id(self, user_id: int) -> List[Account]:
        return self.db.query(Account).filter(Account.user_id == user_id).all()

    def update(self, account_id: int, account_data: AccountUpdate) -> Optional[Account]:
        db_account = self.get_by_id(account_id)
        if db_account:
            for key, value in account_data.model_dump(exclude_unset=True).items():
                setattr(db_account, key, value)
            self.db.commit()
            self.db.refresh(db_account)
        return db_account

    def update_balance(self, account_id: int, amount: decimal.Decimal) -> Account:
        db_account = self.get_by_id(account_id)
        if db_account:
            db_account.balance += amount
            db_account.last_transaction_date = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_account)
            return db_account
        raise HTTPException(status_code=404, detail="Account not found")