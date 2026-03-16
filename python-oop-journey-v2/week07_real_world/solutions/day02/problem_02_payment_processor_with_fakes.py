"""Reference solution for Problem 02: Payment Processor with Fakes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto
from typing import Optional
from uuid import UUID, uuid4


class PaymentStatus(Enum):
    """Enumeration of possible payment statuses."""
    PENDING = auto()
    PROCESSING = auto()
    APPROVED = auto()
    DECLINED = auto()
    REFUNDED = auto()


@dataclass(frozen=True)
class PaymentDetails:
    """Value object containing payment information."""
    amount: Decimal
    currency: str
    card_token: str
    description: Optional[str] = None


@dataclass
class PaymentResult:
    """Value object containing payment processing result."""
    transaction_id: UUID
    status: PaymentStatus
    amount_charged: Decimal
    timestamp: str
    error_message: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        """Return True if the payment was approved."""
        return self.status == PaymentStatus.APPROVED


class PaymentGateway(ABC):
    """Abstract payment gateway interface."""
    
    @abstractmethod
    def process_payment(self, details: PaymentDetails) -> PaymentResult:
        """Process a payment."""
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: UUID, amount: Optional[Decimal] = None) -> PaymentResult:
        """Refund a previously processed payment."""
        pass


class InMemoryPaymentGateway(PaymentGateway):
    """Fake payment gateway for testing."""
    
    def __init__(self, default_approve: bool = True, decline_tokens: Optional[set[str]] = None) -> None:
        """Initialize the fake gateway."""
        self._default_approve = default_approve
        self._decline_tokens = decline_tokens or set()
        self._transactions: dict[UUID, PaymentResult] = {}
        self._refunds: dict[UUID, list[PaymentResult]] = {}
    
    def process_payment(self, details: PaymentDetails) -> PaymentResult:
        """Process a payment in memory."""
        from datetime import datetime
        
        transaction_id = uuid4()
        timestamp = datetime.now().isoformat()
        
        # Validation
        if details.amount <= 0:
            result = PaymentResult(
                transaction_id=transaction_id,
                status=PaymentStatus.DECLINED,
                amount_charged=Decimal("0"),
                timestamp=timestamp,
                error_message="Amount must be greater than zero"
            )
            self._transactions[transaction_id] = result
            return result
        
        if len(details.currency) != 3:
            result = PaymentResult(
                transaction_id=transaction_id,
                status=PaymentStatus.DECLINED,
                amount_charged=Decimal("0"),
                timestamp=timestamp,
                error_message="Invalid currency code"
            )
            self._transactions[transaction_id] = result
            return result
        
        # Check decline conditions
        if (details.card_token in self._decline_tokens or 
            not self._default_approve):
            result = PaymentResult(
                transaction_id=transaction_id,
                status=PaymentStatus.DECLINED,
                amount_charged=Decimal("0"),
                timestamp=timestamp,
                error_message="Payment declined"
            )
            self._transactions[transaction_id] = result
            return result
        
        # Approve payment
        result = PaymentResult(
            transaction_id=transaction_id,
            status=PaymentStatus.APPROVED,
            amount_charged=details.amount,
            timestamp=timestamp
        )
        self._transactions[transaction_id] = result
        self._refunds[transaction_id] = []
        return result
    
    def refund_payment(self, transaction_id: UUID, amount: Optional[Decimal] = None) -> PaymentResult:
        """Process a refund for a previous transaction."""
        from datetime import datetime
        
        timestamp = datetime.now().isoformat()
        
        if transaction_id not in self._transactions:
            return PaymentResult(
                transaction_id=uuid4(),
                status=PaymentStatus.DECLINED,
                amount_charged=Decimal("0"),
                timestamp=timestamp,
                error_message="Transaction not found"
            )
        
        original = self._transactions[transaction_id]
        refund_amount = amount or original.amount_charged
        
        # Check previous refunds
        previous_refunds = sum(r.amount_charged for r in self._refunds.get(transaction_id, []))
        remaining = original.amount_charged - previous_refunds
        
        if refund_amount > remaining:
            return PaymentResult(
                transaction_id=uuid4(),
                status=PaymentStatus.DECLINED,
                amount_charged=Decimal("0"),
                timestamp=timestamp,
                error_message="Refund amount exceeds remaining balance"
            )
        
        result = PaymentResult(
            transaction_id=uuid4(),
            status=PaymentStatus.REFUNDED,
            amount_charged=refund_amount,
            timestamp=timestamp
        )
        
        self._refunds[transaction_id].append(result)
        
        # Update original transaction status if fully refunded
        total_refunded = previous_refunds + refund_amount
        if total_refunded >= original.amount_charged:
            original.status = PaymentStatus.REFUNDED
        
        return result
    
    def get_transaction(self, transaction_id: UUID) -> Optional[PaymentResult]:
        """Retrieve a stored transaction by ID."""
        return self._transactions.get(transaction_id)


class PaymentProcessor:
    """High-level payment processing service."""
    
    def __init__(self, gateway: PaymentGateway) -> None:
        """Initialize with a payment gateway."""
        self._gateway = gateway
    
    def charge(self, amount: Decimal, currency: str, card_token: str, description: Optional[str] = None) -> PaymentResult:
        """Charge a card for the specified amount."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if not currency or len(currency) != 3:
            raise ValueError("Currency must be a 3-letter code")
        
        details = PaymentDetails(
            amount=amount,
            currency=currency.upper(),
            card_token=card_token,
            description=description
        )
        return self._gateway.process_payment(details)
    
    def refund(self, transaction_id: UUID, amount: Optional[Decimal] = None) -> PaymentResult:
        """Refund a previous transaction."""
        return self._gateway.refund_payment(transaction_id, amount)
    
    def get_payment_status(self, transaction_id: UUID) -> Optional[PaymentStatus]:
        """Check the status of a payment."""
        result = self._gateway.get_transaction(transaction_id)
        return result.status if result else None
