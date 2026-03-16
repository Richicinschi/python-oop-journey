"""Exercise: Payment Processor ABC.

Create an abstract base class PaymentProcessor with abstract methods
process_payment and refund.

TODO:
1. Create PaymentProcessor ABC inheriting from ABC
2. Add __init__ with merchant_id attribute
3. Add abstract method process_payment(self, amount: float, currency: str) -> dict
4. Add abstract method refund(self, transaction_id: str) -> bool
5. Create concrete implementations: CreditCardProcessor and PayPalProcessor
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract base class for payment processors.
    
    Attributes:
        merchant_id: The merchant identifier string.
    """
    
    def __init__(self, merchant_id: str) -> None:
        """Initialize the payment processor."""
        # TODO: Initialize merchant_id attribute
        raise NotImplementedError("Initialize merchant_id")
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process a payment and return transaction details.
        
        Args:
            amount: The payment amount (must be positive).
            currency: The currency code (e.g., 'USD', 'EUR').
        
        Returns:
            Dictionary with transaction details including 'transaction_id',
            'amount', 'currency', and 'status'.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("process_payment must be implemented")
    
    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction.
        
        Args:
            transaction_id: The ID of the transaction to refund.
        
        Returns:
            True if refund was successful, False otherwise.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("refund must be implemented")


class CreditCardProcessor(PaymentProcessor):
    """Concrete implementation for credit card payments."""
    
    def __init__(self, merchant_id: str, gateway: str = "stripe") -> None:
        """Initialize credit card processor.
        
        Args:
            merchant_id: The merchant identifier.
            gateway: The payment gateway name.
        """
        # TODO: Call parent __init__ and set gateway
        raise NotImplementedError("Initialize credit card processor")
    
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process credit card payment."""
        # TODO: Return transaction dict with 'cc_' prefix for transaction_id
        raise NotImplementedError("Implement credit card payment processing")
    
    def refund(self, transaction_id: str) -> bool:
        """Process credit card refund."""
        # TODO: Return True if transaction_id starts with 'cc_'
        raise NotImplementedError("Implement credit card refund")


class PayPalProcessor(PaymentProcessor):
    """Concrete implementation for PayPal payments."""
    
    def __init__(self, merchant_id: str, client_id: str) -> None:
        """Initialize PayPal processor.
        
        Args:
            merchant_id: The merchant identifier.
            client_id: The PayPal client ID.
        """
        # TODO: Call parent __init__ and set client_id
        raise NotImplementedError("Initialize PayPal processor")
    
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process PayPal payment."""
        # TODO: Return transaction dict with 'pp_' prefix for transaction_id
        raise NotImplementedError("Implement PayPal payment processing")
    
    def refund(self, transaction_id: str) -> bool:
        """Process PayPal refund."""
        # TODO: Return True if transaction_id starts with 'pp_'
        raise NotImplementedError("Implement PayPal refund")
