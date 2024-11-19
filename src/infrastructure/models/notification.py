from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.infrastructure.models.base import Base

class NotificationType(str, Enum):
    TRANSACTION = "transaction"
    CREDIT_PAYMENT = "credit_payment"
    SECURITY_ALERT = "security_alert"
    CREDIT_STATUS = "credit_status"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(SQLEnum(NotificationType))
    priority = Column(SQLEnum(NotificationPriority), default=NotificationPriority.MEDIUM)
    title = Column(String)
    content = Column(String)
    email_sent = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)

    # Relationship
    user = relationship("User", back_populates="notifications")