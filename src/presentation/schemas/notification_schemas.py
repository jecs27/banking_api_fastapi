from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.infrastructure.models.notification import NotificationType, NotificationPriority

class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    content: str
    priority: NotificationPriority = NotificationPriority.MEDIUM

class NotificationCreate(NotificationBase):
    user_id: int
    email: Optional[str] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    read: bool
    email_sent: bool
    created_at: datetime
    sent_at: Optional[datetime]

    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    read: bool = True
