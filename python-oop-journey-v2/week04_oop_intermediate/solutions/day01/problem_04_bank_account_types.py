"""Reference solution for Problem 04: Bank Account Types."""

from __future__ import annotations


class BankAccount:
    """Base class for bank accounts."""
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0) -> None:
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance
        self.account_type = "Generic"
    
    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self._balance += amount
        return True
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        return True
    
    def get_balance(self) -> float:
        return self._balance
    
    def get_account_info(self) -> str:
        return (f"Account: {self.account_number}, Holder: {self.account_holder}, "
                f"Type: {self.account_type}, Balance: ${self._balance:.2f}")
    
    def can_withdraw(self, amount: float) -> bool:
        return 0 < amount <= self._balance


class CheckingAccount(BankAccount):
    """A checking account with overdraft protection."""
    
    def __init__(self, account_number: str, account_holder: str, 
                 initial_balance: float = 0.0, overdraft_limit: float = 100.0,
                 free_transactions: int = 10, transaction_fee: float = 1.0) -> None:
        super().__init__(account_number, account_holder, initial_balance)
        self.account_type = "Checking"
        self.overdraft_limit = overdraft_limit
        self.free_transactions = free_transactions
        self.transaction_fee = transaction_fee
        self._transaction_count = 0
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            return False
        if self._balance - amount >= -self.overdraft_limit:
            self._balance -= amount
            self._transaction_count += 1
            return True
        return False
    
    def get_account_info(self) -> str:
        base = super().get_account_info()
        return f"{base}, Overdraft: ${self.overdraft_limit:.2f}"
    
    def can_withdraw(self, amount: float) -> bool:
        return amount > 0 and (self._balance - amount) >= -self.overdraft_limit
    
    def reset_transaction_count(self) -> None:
        self._transaction_count = 0


class SavingsAccount(BankAccount):
    """A savings account with interest and withdrawal limits."""
    
    def __init__(self, account_number: str, account_holder: str,
                 initial_balance: float = 0.0, interest_rate: float = 0.02,
                 withdrawal_limit: int = 6, minimum_balance: float = 100.0) -> None:
        super().__init__(account_number, account_holder, initial_balance)
        self.account_type = "Savings"
        self.interest_rate = interest_rate
        self.withdrawal_limit = withdrawal_limit
        self.minimum_balance = minimum_balance
        self._withdrawal_count = 0
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            return False
        if self._withdrawal_count >= self.withdrawal_limit:
            return False
        if self._balance - amount < self.minimum_balance:
            return False
        self._balance -= amount
        self._withdrawal_count += 1
        return True
    
    def get_account_info(self) -> str:
        base = super().get_account_info()
        return f"{base}, Interest: {self.interest_rate*100:.1f}%"
    
    def can_withdraw(self, amount: float) -> bool:
        return (amount > 0 and 
                self._withdrawal_count < self.withdrawal_limit and
                self._balance - amount >= self.minimum_balance)
    
    def apply_interest(self) -> float:
        monthly_rate = self.interest_rate / 12
        interest = self._balance * monthly_rate
        self._balance += interest
        return interest
    
    def reset_withdrawal_count(self) -> None:
        self._withdrawal_count = 0
