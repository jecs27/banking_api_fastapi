from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.application.services.auth_service import AuthService
from src.infrastructure.config.database import get_db
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.schemas.user_schemas import User, UserCreate, UserUpdate
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    user = repo.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = repo.create(user_in)
    return user
    
@router.get("/", response_model=User)
def read_users(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    user = repo.get_by_email(email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/", response_model=User)
def update_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    current_user = repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    user = repo.update(user_id=current_user.id, user_data=user_in)
    return user

@router.delete("/", response_model=bool)
def delete_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    repo = UserRepository(db)
    auth_service = AuthService(repo)
    token_data = auth_service.verify_token(token)
    current_user = repo.get_by_email(email=token_data.email)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return repo.delete(user_id=current_user.id)