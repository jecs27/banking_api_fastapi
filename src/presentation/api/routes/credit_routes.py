from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.application.services.auth_service import AuthService
from src.infrastructure.config.database import get_db
from src.application.services.credit_service import CreditService
from src.infrastructure.models.credit import CreditStatus
from src.infrastructure.models.user import User, UserRole
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security import check_admin_role, get_current_user
from src.presentation.schemas.credit_schemas import CreditCreate, CreditResponse

router = APIRouter(tags=["credits"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=CreditResponse)
def create_credit(
    credit_data: CreditCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = UserRepository(db)
    check_admin_role(current_user)

    client = repo.get_by_id(credit_data.user_id)
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    credit_service = CreditService(db)
    return credit_service.create_credit(credit_data)

@router.get("/{credit_id}", response_model=CreditResponse)
def get_credit(
    credit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    credit_service = CreditService(db)
    return credit_service.get_credit(credit_id, current_user.id)

@router.get("/", response_model=List[CreditResponse])
def get_user_credits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    credit_service = CreditService(db)
    return credit_service.get_user_credits(current_user.id)

@router.patch("/{credit_id}/status", response_model=CreditResponse)
def update_credit_status(
    credit_id: int,
    status: CreditStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin_role(current_user)
    credit_service = CreditService(db)
    return credit_service.update_credit_status(credit_id, status)