import random
import string
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.repositories.account_repository import AccountRepository
from src.infrastructure.models.account import Account, AccountStatus
from src.presentation.schemas.account_schemas import AccountCreate, AccountUpdate

class AccountService:
    def __init__(self, db: Session):
        self.repository = AccountRepository(db)

    def generate_account_number(self) -> str:
        """Generate a unique 12-digit account number"""
        while True:
            account_number = ''.join(random.choices(string.digits, k=12))
            if not self.repository.get_by_account_number(account_number):
                return account_number

    def create_account(self, account_data: AccountCreate, user_id: int) -> Account:
        account_number = self.generate_account_number()
        return self.repository.create(account_data, user_id, account_number)

    def get_account(self, account_id: int, user_id: int) -> Account:
        account = self.repository.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this account")
        return account

    def get_user_accounts(self, user_id: int) -> List[Account]:
        return self.repository.get_by_user_id(user_id)

    def update_account_status(self, account_id: int, user_id: int, status: AccountStatus) -> Account:
        account = self.get_account(account_id, user_id)
        update_data = AccountUpdate(status=status)
        return self.repository.update(account_id, update_data)

    def check_balance(self, account_id: int, user_id: int) -> Decimal:
        account = self.get_account(account_id, user_id)
        return account.balance

    def validate_account_status(self, account: Account) -> None:
        if account.status != AccountStatus.ACTIVE:
            raise HTTPException(
                status_code=400,
                detail=f"Account is {account.status}. Only ACTIVE accounts can perform transactions"
            )