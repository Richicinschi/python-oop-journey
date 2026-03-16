"""Tests for Problem 04: Bank Account Types."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_04_bank_account_types import (
    BankAccount, CheckingAccount, SavingsAccount
)


class TestBankAccount:
    """Tests for the base BankAccount class."""
    
    def test_account_init(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.account_number == "ACC001"
        assert account.account_holder == "John Doe"
        assert account.get_balance() == 1000.0
    
    def test_account_init_default_balance(self) -> None:
        account = BankAccount("ACC001", "John Doe")
        assert account.get_balance() == 0.0
    
    def test_account_deposit_success(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.deposit(500.0) is True
        assert account.get_balance() == 1500.0
    
    def test_account_deposit_zero(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.deposit(0.0) is False
        assert account.get_balance() == 1000.0
    
    def test_account_deposit_negative(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.deposit(-100.0) is False
        assert account.get_balance() == 1000.0
    
    def test_account_withdraw_success(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.withdraw(300.0) is True
        assert account.get_balance() == 700.0
    
    def test_account_withdraw_insufficient_funds(self) -> None:
        account = BankAccount("ACC001", "John Doe", 100.0)
        assert account.withdraw(200.0) is False
        assert account.get_balance() == 100.0
    
    def test_account_withdraw_zero(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.withdraw(0.0) is False
    
    def test_account_withdraw_negative(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.withdraw(-100.0) is False
    
    def test_account_get_info(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        info = account.get_account_info()
        assert "ACC001" in info
        assert "John Doe" in info
        assert "$1000.00" in info
    
    def test_account_can_withdraw_true(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.can_withdraw(500.0) is True
    
    def test_account_can_withdraw_false(self) -> None:
        account = BankAccount("ACC001", "John Doe", 1000.0)
        assert account.can_withdraw(1500.0) is False


class TestCheckingAccount:
    """Tests for the CheckingAccount class."""
    
    def test_checking_inheritance(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe")
        assert isinstance(checking, BankAccount)
    
    def test_checking_init(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe", 500.0, 200.0)
        assert checking.overdraft_limit == 200.0
        assert checking.get_balance() == 500.0
    
    def test_checking_account_type(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe")
        info = checking.get_account_info()
        assert "Type: Checking" in info
    
    def test_checking_withdraw_within_balance(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe", 1000.0, 200.0)
        assert checking.withdraw(500.0) is True
        assert checking.get_balance() == 500.0
    
    def test_checking_withdraw_with_overdraft(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe", 100.0, 200.0)
        assert checking.withdraw(200.0) is True
        assert checking.get_balance() == -100.0
    
    def test_checking_withdraw_over_overdraft_limit(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe", 100.0, 200.0)
        assert checking.withdraw(350.0) is False
        assert checking.get_balance() == 100.0
    
    def test_checking_can_withdraw_with_overdraft(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe", 100.0, 200.0)
        assert checking.can_withdraw(250.0) is True  # Within overdraft
        assert checking.can_withdraw(350.0) is False  # Exceeds overdraft
    
    def test_checking_get_info_includes_overdraft(self) -> None:
        checking = CheckingAccount("CHK001", "Jane Doe", 1000.0, 200.0)
        info = checking.get_account_info()
        assert "Overdraft: $200.00" in info


class TestSavingsAccount:
    """Tests for the SavingsAccount class."""
    
    def test_savings_inheritance(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith")
        assert isinstance(savings, BankAccount)
    
    def test_savings_init(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 5000.0, 0.03)
        assert savings.interest_rate == 0.03
        assert savings.minimum_balance == 100.0
    
    def test_savings_account_type(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith")
        info = savings.get_account_info()
        assert "Type: Savings" in info
    
    def test_savings_get_info_includes_interest(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 5000.0, 0.025)
        info = savings.get_account_info()
        assert "Interest: 2.5%" in info
    
    def test_savings_withdraw_within_limits(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 1000.0)
        assert savings.withdraw(500.0) is True
        assert savings.get_balance() == 500.0
    
    def test_savings_withdraw_below_minimum(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 500.0, minimum_balance=100.0)
        assert savings.withdraw(450.0) is False  # Would go below $100 minimum
        assert savings.get_balance() == 500.0
    
    def test_savings_withdraw_limit_enforced(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 10000.0, withdrawal_limit=6)
        # Make 6 withdrawals
        for _ in range(6):
            assert savings.withdraw(100.0) is True
        # 7th should fail
        assert savings.withdraw(100.0) is False
    
    def test_savings_can_withdraw_considers_limits(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 1000.0, withdrawal_limit=6)
        assert savings.can_withdraw(500.0) is True
        # Make 6 withdrawals
        for _ in range(6):
            savings.withdraw(10.0)
        assert savings.can_withdraw(10.0) is False  # Limit reached
    
    def test_savings_apply_interest(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 1200.0, interest_rate=0.12)  # 12% annual
        interest = savings.apply_interest()  # Should be 1% monthly = $12
        assert interest == pytest.approx(12.0, rel=0.01)
        assert savings.get_balance() == pytest.approx(1212.0, rel=0.01)
    
    def test_savings_reset_withdrawal_count(self) -> None:
        savings = SavingsAccount("SAV001", "Bob Smith", 10000.0, withdrawal_limit=2)
        savings.withdraw(100.0)
        savings.withdraw(100.0)
        assert savings.can_withdraw(100.0) is False
        savings.reset_withdrawal_count()
        assert savings.can_withdraw(100.0) is True


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_accounts(self) -> None:
        accounts: list[BankAccount] = [
            BankAccount("ACC001", "Test", 1000.0),
            CheckingAccount("CHK001", "Test", 1000.0),
            SavingsAccount("SAV001", "Test", 1000.0)
        ]
        
        # All can have deposits
        for account in accounts:
            balance_before = account.get_balance()
            account.deposit(100.0)
            assert account.get_balance() == balance_before + 100.0
    
    def test_polymorphic_withdrawal_behavior(self) -> None:
        """Different account types have different withdrawal rules."""
        basic = BankAccount("ACC001", "Test", 100.0)
        checking = CheckingAccount("CHK001", "Test", 100.0, 200.0)  # $200 overdraft
        savings = SavingsAccount("SAV001", "Test", 1000.0, minimum_balance=100.0)
        
        # Basic can't withdraw more than balance
        assert basic.withdraw(150.0) is False
        
        # Checking can overdraft
        assert checking.withdraw(150.0) is True
        
        # Savings must maintain minimum
        assert savings.withdraw(950.0) is False  # Would go below $100 minimum
