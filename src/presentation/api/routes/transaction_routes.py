from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from src.application.services.notification_service import NotificationService
from src.infrastructure.config.database import get_db
from src.application.services.transaction_service import TransactionService
from src.application.services.account_service import AccountService
from src.application.services.auth_service import AuthService
from src.infrastructure.models.notification import NotificationPriority, NotificationType
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.schemas.transaction_schemas import (
    DepositCreate,
    WithdrawalCreate, 
    TransferCreate,
    TransactionResponse
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/{account_id}/deposit", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_deposit(
    account_id: int,
    deposit_data: DepositCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    current_user = repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    return transaction_service.process_deposit(account_id, deposit_data)

@router.post("/{account_id}/withdrawal", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_withdrawal(
    account_id: int,
    withdrawal_data: WithdrawalCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    current_user = repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    transaction = transaction_service.process_withdrawal(account_id, withdrawal_data)
    notification_service = NotificationService(db)
    await notification_service.create_and_send_notification(
        user_id=current_user.id,
        type=NotificationType.TRANSACTION,
        title="Nueva transacción",
        content=f"Se ha realizado un retiro de <strong>${withdrawal_data.amount:.2f}</strong> desde su cuenta.<br><br>Si no reconoce esta transacción, por favor contáctenos inmediatamente.",
        priority=NotificationPriority.HIGH,
        email=current_user.email
    )
    return transaction

@router.post("/{account_id}/transfer", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(
    account_id: int,
    transfer_data: TransferCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    current_user = repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    source_account = account_service.get_account(account_id, current_user.id)
    if not source_account:
        raise HTTPException(status_code=404, detail="Source account not found")
        
    destination_account = account_service.get_account_by_number(transfer_data.destination_account_number)
    if not destination_account:
        raise HTTPException(status_code=404, detail="Destination account not found")
        
    if source_account.currency != destination_account.currency:
        raise HTTPException(
            status_code=400, 
            detail="Cannot transfer between accounts with different currencies"
        )
    
    transaction_service = TransactionService(db)
    return transaction_service.process_transfer(account_id, transfer_data)

@router.get("/{account_id}/history", response_model=List[TransactionResponse])
def get_transaction_history(
    account_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    current_user = repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_service = TransactionService(db)
    return transaction_service.get_transaction_history(account_id)