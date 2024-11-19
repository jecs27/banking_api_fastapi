from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.infrastructure.config.database import get_db
from src.infrastructure.models.user import User
from src.infrastructure.models.notification import NotificationType
from src.infrastructure.security import get_current_user
from src.application.services.notification_service import NotificationService
from src.presentation.schemas.notification_schemas import NotificationResponse

router = APIRouter(tags=["notifications"])

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = False,
    notification_type: Optional[NotificationType] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    return notification_service.get_user_notifications(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
        notification_type=notification_type
    )

@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification = notification_service.mark_as_read(notification_id, current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/read-all")
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    updated_count = notification_service.mark_all_as_read(current_user.id)
    return {"message": f"Marked {updated_count} notifications as read"}