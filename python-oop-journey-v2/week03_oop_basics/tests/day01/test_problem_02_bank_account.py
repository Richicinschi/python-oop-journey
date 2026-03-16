"""Tests for Problem 02: Bank Account."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_02_bank_account import BankAccount


def test_account_creation_with_default_balance() -> None:
    """Test creating an account with default balance."""
    account = BankAccount("John Doe")
    assert account.owner == "John Doe"
    assert account.get_balance() == 0.0


def test_account_creation_with_initial_balance() -> None:
    """Test creating an account with initial balance."""
    account = BankAccount("Jane Doe", 100.0)
    assert account.owner == "Jane Doe"
    assert account.get_balance() == 100.0


def test_deposit_positive_amount() -> None:
    """Test depositing a positive amount."""
    account = BankAccount("John", 100.0)
    new_balance = account.deposit(50.0)
    assert new_balance == 150.0
    assert account.get_balance() == 150.0


def test_deposit_negative_amount() -> None:
    """Test that depositing negative amount is rejected."""
    account = BankAccount("John", 100.0)
    new_balance = account.deposit(-50.0)
    assert new_balance == 100.0  # Balance unchanged


def test_deposit_zero() -> None:
    """Test that depositing zero is rejected."""
    account = BankAccount("John", 100.0)
    new_balance = account.deposit(0.0)
    assert new_balance == 100.0  # Balance unchanged


def test_withdraw_sufficient_funds() -> None:
    """Test withdrawing with sufficient funds."""
    account = BankAccount("John", 100.0)
    new_balance = account.withdraw(30.0)
    assert new_balance == 70.0
    assert account.get_balance() == 70.0


def test_withdraw_insufficient_funds() -> None:
    """Test withdrawing with insufficient funds."""
    account = BankAccount("John", 100.0)
    result = account.withdraw(150.0)
    assert result is None
    assert account.get_balance() == 100.0  # Balance unchanged


def test_withdraw_exact_amount() -> None:
    """Test withdrawing the exact balance."""
    account = BankAccount("John", 100.0)
    new_balance = account.withdraw(100.0)
    assert new_balance == 0.0


def test_withdraw_negative_amount() -> None:
    """Test that withdrawing negative amount is rejected."""
    account = BankAccount("John", 100.0)
    result = account.withdraw(-50.0)
    assert result is None
    assert account.get_balance() == 100.0


def test_multiple_transactions() -> None:
    """Test multiple deposits and withdrawals."""
    account = BankAccount("John", 100.0)
    account.deposit(50.0)
    account.withdraw(30.0)
    account.deposit(20.0)
    assert account.get_balance() == 140.0


def test_str_representation() -> None:
    """Test the __str__ method."""
    account = BankAccount("John", 100.0)
    result = str(account)
    assert "John" in result
    assert "100.0" in result or "100" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    account = BankAccount("John", 100.0)
    result = repr(account)
    assert "BankAccount" in result
    assert "John" in result
