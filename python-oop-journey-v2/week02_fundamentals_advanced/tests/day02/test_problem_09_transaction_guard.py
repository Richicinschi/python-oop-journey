"""Tests for Problem 09: Transaction Guard."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_09_transaction_guard import (
    TransactionGuard,
)


def test_transaction_guard_success() -> None:
    """Test successful transaction commits."""
    tx = TransactionGuard()
    
    with tx:
        tx.execute("INSERT")
        tx.execute("UPDATE")
    
    assert tx.committed is True
    assert tx.rolled_back is False
    assert tx.operations == ["INSERT", "UPDATE"]


def test_transaction_guard_exception_rolls_back() -> None:
    """Test transaction rolls back on exception."""
    tx = TransactionGuard()
    
    with pytest.raises(ValueError):
        with tx:
            tx.execute("INSERT")
            raise ValueError("Something went wrong")
    
    assert tx.committed is False
    assert tx.rolled_back is True
    assert tx.operations == ["INSERT"]


def test_transaction_guard_exception_propagates() -> None:
    """Test that exceptions are not suppressed."""
    tx = TransactionGuard()
    
    with pytest.raises(RuntimeError) as exc_info:
        with tx:
            raise RuntimeError("Test error")
    
    assert "Test error" in str(exc_info.value)
    assert tx.rolled_back is True


def test_transaction_guard_empty_transaction() -> None:
    """Test transaction with no operations."""
    tx = TransactionGuard()
    
    with tx:
        pass
    
    assert tx.committed is True
    assert tx.operations == []


def test_transaction_guard_multiple_executions() -> None:
    """Test multiple execute calls."""
    tx = TransactionGuard()
    
    with tx:
        tx.execute("OP1")
        tx.execute("OP2")
        tx.execute("OP3")
    
    assert tx.operations == ["OP1", "OP2", "OP3"]


def test_transaction_guard_reuse_not_recommended() -> None:
    """Test that reusing a transaction guard keeps state."""
    tx = TransactionGuard()
    
    with tx:
        tx.execute("FIRST")
    
    # Note: Reusing the same instance is not recommended but should work
    try:
        with tx:
            tx.execute("SECOND")
            raise ValueError("Fail")
    except ValueError:
        pass
    
    # State reflects the last usage
    assert tx.rolled_back is True


def test_transaction_guard_as_context_manager() -> None:
    """Test proper context manager protocol."""
    tx = TransactionGuard()
    
    # __enter__ should return self
    entered = tx.__enter__()
    assert entered is tx
    
    # __exit__ should return False (don't suppress)
    result = tx.__exit__(None, None, None)
    assert result is False
    assert tx.committed is True
