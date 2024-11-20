from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from src.infrastructure.config.database import get_db
from src.application.services.account_service import AccountService
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security import check_admin_role, get_current_user
from src.presentation.schemas.account_schemas import (
    AccountCreate,
    AccountResponse,
    AccountBalance,
)
from src.infrastructure.models.account import AccountStatus
from src.infrastructure.models.user import User, UserRole

router = APIRouter(tags=["accounts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    check_admin_role(current_user)

    userClient = user_repo.get_by_email(email=account_data.email)
    if not userClient:
        raise HTTPException(status_code=404, detail="Client not found")

    account_service = AccountService(db)
    return account_service.create_account(account_data, userClient.id)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    return account_service.get_account(account_id, current_user.id)

@router.get("/", response_model=List[AccountResponse])
def get_user_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    account_service = AccountService(db)
    return account_service.get_user_accounts(current_user.id)

@router.patch("/{account_id}/status", response_model=AccountResponse)
def update_account_status(
    account_id: int,
    status: AccountStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    check_admin_role(current_user)
    account_service = AccountService(db)
    return account_service.update_account_status(account_id, current_user.id, status)

@router.get("/{account_id}/balance", response_model=AccountBalance)
def get_account_balance(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    return AccountBalance(balance=account.balance, currency=account.currency)

@router.get("/all", response_model=List[AccountResponse])
def get_all_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    check_admin_role(current_user)

    account_service = AccountService(db)
    return account_service.get_all_accounts()