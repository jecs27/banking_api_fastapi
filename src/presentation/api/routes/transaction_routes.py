from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.config.database import get_db
from src.application.services.transaction_service import TransactionService
from src.application.services.account_service import AccountService
from src.presentation.schemas.transaction_schemas import (
    DepositCreate,
    WithdrawalCreate,
    TransferCreate,
    TransactionResponse
)
from src.infrastructure.security import get_current_user
from src.infrastructure.models.user import User

router = APIRouter(tags=["transactions"])

@router.post("/{account_id}/deposit", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_deposit(
    account_id: int,
    deposit_data: DepositCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    return transaction_service.process_deposit(account_id, deposit_data)

@router.post("/{account_id}/withdrawal", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_withdrawal(
    account_id: int,
    withdrawal_data: WithdrawalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    return transaction_service.process_withdrawal(account_id, withdrawal_data)

@router.post("/{account_id}/transfer", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(
    account_id: int,
    transfer_data: TransferCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    return transaction_service.process_transfer(account_id, transfer_data)

@router.get("/{account_id}/history", response_model=List[TransactionResponse])
def get_transaction_history(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    return transaction_service.get_transaction_history(account_id)