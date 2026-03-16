"""Problem 08: Custom Exception Hierarchy

Topic: Exception Inheritance
Difficulty: Medium

Create a hierarchy of custom exceptions for a payment processing system.

Examples:
    >>> try:
    ...     raise PaymentDeclinedError("Card expired")
    ... except PaymentError:
    ...     print("Payment failed")
    Payment failed
    
    >>> issubclass(PaymentDeclinedError, PaymentError)
    True
    >>> issubclass(InvalidCardError, PaymentError)
    True
    >>> issubclass(InvalidCardError, PaymentDeclinedError)
    False

Requirements:
    - Create PaymentError as the base exception class
    - Create PaymentDeclinedError inheriting from PaymentError
    - Create InvalidCardError inheriting from PaymentError
    - Create NetworkError inheriting from PaymentError
    - Each exception should accept a message and optional code parameter
"""

from __future__ import annotations


class PaymentError(Exception):
    """Base exception for payment processing errors."""
    pass


class PaymentDeclinedError(PaymentError):
    """Raised when a payment is declined by the processor."""
    pass


class InvalidCardError(PaymentError):
    """Raised when card details are invalid."""
    pass


class NetworkError(PaymentError):
    """Raised when a network error occurs during payment."""
    pass


def process_payment(card_number: str, amount: float) -> str:
    """Process a payment with the given card.

    Args:
        card_number: The card number to charge
        amount: The amount to charge

    Returns:
        Success message if payment processed

    Raises:
        InvalidCardError: If card_number is empty or not a string
        PaymentDeclinedError: If amount > 1000 (simulated limit)
        NetworkError: If card_number contains "network_error"
    """
    raise NotImplementedError("Implement process_payment")
