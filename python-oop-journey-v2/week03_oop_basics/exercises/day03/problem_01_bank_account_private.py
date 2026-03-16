"""Exercise: Bank Account Private.

Implement a BankAccount class with private balance attribute and
getter/setter methods.

TODO:
1. Create a __balance private attribute (use name mangling)
2. Implement get_balance() method to return the balance
3. Implement set_balance() method with validation (no negative balances)
4. Implement deposit() and withdraw() methods
"""

from __future__ import annotations


class BankAccount:
    """A bank account with private balance attribute.
    
    Attributes:
        account_number: The public account number.
        account_holder: The public account holder name.
    """
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0) -> None:
        """Initialize a bank account."""
        self.account_number = account_number
        self.account_holder = account_holder
        # TODO: Create a private __balance attribute
        raise NotImplementedError("Initialize the private __balance attribute")
    
    def get_balance(self) -> float:
        """Get the current account balance."""
        # TODO: Return the balance
        raise NotImplementedError("Return the private balance")
    
    def set_balance(self, new_balance: float) -> None:
        """Set the account balance directly with validation."""
        # TODO: Validate that new_balance is not negative
        # TODO: Set the private __balance attribute
        raise NotImplementedError("Set the balance with validation")
    
    def deposit(self, amount: float) -> None:
        """Deposit money into the account."""
        # TODO: Validate amount is positive
        # TODO: Add amount to balance
        raise NotImplementedError("Implement deposit method")
    
    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account."""
        # TODO: Validate amount is positive and doesn't exceed balance
        # TODO: Subtract amount from balance
        raise NotImplementedError("Implement withdraw method")
