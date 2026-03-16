"""Solution for Problem 08: Savings Account Limits.

Demonstrates multiple properties with validation and interdependent rules.
"""

from __future__ import annotations


class SavingsAccount:
    """A savings account with multiple validated properties.
    
    This class demonstrates complex validation with interdependent
    properties like minimum balance and withdrawal limits.
    
    Attributes:
        account_number: The account identifier (read-only).
        account_holder: The name of the account holder.
    
    Example:
        >>> account = SavingsAccount("SA001", "Alice", 1000.0)
        >>> account.balance
        1000.0
        >>> account.withdraw(500)
        True
        >>> account.balance
        500.0
    """
    
    DEFAULT_MIN_BALANCE = 100.0
    DEFAULT_DAILY_WITHDRAWAL_LIMIT = 500.0
    
    def __init__(
        self,
        account_number: str,
        account_holder: str,
        initial_balance: float = 0.0,
        min_balance: float | None = None,
    ) -> None:
        """Initialize a savings account.
        
        Args:
            account_number: The unique account identifier.
            account_holder: The name of the account holder.
            initial_balance: The starting balance.
            min_balance: The minimum required balance (default: 100.0).
        
        Raises:
            TypeError: If types are incorrect.
            ValueError: If initial balance is below minimum.
        """
        if not isinstance(account_number, str):
            raise TypeError("Account number must be a string")
        if not account_number.strip():
            raise ValueError("Account number cannot be empty")
        self._account_number = account_number.strip()
        
        self.account_holder = account_holder  # Use setter
        
        self._min_balance = min_balance if min_balance is not None else self.DEFAULT_MIN_BALANCE
        if self._min_balance < 0:
            raise ValueError("Minimum balance cannot be negative")
        
        self._daily_withdrawal_limit = self.DEFAULT_DAILY_WITHDRAWAL_LIMIT
        self._daily_withdrawn = 0.0
        
        self._balance = 0.0
        self.balance = initial_balance  # Use setter for validation
    
    @property
    def account_number(self) -> str:
        """Get the account number.
        
        Returns:
            The account number.
        """
        return self._account_number
    
    @property
    def account_holder(self) -> str:
        """Get the account holder name.
        
        Returns:
            The account holder name.
        """
        return self._account_holder
    
    @account_holder.setter
    def account_holder(self, value: str) -> None:
        """Set the account holder name.
        
        Args:
            value: The new account holder name.
        
        Raises:
            TypeError: If value is not a string.
            ValueError: If name is empty.
        """
        if not isinstance(value, str):
            raise TypeError("Account holder must be a string")
        if not value.strip():
            raise ValueError("Account holder cannot be empty")
        self._account_holder = value.strip()
    
    @property
    def balance(self) -> float:
        """Get the current balance.
        
        Returns:
            The current account balance.
        """
        return self._balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        """Set the balance with minimum balance validation.
        
        Args:
            value: The new balance.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If balance would be below minimum.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Balance must be a number")
        if value < self._min_balance:
            raise ValueError(
                f"Balance cannot be below minimum ({self._min_balance})"
            )
        self._balance = float(value)
    
    @property
    def min_balance(self) -> float:
        """Get the minimum required balance.
        
        Returns:
            The minimum balance requirement.
        """
        return self._min_balance
    
    @min_balance.setter
    def min_balance(self, value: float) -> None:
        """Set the minimum required balance.
        
        Args:
            value: The new minimum balance.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If value is negative or would make current balance invalid.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Minimum balance must be a number")
        if value < 0:
            raise ValueError("Minimum balance cannot be negative")
        if self._balance < value:
            raise ValueError(
                f"Cannot set minimum balance to {value} - current balance is {self._balance}"
            )
        self._min_balance = float(value)
    
    @property
    def available_to_withdraw(self) -> float:
        """Calculate available withdrawal amount (read-only).
        
        Returns:
            The amount that can be withdrawn while respecting limits.
        """
        max_by_balance = self._balance - self._min_balance
        max_by_daily = self._daily_withdrawal_limit - self._daily_withdrawn
        return max(0.0, min(max_by_balance, max_by_daily))
    
    @property
    def daily_withdrawal_limit(self) -> float:
        """Get the daily withdrawal limit.
        
        Returns:
            The maximum that can be withdrawn per day.
        """
        return self._daily_withdrawal_limit
    
    @daily_withdrawal_limit.setter
    def daily_withdrawal_limit(self, value: float) -> None:
        """Set the daily withdrawal limit.
        
        Args:
            value: The new daily limit.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If value is negative.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Daily limit must be a number")
        if value < 0:
            raise ValueError("Daily limit cannot be negative")
        self._daily_withdrawal_limit = float(value)
    
    def deposit(self, amount: float) -> None:
        """Deposit money into the account.
        
        Args:
            amount: The amount to deposit.
        
        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money if limits allow.
        
        Args:
            amount: The amount to withdraw.
        
        Returns:
            True if withdrawal succeeded, False if would violate limits.
        
        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.available_to_withdraw:
            return False
        self._balance -= amount
        self._daily_withdrawn += amount
        return True
    
    def reset_daily_limit(self) -> None:
        """Reset the daily withdrawal counter (call at day change)."""
        self._daily_withdrawn = 0.0
