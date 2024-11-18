from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.application.services.auth_service import AuthService
from src.infrastructure.config.database import get_db
from src.application.services.credit_service import CreditService
from src.infrastructure.models.credit import CreditStatus
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.schemas.credit_schemas import CreditCreate, CreditResponse
from src.infrastructure.security import get_current_user
from src.infrastructure.models.user import User

router = APIRouter(tags=["credits"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=CreditResponse)
def create_credit(
    credit_data: CreditCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    credit_service = CreditService(db)
    return credit_service.create_credit(credit_data, user.id)

@router.get("/{credit_id}", response_model=CreditResponse)
def get_credit(
    credit_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    credit_service = CreditService(db)
    return credit_service.get_credit(credit_id, user.id)

@router.get("/", response_model=List[CreditResponse])
def get_user_credits(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    credit_service = CreditService(db)
    return credit_service.get_user_credits(user.id)

@router.patch("/{credit_id}/status", response_model=CreditResponse)
def update_credit_status(
    credit_id: int,
    status: CreditStatus,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    
    if not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update credit status"
        )
        
    credit_service = CreditService(db)
    return credit_service.update_credit_status(credit_id, user.id, status)