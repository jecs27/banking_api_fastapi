from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session
from src.infrastructure.models.payment import Payment, PaymentStatus
from src.infrastructure.models.credit import Credit
from src.infrastructure.models.transaction import Transaction, TransactionType, TransactionStatus
from src.infrastructure.models.notification import Notification, NotificationType, NotificationPriority

class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, credit_id: int, amount: Decimal, payment_date: datetime) -> Payment:
        """Create a new payment record"""
        payment = Payment(
            credit_id=credit_id,
            amount=amount,
            payment_date=payment_date,
            status=PaymentStatus.PENDING
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_payment(self, payment_id: int) -> Optional[Payment]:
        """Get a payment by ID"""
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payments_by_credit(self, credit_id: int) -> List[Payment]:
        """Get all payments for a specific credit"""
        return self.db.query(Payment).filter(Payment.credit_id == credit_id).all()

    def process_payment(self, payment_id: int) -> Payment:
        """Process a pending payment"""
        payment = self.get_payment(payment_id)
        if not payment or payment.status != PaymentStatus.PENDING:
            raise ValueError("Invalid payment or payment already processed")

        credit = payment.credit
        
        # Create transaction for the payment
        transaction = Transaction(
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            amount=payment.amount,
            account_id=credit.account_id,
            description=f"Credit payment - Credit ID: {credit.id}",
            reference_number=f"PAY-{payment.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        )
        self.db.add(transaction)
        
        # Update payment status and link transaction
        payment.status = PaymentStatus.COMPLETED
        payment.transaction_id = transaction.id
        
        # Create notification
        notification = Notification(
            user_id=credit.account.user_id,
            type=NotificationType.CREDIT_PAYMENT,
            priority=NotificationPriority.MEDIUM,
            title="Credit Payment Processed",
            content=f"Your credit payment of ${payment.amount} has been processed successfully."
        )
        self.db.add(notification)
        
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def mark_payment_as_failed(self, payment_id: int, reason: str) -> Payment:
        """Mark a payment as failed"""
        payment = self.get_payment(payment_id)
        if not payment:
            raise ValueError("Payment not found")
            
        payment.status = PaymentStatus.FAILED
        
        notification = Notification(
            user_id=payment.credit.account.user_id,
            type=NotificationType.CREDIT_PAYMENT,
            priority=NotificationPriority.HIGH,
            title="Credit Payment Failed",
            content=f"Your credit payment of ${payment.amount} has failed. Reason: {reason}"
        )
        self.db.add(notification)
        
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def reverse_payment(self, payment_id: int) -> Payment:
        """Reverse a completed payment"""
        payment = self.get_payment(payment_id)
        if not payment or payment.status != PaymentStatus.COMPLETED:
            raise ValueError("Invalid payment or payment not completed")
            
        payment.status = PaymentStatus.REVERSED
        
        if payment.transaction:
            payment.transaction.status = TransactionStatus.REVERSED
            
        notification = Notification(
            user_id=payment.credit.account.user_id,
            type=NotificationType.CREDIT_PAYMENT,
            priority=NotificationPriority.HIGH,
            title="Credit Payment Reversed",
            content=f"Your credit payment of ${payment.amount} has been reversed."
        )
        self.db.add(notification)
        
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_overdue_payments(self) -> List[Payment]:
        """Get all overdue payments"""
        return self.db.query(Payment)\
            .filter(Payment.status == PaymentStatus.PENDING)\
            .filter(Payment.payment_date < datetime.utcnow())\
            .all()

    def mark_payments_as_overdue(self):
        """Mark all overdue payments"""
        overdue_payments = self.get_overdue_payments()
        for payment in overdue_payments:
            payment.status = PaymentStatus.OVERDUE
            
            notification = Notification(
                user_id=payment.credit.account.user_id,
                type=NotificationType.CREDIT_PAYMENT,
                priority=NotificationPriority.HIGH,
                title="Payment Overdue",
                content=f"Your credit payment of ${payment.amount} is overdue."
            )
            self.db.add(notification)
        
        self.db.commit()
