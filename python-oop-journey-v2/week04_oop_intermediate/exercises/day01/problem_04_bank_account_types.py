"""Problem 04: Bank Account Types

Topic: Method Overriding with Business Logic
Difficulty: Medium

Create a BankAccount base class with CheckingAccount and SavingsAccount subclasses,
demonstrating different behaviors and business rules.
"""

from __future__ import annotations


class BankAccount:
    """Base class for bank accounts.
    
    Attributes:
        account_number: Unique account identifier
        account_holder: Name of account holder
        balance: Current account balance
        account_type: Type of account (for identification)
    """
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0) -> None:
        """Initialize a BankAccount.
        
        Args:
            account_number: Unique account identifier
            account_holder: Name of account holder
            initial_balance: Starting balance (default 0.0)
        """
        raise NotImplementedError("Implement BankAccount.__init__")
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Returns:
            True if successful, False if amount <= 0
        """
        raise NotImplementedError("Implement BankAccount.deposit")
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw (must be positive and <= balance)
            
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Implement BankAccount.withdraw")
    
    def get_balance(self) -> float:
        """Return current balance.
        
        Returns:
            Current account balance
        """
        raise NotImplementedError("Implement BankAccount.get_balance")
    
    def get_account_info(self) -> str:
        """Return account information.
        
        Returns:
            String: "Account: X, Holder: Y, Type: Z, Balance: $W"
        """
        raise NotImplementedError("Implement BankAccount.get_account_info")
    
    def can_withdraw(self, amount: float) -> bool:
        """Check if withdrawal is possible without performing it.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if withdrawal would succeed
        """
        raise NotImplementedError("Implement BankAccount.can_withdraw")


class CheckingAccount(BankAccount):
    """A checking account with overdraft protection.
    
    Additional Attributes:
        overdraft_limit: Maximum overdraft allowed (negative balance limit)
        transaction_count: Number of transactions this month
        free_transactions: Number of free transactions per month
        transaction_fee: Fee per transaction after free limit
    """
    
    def __init__(self, account_number: str, account_holder: str, 
                 initial_balance: float = 0.0, overdraft_limit: float = 100.0,
                 free_transactions: int = 10, transaction_fee: float = 1.0) -> None:
        """Initialize a CheckingAccount.
        
        Args:
            account_number: Unique account identifier
            account_holder: Name of account holder
            initial_balance: Starting balance
            overdraft_limit: Maximum negative balance allowed
            free_transactions: Number of free transactions per month
            transaction_fee: Fee charged after free transactions exceeded
        """
        raise NotImplementedError("Implement CheckingAccount.__init__")
    
    def withdraw(self, amount: float) -> bool:
        """Override: Allow withdrawals up to overdraft limit.
        
        Can withdraw if: balance - amount >= -overdraft_limit
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if withdrawal succeeds (including overdraft)
        """
        raise NotImplementedError("Implement CheckingAccount.withdraw")
    
    def get_account_info(self) -> str:
        """Override: Include overdraft information.
        
        Returns:
            Base info + ", Overdraft: $X"
        """
        raise NotImplementedError("Implement CheckingAccount.get_account_info")
    
    def can_withdraw(self, amount: float) -> bool:
        """Override: Check against overdraft limit.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if balance - amount >= -overdraft_limit
        """
        raise NotImplementedError("Implement CheckingAccount.can_withdraw")
    
    def reset_transaction_count(self) -> None:
        """Reset monthly transaction count (call at month end).
        
        Sets transaction_count back to 0.
        """
        raise NotImplementedError("Implement CheckingAccount.reset_transaction_count")


class SavingsAccount(BankAccount):
    """A savings account with interest and withdrawal limits.
    
    Additional Attributes:
        interest_rate: Annual interest rate as decimal
        withdrawal_limit: Maximum withdrawals per month
        withdrawal_count: Withdrawals made this month
        minimum_balance: Minimum required balance
    """
    
    def __init__(self, account_number: str, account_holder: str,
                 initial_balance: float = 0.0, interest_rate: float = 0.02,
                 withdrawal_limit: int = 6, minimum_balance: float = 100.0) -> None:
        """Initialize a SavingsAccount.
        
        Args:
            account_number: Unique account identifier
            account_holder: Name of account holder
            initial_balance: Starting balance
            interest_rate: Annual interest as decimal (e.g., 0.02 = 2%)
            withdrawal_limit: Maximum withdrawals per month
            minimum_balance: Minimum balance that must be maintained
        """
        raise NotImplementedError("Implement SavingsAccount.__init__")
    
    def withdraw(self, amount: float) -> bool:
        """Override: Enforce withdrawal limits and minimum balance.
        
        Can only withdraw if:
        - withdrawal_count < withdrawal_limit
        - balance - amount >= minimum_balance
        - amount > 0
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if all conditions met
        """
        raise NotImplementedError("Implement SavingsAccount.withdraw")
    
    def get_account_info(self) -> str:
        """Override: Include interest rate.
        
        Returns:
            Base info + ", Interest: X%"
        """
        raise NotImplementedError("Implement SavingsAccount.get_account_info")
    
    def can_withdraw(self, amount: float) -> bool:
        """Override: Check withdrawal limits.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if withdrawal_count < limit AND balance - amount >= minimum_balance
        """
        raise NotImplementedError("Implement SavingsAccount.can_withdraw")
    
    def apply_interest(self) -> float:
        """Apply monthly interest to the account.
        
        Calculates and adds one month's interest.
        
        Returns:
            Interest amount added
        """
        raise NotImplementedError("Implement SavingsAccount.apply_interest")
    
    def reset_withdrawal_count(self) -> None:
        """Reset monthly withdrawal count.
        
        Sets withdrawal_count back to 0.
        """
        raise NotImplementedError("Implement SavingsAccount.reset_withdrawal_count")
