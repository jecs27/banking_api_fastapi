from datetime import datetime
from typing import List, Optional
from fastapi_mail import MessageSchema, MessageType
from sqlalchemy.orm import Session
from src.infrastructure.config.email import fastmail
from src.infrastructure.models.notification import Notification, NotificationType, NotificationPriority
from src.infrastructure.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = NotificationRepository(db)

    async def create_and_send_notification(
        self,
        user_id: int,
        type: NotificationType,
        title: str,
        content: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        email: str = None
    ) -> Notification:

        notification = self.repository.create(
            user_id=user_id,
            type=type,
            title=title,
            content=content,
            priority=priority
        )

        if email:
            await self._send_email_notification(
                email=email,
                title=title,
                content=content,
                notification_id=notification.id
            )
            
            notification.email_sent = True
            notification.sent_at = datetime.utcnow()
            self.db.commit()

        return notification

    async def _send_email_notification(
        self,
        email: str,
        title: str,
        content: str,
        notification_id: int
    ):
        message = MessageSchema(
            subject=title,
            recipients=[email],
            body=self._get_email_template(title, content),
            subtype=MessageType.html
        )
        
        await fastmail.send_message(message)

    def _get_email_template(self, title: str, content: str) -> str:
        return f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Su código OTP</title>
                <style type="text/css">
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .logo {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .logo img {{
                        max-width: 150px;
                    }}
                    .container {{
                        background-color: #f9f9f9;
                        border-radius: 5px;
                        padding: 20px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .message {{
                        font-size: 16px;
                        line-height: 1.6;
                        margin: 15px 0;
                    }}
                    .footer {{
                        margin-top: 20px;
                        padding-top: 15px;
                        border-top: 1px solid #eee;
                        font-size: 14px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="logo">
                    <img src="https://api.finco.lat/assets/finch_logo-de7068b89f7e60575666bd7079844f5f5fe1153b80cd4102633625221d9dd95d.png" alt="Logo de la empresa">
                </div>
                <div class="container">
                    <h1>{title}</h1>
                    <p>Estimado usuario,</p>
                    <p>{content}</p>
                    <p>Atentamente,</p>
                    <p>Equipo de Finch<br>
                    Departamento de Operaciones Bancarias<br>
                    Tel: +1 (555) 123-4567<br>
                    soporte@finch.lat</p>
                    <p class="footer-note" style="font-size: 12px; color: #666;">
                        Este es un mensaje automático. Por favor no responda a este correo. Si necesita ayuda, 
                        contáctenos a través de nuestros canales oficiales de atención al cliente.
                    </p>
                </div>
            </body>
            </html>
        """

    def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False,
        notification_type: Optional[NotificationType] = None
    ) -> List[Notification]:
        return self.repository.get_user_notifications(
            user_id=user_id,
            skip=skip,
            limit=limit,
            unread_only=unread_only,
            notification_type=notification_type
        )

    def mark_as_read(self, notification_id: int, user_id: int) -> Notification:
        return self.repository.mark_as_read(notification_id, user_id)

    def mark_all_as_read(self, user_id: int) -> int:
        return self.repository.mark_all_as_read(user_id)