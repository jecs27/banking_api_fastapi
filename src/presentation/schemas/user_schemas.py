from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated
from datetime import datetime

from src.infrastructure.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    role: Optional[UserRole] = UserRole.USER

class UserCreate(UserBase):
    password: Annotated[str, constr(min_length=8)]

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[Annotated[str, constr(min_length=8)]] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str