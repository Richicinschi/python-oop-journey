"""Solution for Problem 10: Account Factory."""

from __future__ import annotations


class Account:
    """Base account class with factory pattern."""
    
    _account_types: dict[str, type[Account]] = {}
    
    def __init__(self, account_number: str, balance: float) -> None:
        """Initialize base account.
        
        Args:
            account_number: Unique account identifier
            balance: Initial balance
        """
        self.account_number = account_number
        self.balance = balance
        self.account_type = "base"
    
    @classmethod
    def create(
        cls,
        account_type: str,
        account_number: str,
        balance: float,
        **kwargs: float,
    ) -> Account:
        """Factory method to create account of specified type.
        
        Args:
            account_type: Type of account to create
            account_number: Account number
            balance: Initial balance
            **kwargs: Additional type-specific parameters
            
        Returns:
            New account instance
            
        Raises:
            ValueError: If account type is not registered
        """
        if account_type not in cls._account_types:
            raise ValueError(f"Unknown account type: {account_type}")
        
        account_class = cls._account_types[account_type]
        return account_class(account_number, balance, **kwargs)
    
    @classmethod
    def register_account_type(cls, name: str, class_type: type[Account]) -> None:
        """Register a new account type.
        
        Args:
            name: Account type name
            class_type: Class to instantiate for this type
        """
        cls._account_types[name] = class_type
    
    @classmethod
    def get_account_types(cls) -> list[str]:
        """Get list of registered account types.
        
        Returns:
            List of account type names
        """
        return list(cls._account_types.keys())


class SavingsAccount(Account):
    """Savings account with interest."""
    
    def __init__(self, account_number: str, balance: float, interest_rate: float = 0.0) -> None:
        """Initialize savings account.
        
        Args:
            account_number: Account number
            balance: Initial balance
            interest_rate: Annual interest rate (decimal)
        """
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate
        self.account_type = "savings"
    
    def apply_interest(self) -> None:
        """Apply interest to the balance."""
        interest = self.balance * self.interest_rate
        self.balance += interest


class CheckingAccount(Account):
    """Checking account with overdraft."""
    
    def __init__(self, account_number: str, balance: float, overdraft_limit: float = 0.0) -> None:
        """Initialize checking account.
        
        Args:
            account_number: Account number
            balance: Initial balance
            overdraft_limit: Maximum allowed overdraft
        """
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit
        self.account_type = "checking"
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money if within overdraft limit.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if withdrawal succeeded, False otherwise
        """
        if amount <= 0:
            return False
        new_balance = self.balance - amount
        if new_balance >= -self.overdraft_limit:
            self.balance = new_balance
            return True
        return False


# Register built-in account types
Account.register_account_type("savings", SavingsAccount)
Account.register_account_type("checking", CheckingAccount)
