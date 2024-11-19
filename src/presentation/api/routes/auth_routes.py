from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from src.infrastructure.config.database import get_db
from src.infrastructure.repositories.user_repository import UserRepository
from src.application.services.auth_service import AuthService
from src.presentation.schemas.auth_schemas import Login, Token
from src.presentation.schemas.user_schemas import User
from src.infrastructure.config.settings import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    token_data = auth_service.verify_token(token)
    user = user_repository.get_by_email(email=token_data.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_data: Login,
    db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user