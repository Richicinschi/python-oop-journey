"""Solution for Problem 01: Payment Processor ABC.

Demonstrates abstract base classes with process_payment and refund methods.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract base class for payment processors.
    
    Attributes:
        merchant_id: The merchant identifier string.
    
    Example:
        >>> processor = CreditCardProcessor("merch_123", "stripe")
        >>> result = processor.process_payment(100.0, "USD")
        >>> result['amount']
        100.0
    """
    
    def __init__(self, merchant_id: str) -> None:
        """Initialize the payment processor.
        
        Args:
            merchant_id: The merchant identifier string.
        """
        self.merchant_id = merchant_id
    
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
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction.
        
        Args:
            transaction_id: The ID of the transaction to refund.
        
        Returns:
            True if refund was successful, False otherwise.
        """
        pass


class CreditCardProcessor(PaymentProcessor):
    """Concrete implementation for credit card payments.
    
    Attributes:
        gateway: The payment gateway name (e.g., 'stripe', 'braintree').
    """
    
    def __init__(self, merchant_id: str, gateway: str = "stripe") -> None:
        """Initialize credit card processor.
        
        Args:
            merchant_id: The merchant identifier.
            gateway: The payment gateway name.
        """
        super().__init__(merchant_id)
        self.gateway = gateway
    
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process credit card payment.
        
        Args:
            amount: The payment amount.
            currency: The currency code.
        
        Returns:
            Transaction details with 'cc_' prefixed transaction_id.
        """
        import uuid
        transaction_id = f"cc_{uuid.uuid4().hex[:12]}"
        return {
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "status": "completed",
            "gateway": self.gateway,
        }
    
    def refund(self, transaction_id: str) -> bool:
        """Process credit card refund.
        
        Args:
            transaction_id: The transaction to refund.
        
        Returns:
            True if the transaction_id starts with 'cc_', False otherwise.
        """
        return transaction_id.startswith("cc_")


class PayPalProcessor(PaymentProcessor):
    """Concrete implementation for PayPal payments.
    
    Attributes:
        client_id: The PayPal client ID.
    """
    
    def __init__(self, merchant_id: str, client_id: str) -> None:
        """Initialize PayPal processor.
        
        Args:
            merchant_id: The merchant identifier.
            client_id: The PayPal client ID.
        """
        super().__init__(merchant_id)
        self.client_id = client_id
    
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process PayPal payment.
        
        Args:
            amount: The payment amount.
            currency: The currency code.
        
        Returns:
            Transaction details with 'pp_' prefixed transaction_id.
        """
        import uuid
        transaction_id = f"pp_{uuid.uuid4().hex[:12]}"
        return {
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "status": "completed",
            "client_id": self.client_id,
        }
    
    def refund(self, transaction_id: str) -> bool:
        """Process PayPal refund.
        
        Args:
            transaction_id: The transaction to refund.
        
        Returns:
            True if the transaction_id starts with 'pp_', False otherwise.
        """
        return transaction_id.startswith("pp_")
