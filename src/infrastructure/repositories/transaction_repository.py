from decimal import Decimal
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.infrastructure.models.transaction import Transaction, TransactionStatus, TransactionType
from src.infrastructure.models.account import Account, AccountStatus

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, 
               account_id: int, 
               transaction_type: TransactionType,
               amount: Decimal,
               reference_number: str,
               destination_account_id: Optional[int] = None,
               description: Optional[str] = None) -> Transaction:
        try:
            transaction = Transaction(
                account_id=account_id,
                transaction_type=transaction_type,
                amount=amount,
                reference_number=reference_number,
                destination_account_id=destination_account_id,
                description=description
            )
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Transaction reference number already exists")

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_by_reference(self, reference_number: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.reference_number == reference_number).first()

    def get_account_transactions(self, account_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter(
            (Transaction.account_id == account_id) | 
            (Transaction.destination_account_id == account_id)
        ).order_by(Transaction.created_at.desc()).all()

    def update_status(self, transaction_id: int, status: TransactionStatus) -> Transaction:
        transaction = self.get_by_id(transaction_id)
        if transaction:
            transaction.status = status
            transaction.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        raise HTTPException(status_code=404, detail="Transaction not found")