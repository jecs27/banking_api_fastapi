from sqlalchemy import Column, String, Boolean
from sqlalchemy import Enum as SQLEnum
from enum import Enum
from .base import BaseModel
from sqlalchemy.orm import relationship

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole, name="user_role_enum", create_type=False), 
                 nullable=False, 
                 default=UserRole.USER,
                 server_default=UserRole.USER.value)

    # Relationships
    credits = relationship("Credit", back_populates="user")
    accounts = relationship("Account", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
