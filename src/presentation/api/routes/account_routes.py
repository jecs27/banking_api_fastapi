from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from src.infrastructure.config.database import get_db
from src.application.services.account_service import AccountService
from src.application.services.auth_service import AuthService
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.schemas.account_schemas import (
    AccountCreate,
    AccountResponse,
    AccountBalance,
)
from src.infrastructure.models.account import AccountStatus
from src.infrastructure.models.user import User

router = APIRouter(tags=["accounts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: AccountCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    token_data = auth_service.verify_token(token)
    current_user = user_repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    account_service = AccountService(db)
    return account_service.create_account(account_data, current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    token_data = auth_service.verify_token(token)
    current_user = user_repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    return account_service.get_account(account_id, current_user.id)

@router.get("/", response_model=List[AccountResponse])
def get_user_accounts(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    token_data = auth_service.verify_token(token)
    current_user = user_repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    return account_service.get_user_accounts(current_user.id)

@router.patch("/{account_id}/status", response_model=AccountResponse)
def update_account_status(
    account_id: int,
    status: AccountStatus,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    token_data = auth_service.verify_token(token)
    current_user = user_repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    return account_service.update_account_status(account_id, current_user.id, status)

@router.get("/{account_id}/balance", response_model=AccountBalance)
def get_account_balance(
    account_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    token_data = auth_service.verify_token(token)
    current_user = user_repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    account_service = AccountService(db)
    account = account_service.get_account(account_id, current_user.id)
    return AccountBalance(balance=account.balance, currency=account.currency)