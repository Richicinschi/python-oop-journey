"""Tests for Problem 06: Bank Branch."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_06_bank_branch import BankAccount


class TestInterestRate:
    """Test suite for interest rate class methods."""
    
    def setup_method(self) -> None:
        """Reset interest rate before each test."""
        BankAccount._interest_rate = 0.0
    
    def test_default_interest_rate(self) -> None:
        """Test default interest rate is 0."""
        assert BankAccount.get_interest_rate() == 0.0
    
    def test_set_interest_rate(self) -> None:
        """Test setting interest rate."""
        BankAccount.set_interest_rate(0.05)
        assert BankAccount.get_interest_rate() == 0.05
    
    def test_set_interest_rate_affects_all_accounts(self) -> None:
        """Test that interest rate is class-level."""
        acc1 = BankAccount("Alice", 1000)
        acc2 = BankAccount("Bob", 2000)
        BankAccount.set_interest_rate(0.10)
        assert acc1._interest_rate == 0.10
        assert acc2._interest_rate == 0.10


class TestApplyInterest:
    """Test suite for apply interest instance method."""
    
    def setup_method(self) -> None:
        """Reset interest rate before each test."""
        BankAccount._interest_rate = 0.0
    
    def test_apply_interest_zero_rate(self) -> None:
        """Test apply interest with zero rate."""
        acc = BankAccount("Alice", 1000)
        acc.apply_interest()
        assert acc.balance == 1000
    
    def test_apply_interest(self) -> None:
        """Test apply interest with non-zero rate."""
        BankAccount.set_interest_rate(0.05)
        acc = BankAccount("Alice", 1000)
        acc.apply_interest()
        assert acc.balance == 1050.0
    
    def test_apply_interest_multiple_times(self) -> None:
        """Test applying interest multiple times."""
        BankAccount.set_interest_rate(0.10)
        acc = BankAccount("Alice", 1000)
        acc.apply_interest()
        acc.apply_interest()
        assert acc.balance == 1210.0  # 1000 * 1.1 * 1.1


class TestIsValidAccountNumber:
    """Test suite for is_valid_account_number static method."""
    
    def test_valid_account_number(self) -> None:
        """Test valid account numbers."""
        assert BankAccount.is_valid_account_number("ACC-12345") is True
        assert BankAccount.is_valid_account_number("ACC-00000") is True
        assert BankAccount.is_valid_account_number("ACC-99999") is True
    
    def test_invalid_format(self) -> None:
        """Test invalid account number formats."""
        assert BankAccount.is_valid_account_number("INVALID") is False
        assert BankAccount.is_valid_account_number("ACC-1234") is False  # Too short
        assert BankAccount.is_valid_account_number("ACC-123456") is False  # Too long
        assert BankAccount.is_valid_account_number("acc-12345") is False  # Lowercase
        assert BankAccount.is_valid_account_number("ABC-12345") is False  # Wrong prefix
        assert BankAccount.is_valid_account_number("ACC-abcde") is False  # Non-digits
    
    def test_invalid_types(self) -> None:
        """Test invalid input types."""
        assert BankAccount.is_valid_account_number(12345) is False
        assert BankAccount.is_valid_account_number(None) is False


class TestCalculateFee:
    """Test suite for calculate_fee static method."""
    
    def test_calculate_fee(self) -> None:
        """Test fee calculation."""
        assert BankAccount.calculate_fee(500, 0.02) == 10.0
        assert BankAccount.calculate_fee(1000, 0.05) == 50.0
    
    def test_calculate_fee_zero(self) -> None:
        """Test fee calculation with zero values."""
        assert BankAccount.calculate_fee(0, 0.05) == 0.0
        assert BankAccount.calculate_fee(100, 0) == 0.0
    
    def test_calculate_fee_negative(self) -> None:
        """Test fee calculation with negative values."""
        assert BankAccount.calculate_fee(-100, 0.1) == -10.0
