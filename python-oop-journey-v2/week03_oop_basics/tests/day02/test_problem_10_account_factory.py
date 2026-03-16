"""Tests for Problem 10: Account Factory."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_10_account_factory import (
    Account,
    SavingsAccount,
    CheckingAccount,
)


class TestAccountBase:
    """Test suite for Account base class."""
    
    def setup_method(self) -> None:
        """Reset registry before each test."""
        Account._account_types.clear()
        Account.register_account_type("savings", SavingsAccount)
        Account.register_account_type("checking", CheckingAccount)
    
    def test_register_account_type(self) -> None:
        """Test registering account types."""
        # Already registered in setup, verify they exist
        assert "savings" in Account.get_account_types()
        assert "checking" in Account.get_account_types()
    
    def test_get_account_types(self) -> None:
        """Test getting account type list."""
        types = Account.get_account_types()
        assert isinstance(types, list)
        assert "savings" in types
        assert "checking" in types


class TestAccountFactory:
    """Test suite for Account factory method."""
    
    def setup_method(self) -> None:
        """Reset registry before each test."""
        Account._account_types.clear()
        Account.register_account_type("savings", SavingsAccount)
        Account.register_account_type("checking", CheckingAccount)
    
    def test_create_savings(self) -> None:
        """Test creating savings account."""
        acc = Account.create("savings", "SA-001", 1000, interest_rate=0.05)
        assert isinstance(acc, SavingsAccount)
        assert acc.account_number == "SA-001"
        assert acc.balance == 1000
        assert acc.interest_rate == 0.05
    
    def test_create_checking(self) -> None:
        """Test creating checking account."""
        acc = Account.create("checking", "CH-001", 500, overdraft_limit=100)
        assert isinstance(acc, CheckingAccount)
        assert acc.account_number == "CH-001"
        assert acc.balance == 500
        assert acc.overdraft_limit == 100
    
    def test_create_unknown_type_raises(self) -> None:
        """Test creating unknown account type raises ValueError."""
        with pytest.raises(ValueError):
            Account.create("unknown", "X-001", 100)


class TestSavingsAccount:
    """Test suite for SavingsAccount."""
    
    def test_savings_init(self) -> None:
        """Test savings account initialization."""
        acc = SavingsAccount("SA-001", 1000, interest_rate=0.05)
        assert acc.account_number == "SA-001"
        assert acc.balance == 1000
        assert acc.interest_rate == 0.05
        assert acc.account_type == "savings"
    
    def test_apply_interest(self) -> None:
        """Test applying interest."""
        acc = SavingsAccount("SA-001", 1000, interest_rate=0.05)
        acc.apply_interest()
        assert acc.balance == 1050.0
    
    def test_apply_interest_zero_rate(self) -> None:
        """Test applying zero interest."""
        acc = SavingsAccount("SA-001", 1000, interest_rate=0.0)
        acc.apply_interest()
        assert acc.balance == 1000


class TestCheckingAccount:
    """Test suite for CheckingAccount."""
    
    def test_checking_init(self) -> None:
        """Test checking account initialization."""
        acc = CheckingAccount("CH-001", 500, overdraft_limit=100)
        assert acc.account_number == "CH-001"
        assert acc.balance == 500
        assert acc.overdraft_limit == 100
        assert acc.account_type == "checking"
    
    def test_withdraw_success(self) -> None:
        """Test successful withdrawal."""
        acc = CheckingAccount("CH-001", 500, overdraft_limit=100)
        result = acc.withdraw(300)
        assert result is True
        assert acc.balance == 200
    
    def test_withdraw_to_overdraft_limit(self) -> None:
        """Test withdrawal to overdraft limit."""
        acc = CheckingAccount("CH-001", 500, overdraft_limit=100)
        result = acc.withdraw(600)  # Go to -100
        assert result is True
        assert acc.balance == -100
    
    def test_withdraw_exceeds_overdraft(self) -> None:
        """Test withdrawal exceeding overdraft limit."""
        acc = CheckingAccount("CH-001", 500, overdraft_limit=100)
        result = acc.withdraw(601)  # Would go to -101
        assert result is False
        assert acc.balance == 500  # Unchanged
    
    def test_withdraw_zero_amount(self) -> None:
        """Test withdrawal of zero amount."""
        acc = CheckingAccount("CH-001", 500, overdraft_limit=100)
        result = acc.withdraw(0)
        assert result is False
        assert acc.balance == 500
    
    def test_withdraw_negative_amount(self) -> None:
        """Test withdrawal of negative amount."""
        acc = CheckingAccount("CH-001", 500, overdraft_limit=100)
        result = acc.withdraw(-100)
        assert result is False
        assert acc.balance == 500


class TestCustomAccountType:
    """Test suite for registering custom account types."""
    
    def setup_method(self) -> None:
        """Reset registry before each test."""
        Account._account_types.clear()
        Account.register_account_type("savings", SavingsAccount)
        Account.register_account_type("checking", CheckingAccount)
    
    def test_register_custom_type(self) -> None:
        """Test registering a custom account type."""
        class BusinessAccount(Account):
            def __init__(self, account_number: str, balance: float) -> None:
                super().__init__(account_number, balance)
                self.account_type = "business"
        
        Account.register_account_type("business", BusinessAccount)
        assert "business" in Account.get_account_types()
        
        acc = Account.create("business", "B-001", 5000)
        assert isinstance(acc, BusinessAccount)
