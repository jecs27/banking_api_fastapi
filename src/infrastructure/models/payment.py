from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from src.infrastructure.models.base import Base

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"
    OVERDUE = "OVERDUE"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    credit_id = Column(Integer, ForeignKey("credits.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(SQLEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    credit = relationship("Credit", back_populates="payments")
    transaction = relationship("Transaction")
