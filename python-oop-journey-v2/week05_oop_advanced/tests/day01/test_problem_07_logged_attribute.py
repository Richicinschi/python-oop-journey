"""Tests for Problem 07: Logged Attribute."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_07_logged_attribute import (
    LoggedAttribute, LogEntry, Operation, User, BankAccount
)


class TestLoggedAttribute:
    """Tests for the LoggedAttribute descriptor."""
    
    def setup_method(self) -> None:
        LoggedAttribute.clear_logs()
    
    def test_get_operation_logged(self) -> None:
        class TestClass:
            value = LoggedAttribute(default="test")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        _ = obj.value
        
        logs = LoggedAttribute.get_logs_for_instance(obj)
        get_logs = [log for log in logs if log.operation == Operation.GET]
        assert len(get_logs) == 1
    
    def test_set_operation_logged(self) -> None:
        class TestClass:
            value = LoggedAttribute()
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "new_value"
        
        logs = LoggedAttribute.get_logs_for_instance(obj)
        set_logs = [log for log in logs if log.operation == Operation.SET]
        assert len(set_logs) == 1
        assert set_logs[0].new_value == "new_value"
    
    def test_delete_operation_logged(self) -> None:
        class TestClass:
            value = LoggedAttribute()
            
            def __init__(self) -> None:
                self.value = "test"
        
        obj = TestClass()
        del obj.value
        
        logs = LoggedAttribute.get_logs_for_instance(obj)
        del_logs = [log for log in logs if log.operation == Operation.DELETE]
        assert len(del_logs) == 1
    
    def test_log_contains_instance_id(self) -> None:
        class TestClass:
            value = LoggedAttribute(default="test")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        _ = obj.value
        
        logs = LoggedAttribute.get_logs_for_instance(obj)
        assert len(logs) > 0
        assert logs[0].instance_id == id(obj)
    
    def test_clear_logs(self) -> None:
        class TestClass:
            value = LoggedAttribute(default="test")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        _ = obj.value
        
        assert len(LoggedAttribute.logs) > 0
        LoggedAttribute.clear_logs()
        assert len(LoggedAttribute.logs) == 0


class TestUser:
    """Tests for the User class."""
    
    def setup_method(self) -> None:
        LoggedAttribute.clear_logs()
    
    def test_user_creation_logs(self) -> None:
        user = User("alice", "alice@example.com")
        
        logs = user.get_activity_log()
        set_logs = [log for log in logs if log.operation == Operation.SET]
        assert len(set_logs) >= 2  # username and email
    
    def test_attribute_access_logged(self) -> None:
        user = User("alice", "alice@example.com")
        LoggedAttribute.clear_logs()
        
        _ = user.username
        logs = user.get_activity_log()
        
        get_logs = [log for log in logs if log.operation == Operation.GET]
        assert len(get_logs) == 1
        assert get_logs[0].attribute_name == "username"
    
    def test_deactivate_logged(self) -> None:
        user = User("alice", "alice@example.com")
        LoggedAttribute.clear_logs()
        
        user.deactivate()
        logs = user.get_activity_log()
        
        set_logs = [log for log in logs if log.attribute_name == "active"]
        assert len(set_logs) == 1
        assert set_logs[0].new_value is False


class TestBankAccount:
    """Tests for the BankAccount class."""
    
    def setup_method(self) -> None:
        LoggedAttribute.clear_logs()
    
    def test_account_creation(self) -> None:
        account = BankAccount("savings", 1000.0)
        assert account.account_type == "savings"
        assert account.balance == 1000.0
    
    def test_deposit_logs_transaction(self) -> None:
        account = BankAccount("checking", 100.0)
        LoggedAttribute.clear_logs()
        
        account.deposit(50.0)
        history = account.get_transaction_history()
        
        assert len(history) == 1
        assert history[0].old_value == 100.0
        assert history[0].new_value == 150.0
    
    def test_withdraw_logs_transaction(self) -> None:
        account = BankAccount("checking", 100.0)
        LoggedAttribute.clear_logs()
        
        account.withdraw(30.0)
        history = account.get_transaction_history()
        
        assert len(history) == 1
        assert history[0].old_value == 100.0
        assert history[0].new_value == 70.0
    
    def test_transaction_history_only_includes_balance(self) -> None:
        account = BankAccount("checking", 100.0)
        # This will log account_type and balance
        LoggedAttribute.clear_logs()
        
        account.deposit(50.0)
        history = account.get_transaction_history()
        
        # Should only have balance changes
        assert all(log.attribute_name == "balance" for log in history)
    
    def test_deposit_negative_amount_raises(self) -> None:
        account = BankAccount("checking", 100.0)
        with pytest.raises(ValueError, match="negative"):
            account.deposit(-10.0)
    
    def test_withdraw_more_than_balance_raises(self) -> None:
        account = BankAccount("checking", 100.0)
        with pytest.raises(ValueError, match="Insufficient"):
            account.withdraw(150.0)
