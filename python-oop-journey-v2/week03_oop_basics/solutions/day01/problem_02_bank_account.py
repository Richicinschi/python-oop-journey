"""Reference solution for Problem 02: Bank Account."""

from __future__ import annotations


class BankAccount:
    """A class representing a bank account."""

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        """Initialize a bank account with owner and optional initial balance.
        
        Args:
            owner: The account owner's name
            initial_balance: Starting balance (default 0.0)
        """
        self.owner = owner
        self._balance = initial_balance

    def deposit(self, amount: float) -> float:
        """Deposit money into the account.
        
        Args:
            amount: The amount to deposit (must be positive)
            
        Returns:
            The new balance after deposit
        """
        if amount > 0:
            self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float | None:
        """Withdraw money from the account if sufficient funds exist.
        
        Args:
            amount: The amount to withdraw (must be positive)
            
        Returns:
            The new balance after withdrawal, or None if insufficient funds
        """
        if 0 < amount <= self._balance:
            self._balance -= amount
            return self._balance
        return None

    def get_balance(self) -> float:
        """Return the current balance."""
        return self._balance

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"BankAccount(owner={self.owner}, balance={self._balance})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"BankAccount(owner='{self.owner}', initial_balance={self._balance})"
