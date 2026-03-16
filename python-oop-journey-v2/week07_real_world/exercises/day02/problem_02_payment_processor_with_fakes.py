"""Problem 02: Payment Processor with Fakes

Topic: Fake implementations
Difficulty: Medium

Learn to create fake implementations that behave like real dependencies
but are faster and more controllable for testing.
"""

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
    """Value object containing payment information.
    
    Attributes:
        amount: The payment amount
        currency: Three-letter currency code (e.g., 'USD')
        card_token: Tokenized card identifier
        description: Optional payment description
    """
    amount: Decimal
    currency: str
    card_token: str
    description: Optional[str] = None


@dataclass
class PaymentResult:
    """Value object containing payment processing result.
    
    Attributes:
        transaction_id: Unique identifier for this transaction
        status: Final payment status
        amount_charged: Actual amount charged (may differ from request)
        timestamp: When the transaction was processed
        error_message: Description of error if declined
    """
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
    """Abstract payment gateway interface.
    
    Defines the contract for payment processing implementations.
    Real implementations connect to Stripe, PayPal, etc.
    """
    
    @abstractmethod
    def process_payment(self, details: PaymentDetails) -> PaymentResult:
        """Process a payment.
        
        Args:
            details: The payment details to process
            
        Returns:
            Result of the payment operation
        """
        raise NotImplementedError("Implement process_payment")
    
    @abstractmethod
    def refund_payment(self, transaction_id: UUID, amount: Optional[Decimal] = None) -> PaymentResult:
        """Refund a previously processed payment.
        
        Args:
            transaction_id: The transaction to refund
            amount: Amount to refund (None for full refund)
            
        Returns:
            Result of the refund operation
        """
        raise NotImplementedError("Implement refund_payment")


class InMemoryPaymentGateway(PaymentGateway):
    """Fake payment gateway for testing.
    
    Simulates payment processing in memory without external calls.
    Supports configurable success/failure scenarios.
    
    TODO: Implement this fake gateway with the following features:
    - Store processed payments in memory
    - Support configurable approval/decline behavior
    - Validate basic rules (amount > 0, valid currency)
    - Support partial and full refunds
    """
    
    def __init__(self, default_approve: bool = True, decline_tokens: Optional[set[str]] = None) -> None:
        """Initialize the fake gateway.
        
        Args:
            default_approve: Whether to approve payments by default
            decline_tokens: Set of card tokens that should be declined
        """
        raise NotImplementedError("Implement __init__")
    
    def process_payment(self, details: PaymentDetails) -> PaymentResult:
        """Process a payment in memory.
        
        Should validate inputs, simulate processing time if desired,
        and return appropriate PaymentResult.
        
        Decline if:
        - amount <= 0
        - card_token in decline_tokens
        - default_approve is False
        """
        raise NotImplementedError("Implement process_payment")
    
    def refund_payment(self, transaction_id: UUID, amount: Optional[Decimal] = None) -> PaymentResult:
        """Process a refund for a previous transaction.
        
        Should verify the transaction exists and hasn't been fully refunded.
        """
        raise NotImplementedError("Implement refund_payment")
    
    def get_transaction(self, transaction_id: UUID) -> Optional[PaymentResult]:
        """Retrieve a stored transaction by ID.
        
        Useful for test verification.
        
        Args:
            transaction_id: The transaction to look up
            
        Returns:
            The stored result, or None if not found
        """
        raise NotImplementedError("Implement get_transaction")


class PaymentProcessor:
    """High-level payment processing service.
    
    Orchestrates payment operations and provides business logic
    on top of the gateway abstraction.
    
    TODO: Implement the processor methods.
    """
    
    def __init__(self, gateway: PaymentGateway) -> None:
        """Initialize with a payment gateway.
        
        Args:
            gateway: The payment gateway to use
        """
        raise NotImplementedError("Implement __init__")
    
    def charge(self, amount: Decimal, currency: str, card_token: str, description: Optional[str] = None) -> PaymentResult:
        """Charge a card for the specified amount.
        
        Args:
            amount: Amount to charge
            currency: Currency code
            card_token: Tokenized card
            description: Optional payment description
            
        Returns:
            Payment processing result
            
        Raises:
            ValueError: If amount <= 0 or currency is invalid
        """
        raise NotImplementedError("Implement charge")
    
    def refund(self, transaction_id: UUID, amount: Optional[Decimal] = None) -> PaymentResult:
        """Refund a previous transaction.
        
        Args:
            transaction_id: Transaction to refund
            amount: Amount to refund (None for full)
            
        Returns:
            Refund result
        """
        raise NotImplementedError("Implement refund")
    
    def get_payment_status(self, transaction_id: UUID) -> Optional[PaymentStatus]:
        """Check the status of a payment.
        
        Args:
            transaction_id: Transaction to check
            
        Returns:
            Current status, or None if not found
        """
        raise NotImplementedError("Implement get_payment_status")
