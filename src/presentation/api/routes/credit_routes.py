from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.config.database import get_db
from src.application.services.credit_service import CreditService
from src.presentation.schemas.credit_schemas import CreditCreate, CreditResponse
from src.infrastructure.security import get_current_user
from src.infrastructure.models.user import User

router = APIRouter(prefix="/credits", tags=["credits"])

@router.post("/", response_model=CreditResponse)
def create_credit(
    credit_data: CreditCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    credit_service = CreditService(db)
    return credit_service.create_credit(credit_data, current_user.id)

@router.get("/{credit_id}", response_model=CreditResponse)
def get_credit(
    credit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    credit_service = CreditService(db)
    return credit_service.get_credit(credit_id, current_user.id)

@router.get("/", response_model=List[CreditResponse])
def get_user_credits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    credit_service = CreditService(db)
    return credit_service.get_user_credits(current_user.id)

@router.patch("/{credit_id}/status", response_model=CreditResponse)
def update_credit_status(
    credit_id: int,
    status: CreditStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    credit_service = CreditService(db)
    return credit_service.update_credit_status(credit_id, current_user.id, status)