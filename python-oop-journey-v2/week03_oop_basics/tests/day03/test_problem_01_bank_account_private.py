"""Tests for Problem 01: Bank Account Private."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_01_bank_account_private import (
    BankAccount,
)


class TestBankAccount:
    """Test suite for BankAccount class."""
    
    def test_initialization(self) -> None:
        """Test account initialization."""
        account = BankAccount("12345", "Alice", 100.0)
        assert account.account_number == "12345"
        assert account.account_holder == "Alice"
        assert account.get_balance() == 100.0
    
    def test_initialization_default_balance(self) -> None:
        """Test account initialization with default balance."""
        account = BankAccount("12345", "Alice")
        assert account.get_balance() == 0.0
    
    def test_get_balance(self) -> None:
        """Test get_balance method."""
        account = BankAccount("12345", "Alice", 500.0)
        assert account.get_balance() == 500.0
    
    def test_set_balance_valid(self) -> None:
        """Test set_balance with valid value."""
        account = BankAccount("12345", "Alice", 100.0)
        account.set_balance(200.0)
        assert account.get_balance() == 200.0
    
    def test_set_balance_zero(self) -> None:
        """Test set_balance with zero."""
        account = BankAccount("12345", "Alice", 100.0)
        account.set_balance(0.0)
        assert account.get_balance() == 0.0
    
    def test_set_balance_negative_raises(self) -> None:
        """Test set_balance with negative value raises ValueError."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(ValueError, match="cannot be negative"):
            account.set_balance(-50.0)
    
    def test_deposit_valid(self) -> None:
        """Test deposit with valid amount."""
        account = BankAccount("12345", "Alice", 100.0)
        account.deposit(50.0)
        assert account.get_balance() == 150.0
    
    def test_deposit_multiple(self) -> None:
        """Test multiple deposits."""
        account = BankAccount("12345", "Alice", 0.0)
        account.deposit(10.0)
        account.deposit(20.0)
        account.deposit(30.0)
        assert account.get_balance() == 60.0
    
    def test_deposit_negative_raises(self) -> None:
        """Test deposit with negative amount raises ValueError."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(ValueError, match="positive"):
            account.deposit(-10.0)
    
    def test_deposit_zero_raises(self) -> None:
        """Test deposit with zero amount raises ValueError."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(ValueError, match="positive"):
            account.deposit(0.0)
    
    def test_withdraw_valid(self) -> None:
        """Test withdraw with valid amount."""
        account = BankAccount("12345", "Alice", 100.0)
        account.withdraw(40.0)
        assert account.get_balance() == 60.0
    
    def test_withdraw_full_balance(self) -> None:
        """Test withdrawing entire balance."""
        account = BankAccount("12345", "Alice", 100.0)
        account.withdraw(100.0)
        assert account.get_balance() == 0.0
    
    def test_withdraw_insufficient_funds_raises(self) -> None:
        """Test withdraw with insufficient funds raises ValueError."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(ValueError, match="Insufficient"):
            account.withdraw(150.0)
    
    def test_withdraw_negative_raises(self) -> None:
        """Test withdraw with negative amount raises ValueError."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(ValueError, match="positive"):
            account.withdraw(-10.0)
    
    def test_withdraw_zero_raises(self) -> None:
        """Test withdraw with zero amount raises ValueError."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(ValueError, match="positive"):
            account.withdraw(0.0)
    
    def test_private_attribute_inaccessible(self) -> None:
        """Test that __balance is name-mangled and inaccessible."""
        account = BankAccount("12345", "Alice", 100.0)
        with pytest.raises(AttributeError):
            _ = account.__balance  # type: ignore
    
    def test_private_attribute_accessible_via_mangling(self) -> None:
        """Test that __balance is accessible via name mangling."""
        account = BankAccount("12345", "Alice", 100.0)
        # Name mangling makes it _BankAccount__balance
        assert account._BankAccount__balance == 100.0
