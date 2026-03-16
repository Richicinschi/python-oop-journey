"""Solution for Problem 04: Bounded Withdrawal."""

from __future__ import annotations


class InsufficientFundsError(Exception):
    """Raised when account balance is insufficient for withdrawal."""
    pass


class LimitExceededError(Exception):
    """Raised when withdrawal exceeds the allowed limit."""
    pass


def bounded_withdrawal(balance: float, amount: float, limit: float) -> float:
    """Process a withdrawal with balance and limit checks.

    Args:
        balance: Current account balance
        amount: Amount to withdraw
        limit: Maximum allowed withdrawal amount

    Returns:
        The new balance after withdrawal

    Raises:
        ValueError: If amount is not positive
        InsufficientFundsError: If balance is insufficient
        LimitExceededError: If amount exceeds limit
    """
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    
    if amount > balance:
        raise InsufficientFundsError(
            f"Cannot withdraw {amount}, balance is {balance}"
        )
    
    if amount > limit:
        raise LimitExceededError(f"Cannot withdraw {amount}, limit is {limit}")
    
    return balance - amount
