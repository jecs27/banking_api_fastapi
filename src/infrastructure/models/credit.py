from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from src.infrastructure.models.base import Base

class CreditStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DEFAULTED = "DEFAULTED"

class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    interest_rate = Column(Numeric(precision=5, scale=2), nullable=False)
    term_months = Column(Integer, nullable=False)
    monthly_payment = Column(Numeric(precision=10, scale=2), nullable=False)
    status = Column(SQLEnum(CreditStatus), nullable=False, default=CreditStatus.PENDING)
    purpose = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    next_payment_date = Column(DateTime, nullable=True)
    remaining_amount = Column(Numeric(precision=10, scale=2), nullable=True)

    # Relationships
    user = relationship("User", back_populates="credits")