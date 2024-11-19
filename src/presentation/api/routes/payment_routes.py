from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordBearer

from src.application.services.pyament_service import PaymentService
from src.application.services.auth_service import AuthService
from src.infrastructure.config.database import get_db
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.schemas.payment_schema import Payment, PaymentCreate, PaymentUpdate
from src.infrastructure.models.user import User

router = APIRouter(tags=["payments"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    payment_service = PaymentService(db)
    return payment_service.create_payment(payment)

@router.get("/{payment_id}", response_model=Payment)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    payment_service = PaymentService(db)
    payment = payment_service.get_payment(payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

@router.get("/credit/{credit_id}", response_model=List[Payment])
def get_credit_payments(
    credit_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    payment_service = PaymentService(db)
    return payment_service.get_credit_payments(credit_id)

@router.patch("/{payment_id}", response_model=Payment)
def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    payment_service = PaymentService(db)
    payment = payment_service.update_payment(payment_id, payment_update)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

@router.post("/{payment_id}/complete", response_model=Payment)
def complete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    payment_service = PaymentService(db)
    try:
        return payment_service.complete_payment(payment_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{payment_id}/reverse", response_model=Payment)
def reverse_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    payment_service = PaymentService(db)
    try:
        return payment_service.reverse_payment(payment_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
