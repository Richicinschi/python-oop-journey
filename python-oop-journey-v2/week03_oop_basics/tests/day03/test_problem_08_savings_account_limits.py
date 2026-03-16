"""Tests for Problem 08: Savings Account Limits."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_08_savings_account_limits import (
    SavingsAccount,
)


class TestSavingsAccount:
    """Test suite for SavingsAccount class."""
    
    def test_initialization(self) -> None:
        """Test account initialization."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        assert account.account_number == "SA001"
        assert account.account_holder == "Alice"
        assert account.balance == 1000.0
        assert account.min_balance == 100.0  # Default
    
    def test_initialization_custom_min_balance(self) -> None:
        """Test initialization with custom min balance."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 200.0)
        assert account.min_balance == 200.0
    
    def test_initialization_below_min_balance_raises(self) -> None:
        """Test initialization below minimum balance raises."""
        with pytest.raises(ValueError, match="minimum"):
            SavingsAccount("SA001", "Alice", 50.0)  # Default min is 100
    
    def test_account_number_read_only(self) -> None:
        """Test that account_number is read-only."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(AttributeError):
            account.account_number = "SA002"  # type: ignore
    
    def test_account_holder_setter_valid(self) -> None:
        """Test account_holder setter with valid value."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        account.account_holder = "Bob"
        assert account.account_holder == "Bob"
    
    def test_account_holder_setter_empty_raises(self) -> None:
        """Test account_holder setter with empty value raises."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="empty"):
            account.account_holder = ""
    
    def test_balance_getter(self) -> None:
        """Test balance getter."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        assert account.balance == 1000.0
    
    def test_balance_setter_valid(self) -> None:
        """Test balance setter with valid value."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        account.balance = 1500.0
        assert account.balance == 1500.0
    
    def test_balance_setter_at_min(self) -> None:
        """Test balance setter at minimum balance."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        account.balance = 100.0  # At default minimum
        assert account.balance == 100.0
    
    def test_balance_setter_below_min_raises(self) -> None:
        """Test balance setter below minimum raises ValueError."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="minimum"):
            account.balance = 50.0
    
    def test_min_balance_getter(self) -> None:
        """Test min_balance getter."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        assert account.min_balance == 100.0
    
    def test_min_balance_setter_valid(self) -> None:
        """Test min_balance setter with valid value."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        account.min_balance = 200.0
        assert account.min_balance == 200.0
    
    def test_min_balance_setter_negative_raises(self) -> None:
        """Test min_balance setter with negative raises ValueError."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="negative"):
            account.min_balance = -100.0
    
    def test_min_balance_setter_above_balance_raises(self) -> None:
        """Test min_balance setter above current balance raises."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="current balance"):
            account.min_balance = 1500.0
    
    def test_available_to_withdraw(self) -> None:
        """Test available_to_withdraw calculation."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 100.0)
        # Balance 1000, min 100, daily limit 500
        # Available: min(1000-100, 500-0) = 500
        assert account.available_to_withdraw == 500.0
    
    def test_available_to_withdraw_limited_by_balance(self) -> None:
        """Test available limited by balance not daily limit."""
        account = SavingsAccount("SA001", "Alice", 300.0, 100.0)
        # Balance 300, min 100, so max by balance is 200
        assert account.available_to_withdraw == 200.0
    
    def test_available_to_withdraw_after_withdrawal(self) -> None:
        """Test available decreases after withdrawal."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 100.0)
        account.withdraw(200.0)
        # Daily withdrawn: 200, so remaining: 500-200 = 300
        assert account.available_to_withdraw == 300.0
    
    def test_deposit(self) -> None:
        """Test deposit method."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        account.deposit(500.0)
        assert account.balance == 1500.0
    
    def test_deposit_negative_raises(self) -> None:
        """Test deposit with negative amount raises."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="positive"):
            account.deposit(-100.0)
    
    def test_deposit_zero_raises(self) -> None:
        """Test deposit with zero raises."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="positive"):
            account.deposit(0.0)
    
    def test_withdraw_success(self) -> None:
        """Test successful withdrawal."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 100.0)
        result = account.withdraw(200.0)
        assert result is True
        assert account.balance == 800.0
    
    def test_withdraw_failure_insufficient_funds(self) -> None:
        """Test withdrawal failure due to minimum balance."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 100.0)
        result = account.withdraw(950.0)  # Would leave 50 < min 100
        assert result is False
        assert account.balance == 1000.0  # Unchanged
    
    def test_withdraw_failure_daily_limit(self) -> None:
        """Test withdrawal failure due to daily limit."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 100.0)
        account.withdraw(400.0)  # OK
        result = account.withdraw(200.0)  # Would exceed 500 limit
        assert result is False
    
    def test_withdraw_negative_raises(self) -> None:
        """Test withdraw with negative amount raises."""
        account = SavingsAccount("SA001", "Alice", 1000.0)
        with pytest.raises(ValueError, match="positive"):
            account.withdraw(-100.0)
    
    def test_reset_daily_limit(self) -> None:
        """Test reset_daily_limit method."""
        account = SavingsAccount("SA001", "Alice", 1000.0, 100.0)
        account.withdraw(400.0)
        assert account.available_to_withdraw == 100.0  # 500-400
        account.reset_daily_limit()
        assert account.available_to_withdraw == 500.0  # Reset to full
