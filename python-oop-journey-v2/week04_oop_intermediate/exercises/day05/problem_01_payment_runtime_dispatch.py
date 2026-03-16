"""Problem 01: Payment Runtime Dispatch.

Topic: Polymorphism
Difficulty: Easy

Create a PaymentProcessor base class and concrete implementations.
Demonstrate polymorphic processing where different payment types
are handled uniformly through a common interface.

TODO:
1. Create PaymentProcessor ABC with:
   - __init__(self, merchant_id: str)
   - process_payment(self, amount: float, currency: str) -> dict (abstract)
   - get_processor_name(self) -> str (abstract)

2. Create CreditCardProcessor class:
   - __init__(self, merchant_id: str, gateway: str = "stripe")
   - process_payment returns dict with 'transaction_id', 'amount', 'currency', 'method': 'credit_card'
   - get_processor_name returns "Credit Card"

3. Create PayPalProcessor class:
   - __init__(self, merchant_id: str, client_id: str)
   - process_payment returns dict with 'transaction_id', 'amount', 'currency', 'method': 'paypal'
   - get_processor_name returns "PayPal"

4. Create CryptoProcessor class:
   - __init__(self, merchant_id: str, currency_type: str = "BTC")
   - process_payment returns dict with 'transaction_id', 'amount', 'currency', 'method': 'crypto'
   - get_processor_name returns "Cryptocurrency"

5. Implement process_all_payments(processors: list, amount: float, currency: str) -> list[dict]
   that processes all payments polymorphically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract base class for payment processors."""
    
    def __init__(self, merchant_id: str) -> None:
        """Initialize the payment processor.
        
        Args:
            merchant_id: The merchant identifier string.
        """
        # TODO: Initialize merchant_id attribute
        raise NotImplementedError("Initialize merchant_id")
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process a payment and return transaction details.
        
        Args:
            amount: The payment amount.
            currency: The currency code (e.g., 'USD', 'EUR').
        
        Returns:
            Dictionary with transaction details.
        """
        raise NotImplementedError("process_payment must be implemented")
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """Return the human-readable processor name.
        
        Returns:
            String name of the processor type.
        """
        raise NotImplementedError("get_processor_name must be implemented")


class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor."""
    
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
        # TODO: Return transaction dict with method='credit_card'
        raise NotImplementedError("Implement credit card payment processing")
    
    def get_processor_name(self) -> str:
        """Return processor name."""
        # TODO: Return "Credit Card"
        raise NotImplementedError("Implement get_processor_name")


class PayPalProcessor(PaymentProcessor):
    """PayPal payment processor."""
    
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
        # TODO: Return transaction dict with method='paypal'
        raise NotImplementedError("Implement PayPal payment processing")
    
    def get_processor_name(self) -> str:
        """Return processor name."""
        # TODO: Return "PayPal"
        raise NotImplementedError("Implement get_processor_name")


class CryptoProcessor(PaymentProcessor):
    """Cryptocurrency payment processor."""
    
    def __init__(self, merchant_id: str, currency_type: str = "BTC") -> None:
        """Initialize crypto processor.
        
        Args:
            merchant_id: The merchant identifier.
            currency_type: The cryptocurrency type (e.g., 'BTC', 'ETH').
        """
        # TODO: Call parent __init__ and set currency_type
        raise NotImplementedError("Initialize crypto processor")
    
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process cryptocurrency payment."""
        # TODO: Return transaction dict with method='crypto'
        raise NotImplementedError("Implement crypto payment processing")
    
    def get_processor_name(self) -> str:
        """Return processor name."""
        # TODO: Return "Cryptocurrency"
        raise NotImplementedError("Implement get_processor_name")


def process_all_payments(
    processors: list[PaymentProcessor],
    amount: float,
    currency: str
) -> list[dict]:
    """Process payments through all processors polymorphically.
    
    Args:
        processors: List of PaymentProcessor instances.
        amount: The payment amount.
        currency: The currency code.
    
    Returns:
        List of transaction result dictionaries.
    """
    # TODO: Iterate through processors and call process_payment on each
    # Demonstrate polymorphism - same method call, different implementations
    raise NotImplementedError("Implement process_all_payments")
