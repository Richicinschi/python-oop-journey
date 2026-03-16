"""Problem 04: Bounded Withdrawal

Topic: Exception Handling, Validation
Difficulty: Easy

Implement a bank withdrawal function with multiple validation checks.

Examples:
    >>> bounded_withdrawal(100, 50, 200)
    50
    >>> bounded_withdrawal(100, 150, 200)
    Traceback (most recent call last):
        ...
    InsufficientFundsError: Cannot withdraw 150, balance is 100
    >>> bounded_withdrawal(100, 50, 40)
    Traceback (most recent call last):
        ...
    LimitExceededError: Cannot withdraw 50, limit is 40
    >>> bounded_withdrawal(100, -10, 200)
    Traceback (most recent call last):
        ...
    ValueError: Withdrawal amount must be positive

Requirements:
    - Create custom exceptions InsufficientFundsError and LimitExceededError
    - Check that withdrawal amount is positive (raise ValueError if not)
    - Check that balance is sufficient (raise InsufficientFundsError if not)
    - Check that withdrawal doesn't exceed limit (raise LimitExceededError if not)
    - Return the new balance (balance - amount) on success
"""

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
    raise NotImplementedError("Implement bounded_withdrawal")
