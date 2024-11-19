from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.models.notification import Notification, NotificationType

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Notification:
        notification = Notification(**kwargs)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False,
        notification_type: Optional[NotificationType] = None
    ) -> List[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.read == False)
        
        if notification_type:
            query = query.filter(Notification.type == notification_type)
        
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    def mark_as_read(self, notification_id: int, user_id: int) -> Notification:
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.read = True
            self.db.commit()
            self.db.refresh(notification)
        
        return notification

    def mark_all_as_read(self, user_id: int) -> int:
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.read == False
        ).update({"read": True})