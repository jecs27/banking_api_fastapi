from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from src.infrastructure.models.base import Base

class AccountType(str, Enum):
    SAVINGS = "SAVINGS"     # Cuenta de ahorro - Para guardar dinero a largo plazo
    DEBIT = "DEBIT"        # Cuenta de débito - Para gastos diarios y transacciones frecuentes

class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"
    CLOSED = "CLOSED"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_number = Column(String(20), unique=True, nullable=False, index=True)
    account_type = Column(SQLEnum(AccountType), nullable=False)
    status = Column(SQLEnum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE)
    balance = Column(Numeric(precision=15, scale=2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="MXN")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_transaction_date = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions = relationship(
        "Transaction",
        back_populates="account",
        foreign_keys="[Transaction.account_id]"
    )