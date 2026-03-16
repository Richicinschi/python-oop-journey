"""Problem 10: Account Factory

Topic: Factory pattern with @classmethod
Difficulty: Medium

Create an Account base class and specialized account types using
the factory pattern with class methods.

Example:
    >>> # Create using factory method
    >>> savings = Account.create("savings", "SA-001", 1000, interest_rate=0.05)
    >>> savings.account_type
    'savings'
    >>> savings.apply_interest()
    >>> savings.balance
    1050.0
    >>> 
    >>> checking = Account.create("checking", "CH-001", 500, overdraft_limit=100)
    >>> checking.account_type
    'checking'
    >>> checking.withdraw(550)  # Within overdraft
    True
    >>> checking.balance
    -50
    >>> 
    >>> # List available account types
    >>> Account.get_account_types()
    ['savings', 'checking']
    >>> 
    >>> # Register new account type
    >>> class BusinessAccount(Account):
    ...     pass  # Implementation details
    >>> Account.register_account_type("business", BusinessAccount)
    >>> "business" in Account.get_account_types()
    True

Requirements:
    - Account base class with account_number and balance attributes
    - _account_types: class-level dict mapping type names to classes
    - create(cls, account_type: str, account_number: str, balance: float, **kwargs): classmethod factory
    - register_account_type(cls, name: str, class_type: type): classmethod
    - get_account_types(cls) -> list[str]: classmethod
    - SavingsAccount subclass with interest_rate and apply_interest() method
    - CheckingAccount subclass with overdraft_limit and withdraw(amount) -> bool method

Hints:
    - Hint 1: In create(), look up class in _account_types dict, then instantiate with **kwargs
    - Hint 2: Subclasses call super().__init__() and set account_type string
    - Hint 3: Register account types at module level AFTER class definitions
"""

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
        raise NotImplementedError("Implement __init__")
    
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
        raise NotImplementedError("Implement create")
    
    @classmethod
    def register_account_type(cls, name: str, class_type: type[Account]) -> None:
        """Register a new account type.
        
        Args:
            name: Account type name
            class_type: Class to instantiate for this type
        """
        raise NotImplementedError("Implement register_account_type")
    
    @classmethod
    def get_account_types(cls) -> list[str]:
        """Get list of registered account types.
        
        Returns:
            List of account type names
        """
        raise NotImplementedError("Implement get_account_types")


class SavingsAccount(Account):
    """Savings account with interest."""
    
    def __init__(self, account_number: str, balance: float, interest_rate: float = 0.0) -> None:
        """Initialize savings account.
        
        Args:
            account_number: Account number
            balance: Initial balance
            interest_rate: Annual interest rate (decimal)
        """
        raise NotImplementedError("Implement SavingsAccount __init__")
    
    def apply_interest(self) -> None:
        """Apply interest to the balance."""
        raise NotImplementedError("Implement apply_interest")


class CheckingAccount(Account):
    """Checking account with overdraft."""
    
    def __init__(self, account_number: str, balance: float, overdraft_limit: float = 0.0) -> None:
        """Initialize checking account.
        
        Args:
            account_number: Account number
            balance: Initial balance
            overdraft_limit: Maximum allowed overdraft
        """
        raise NotImplementedError("Implement CheckingAccount __init__")
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money if within overdraft limit.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if withdrawal succeeded, False otherwise
        """
        raise NotImplementedError("Implement withdraw")


# Register built-in account types
Account.register_account_type("savings", SavingsAccount)
Account.register_account_type("checking", CheckingAccount)
