"""Problem 02: Bank Account

Topic: Methods, validation, state management
Difficulty: Easy

Create a BankAccount class with balance management.

Examples:
    >>> account = BankAccount("John Doe", 100.0)
    >>> account.deposit(50.0)
    150.0
    >>> account.withdraw(30.0)
    120.0
    >>> account.withdraw(200.0)  # Insufficient funds
    >>> account.get_balance()
    120.0

Requirements:
    - __init__ takes owner (str) and optional initial_balance (float, default 0.0)
    - deposit(amount) adds to balance, returns new balance
    - withdraw(amount) subtracts if sufficient funds, returns new balance or None
    - get_balance() returns current balance
    - Negative amounts should be rejected in deposit/withdraw
"""

from __future__ import annotations


class BankAccount:
    """A class representing a bank account."""

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        """Initialize a bank account with owner and optional initial balance."""
        raise NotImplementedError("Initialize owner and balance attributes")

    def deposit(self, amount: float) -> float:
        """Deposit money into the account.
        
        Args:
            amount: The amount to deposit (must be positive)
            
        Returns:
            The new balance after deposit
        """
        raise NotImplementedError("Implement deposit method")

    def withdraw(self, amount: float) -> float | None:
        """Withdraw money from the account if sufficient funds exist.
        
        Args:
            amount: The amount to withdraw (must be positive)
            
        Returns:
            The new balance after withdrawal, or None if insufficient funds
        """
        raise NotImplementedError("Implement withdraw method")

    def get_balance(self) -> float:
        """Return the current balance."""
        raise NotImplementedError("Implement get_balance method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
