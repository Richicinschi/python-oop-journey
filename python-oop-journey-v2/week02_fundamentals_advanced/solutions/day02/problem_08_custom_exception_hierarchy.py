"""Solution for Problem 08: Custom Exception Hierarchy."""

from __future__ import annotations


class PaymentError(Exception):
    """Base exception for payment processing errors."""
    
    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


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
    if not isinstance(card_number, str) or card_number == "":
        raise InvalidCardError("Invalid card number")
    
    if "network_error" in card_number:
        raise NetworkError("Network connection failed")
    
    if amount > 1000:
        raise PaymentDeclinedError("Amount exceeds limit")
    
    return f"Payment of {amount} processed successfully"
