from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.models.payment import Payment, PaymentStatus
from src.infrastructure.models.notification import Notification, NotificationType, NotificationPriority

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_by_credit_id(self, credit_id: int) -> List[Payment]:
        return self.db.query(Payment).filter(Payment.credit_id == credit_id).all()

    def get_overdue_payments(self) -> List[Payment]:
        return self.db.query(Payment)\
            .filter(Payment.status == PaymentStatus.PENDING)\
            .filter(Payment.payment_date < datetime.utcnow())\
            .all()

    def update(self, payment: Payment) -> Payment:
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def mark_as_completed(self, payment: Payment) -> Payment:
        payment.status = PaymentStatus.COMPLETED
        return self.update(payment)

    def mark_as_failed(self, payment: Payment) -> Payment:
        payment.status = PaymentStatus.FAILED
        return self.update(payment)

    def mark_as_reversed(self, payment: Payment) -> Payment:
        payment.status = PaymentStatus.REVERSED
        return self.update(payment)

    def mark_as_overdue(self, payment: Payment) -> Payment:
        payment.status = PaymentStatus.OVERDUE
        
        notification = Notification(
            user_id=payment.credit.account.user_id,
            type=NotificationType.CREDIT_PAYMENT,
            priority=NotificationPriority.HIGH,
            title="Payment Overdue",
            content=f"Your credit payment of ${payment.amount} is overdue."
        )
        self.db.add(notification)
        
        return self.update(payment)
