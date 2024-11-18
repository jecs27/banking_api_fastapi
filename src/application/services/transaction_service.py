import uuid
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.repositories.transaction_repository import TransactionRepository
from src.infrastructure.repositories.account_repository import AccountRepository
from src.infrastructure.models.transaction import Transaction, TransactionStatus, TransactionType
from src.infrastructure.models.account import Account, AccountStatus
from src.presentation.schemas.transaction_schemas import DepositCreate, WithdrawalCreate, TransferCreate

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repository = TransactionRepository(db)
        self.account_repository = AccountRepository(db)

    def generate_reference_number(self) -> str:
        return f"TRX-{str(uuid.uuid4())[:8].upper()}"

    def validate_accounts(self, *accounts: Account) -> None:
        for account in accounts:
            if account.status != AccountStatus.ACTIVE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Account {account.account_number} is {account.status}."
                )

    def validate_sufficient_funds(self, account: Account, amount: Decimal) -> None:
        if account.balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient funds"
            )

    def process_deposit(self, account_id: int, deposit_data: DepositCreate) -> Transaction:
        account = self.account_repository.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        self.validate_accounts(account)
        
        transaction = self.transaction_repository.create(
            account_id=account_id,
            transaction_type=TransactionType.DEPOSIT,
            amount=deposit_data.amount,
            reference_number=self.generate_reference_number(),
            description=deposit_data.description
        )
        
        self.account_repository.update_balance(account_id, deposit_data.amount)
        
        self.transaction_repository.update_status(transaction.id, TransactionStatus.COMPLETED)
        
        return transaction

    def process_withdrawal(self, account_id: int, withdrawal_data: WithdrawalCreate) -> Transaction:
        account = self.account_repository.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        self.validate_accounts(account)
        self.validate_sufficient_funds(account, withdrawal_data.amount)
        
        transaction = self.transaction_repository.create(
            account_id=account_id,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=withdrawal_data.amount,
            reference_number=self.generate_reference_number(),
            description=withdrawal_data.description
        )
        
        self.account_repository.update_balance(account_id, -withdrawal_data.amount)
        
        self.transaction_repository.update_status(transaction.id, TransactionStatus.COMPLETED)
        
        return transaction

    def process_transfer(self, source_account_id: int, transfer_data: TransferCreate) -> Transaction:
        source_account = self.account_repository.get_by_id(source_account_id)
        destination_account = self.account_repository.get_by_account_number(
            transfer_data.destination_account_number
        )
        
        if not source_account or not destination_account:
            raise HTTPException(status_code=404, detail="One or both accounts not found")
        
        if source_account.id == destination_account.id:
            raise HTTPException(status_code=400, detail="Cannot transfer to the same account")
        
        self.validate_accounts(source_account, destination_account)
        self.validate_sufficient_funds(source_account, transfer_data.amount)
        
        transaction = self.transaction_repository.create(
            account_id=source_account_id,
            transaction_type=TransactionType.TRANSFER,
            amount=transfer_data.amount,
            reference_number=self.generate_reference_number(),
            destination_account_id=destination_account.id,
            description=transfer_data.description
        )
        
        self.account_repository.update_balance(source_account_id, -transfer_data.amount)
        self.account_repository.update_balance(destination_account.id, transfer_data.amount)
        
        self.transaction_repository.update_status(transaction.id, TransactionStatus.COMPLETED)
        
        return transaction

    def get_transaction_history(self, account_id: int) -> List[Transaction]:
        return self.transaction_repository.get_account_transactions(account_id)