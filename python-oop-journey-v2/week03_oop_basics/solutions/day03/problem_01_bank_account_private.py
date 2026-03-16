"""Solution for Problem 01: Bank Account Private.

Demonstrates private attributes with getter and setter methods.
"""

from __future__ import annotations


class BankAccount:
    """A bank account with private balance attribute.
    
    This class demonstrates the traditional getter/setter pattern
    using explicit methods rather than properties.
    
    Attributes:
        account_number: The public account number.
        account_holder: The public account holder name.
    
    Example:
        >>> account = BankAccount("12345", "Alice", 100.0)
        >>> account.get_balance()
        100.0
        >>> account.deposit(50.0)
        >>> account.get_balance()
        150.0
        >>> account.withdraw(30.0)
        >>> account.get_balance()
        120.0
    """
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0) -> None:
        """Initialize a bank account.
        
        Args:
            account_number: The unique account identifier.
            account_holder: The name of the account holder.
            initial_balance: The starting balance (default 0.0).
        """
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = float(initial_balance)  # Private attribute with name mangling
    
    def get_balance(self) -> float:
        """Get the current account balance.
        
        Returns:
            The current balance as a float.
        """
        return self.__balance
    
    def set_balance(self, new_balance: float) -> None:
        """Set the account balance directly.
        
        Args:
            new_balance: The new balance value.
        
        Raises:
            ValueError: If new_balance is negative.
        """
        if new_balance < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = float(new_balance)
    
    def deposit(self, amount: float) -> None:
        """Deposit money into the account.
        
        Args:
            amount: The amount to deposit.
        
        Raises:
            ValueError: If amount is negative or zero.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
    
    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account.
        
        Args:
            amount: The amount to withdraw.
        
        Raises:
            ValueError: If amount is negative, zero, or exceeds balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
