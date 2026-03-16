"""Tests for Problem 05: Transaction Context Manager."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day06.problem_05_transaction_context_manager import (
    MultiResourceTransaction,
    SimpleDatabase,
    Transaction,
)


class TestSimpleDatabase:
    """Tests for the SimpleDatabase class."""
    
    def test_init(self) -> None:
        """Test database initialization."""
        db = SimpleDatabase()
        assert db.keys() == []
    
    def test_set_and_get(self) -> None:
        """Test setting and getting values."""
        db = SimpleDatabase()
        db.set("key", "value")
        
        assert db.get("key") == "value"
    
    def test_get_nonexistent_raises(self) -> None:
        """Test getting non-existent key raises KeyError."""
        db = SimpleDatabase()
        
        with pytest.raises(KeyError):
            db.get("nonexistent")
    
    def test_delete(self) -> None:
        """Test deleting a key."""
        db = SimpleDatabase()
        db.set("key", "value")
        db.delete("key")
        
        with pytest.raises(KeyError):
            db.get("key")
    
    def test_delete_nonexistent_raises(self) -> None:
        """Test deleting non-existent key raises KeyError."""
        db = SimpleDatabase()
        
        with pytest.raises(KeyError):
            db.delete("nonexistent")
    
    def test_keys(self) -> None:
        """Test getting all keys."""
        db = SimpleDatabase()
        db.set("a", 1)
        db.set("b", 2)
        
        assert sorted(db.keys()) == ["a", "b"]
    
    def test_snapshot(self) -> None:
        """Test snapshot creates a copy."""
        db = SimpleDatabase()
        db.set("key", [1, 2, 3])
        
        snap = db.snapshot()
        db.set("key", [4, 5, 6])
        
        assert snap["key"] == [1, 2, 3]
    
    def test_contains(self) -> None:
        """Test __contains__ method."""
        db = SimpleDatabase()
        db.set("key", "value")
        
        assert "key" in db
        assert "nonexistent" not in db


class TestTransaction:
    """Tests for the Transaction class."""
    
    def test_transaction_commits_on_success(self) -> None:
        """Test that successful transaction commits changes."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        with Transaction(db) as tx:
            tx.set("a", 100)
        
        assert db.get("a") == 100
        assert tx.committed is True
    
    def test_transaction_rolls_back_on_exception(self) -> None:
        """Test that failed transaction rolls back changes."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        try:
            with Transaction(db) as tx:
                tx.set("a", 100)
                raise ValueError("Test error")
        except ValueError:
            pass
        
        assert db.get("a") == 1  # Rolled back
        assert tx.committed is False
    
    def test_transaction_get_from_buffer(self) -> None:
        """Test that get returns buffered value."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        with Transaction(db) as tx:
            tx.set("a", 100)
            assert tx.get("a") == 100
    
    def test_transaction_get_from_database(self) -> None:
        """Test that get falls back to database for unmodified keys."""
        db = SimpleDatabase()
        db.set("a", 1)
        db.set("b", 2)
        
        with Transaction(db) as tx:
            tx.set("a", 100)
            assert tx.get("b") == 2  # Unchanged, from database
    
    def test_transaction_delete(self) -> None:
        """Test deletion within transaction."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        with Transaction(db) as tx:
            tx.delete("a")
        
        assert "a" not in db
    
    def test_transaction_delete_rollback(self) -> None:
        """Test deletion is rolled back on failure."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        try:
            with Transaction(db) as tx:
                tx.delete("a")
                raise ValueError("Test error")
        except ValueError:
            pass
        
        assert db.get("a") == 1  # Not deleted
    
    def test_transaction_add_new_key(self) -> None:
        """Test adding a new key in transaction."""
        db = SimpleDatabase()
        
        with Transaction(db) as tx:
            tx.set("new_key", "new_value")
        
        assert db.get("new_key") == "new_value"
    
    def test_transaction_add_rollback(self) -> None:
        """Test new key addition is rolled back."""
        db = SimpleDatabase()
        
        try:
            with Transaction(db) as tx:
                tx.set("new_key", "new_value")
                raise ValueError("Test error")
        except ValueError:
            pass
        
        assert "new_key" not in db
    
    def test_transaction_multiple_operations(self) -> None:
        """Test multiple operations in single transaction."""
        db = SimpleDatabase()
        db.set("a", 1)
        db.set("b", 2)
        
        with Transaction(db) as tx:
            tx.set("a", 10)
            tx.set("b", 20)
            tx.set("c", 30)
        
        assert db.get("a") == 10
        assert db.get("b") == 20
        assert db.get("c") == 30
    
    def test_transaction_delete_then_set(self) -> None:
        """Test deleting then setting same key."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        with Transaction(db) as tx:
            tx.delete("a")
            tx.set("a", 100)
        
        assert db.get("a") == 100
    
    def test_transaction_get_deleted_raises(self) -> None:
        """Test that getting a pending-deleted key raises KeyError."""
        db = SimpleDatabase()
        db.set("a", 1)
        
        with Transaction(db) as tx:
            tx.delete("a")
            with pytest.raises(KeyError):
                tx.get("a")


class TestMultiResourceTransaction:
    """Tests for the MultiResourceTransaction class."""
    
    def test_multi_commit_success(self) -> None:
        """Test committing across multiple databases."""
        db1 = SimpleDatabase()
        db2 = SimpleDatabase()
        
        with MultiResourceTransaction(db1, db2) as tx:
            tx.on(db1).set("key1", "value1")
            tx.on(db2).set("key2", "value2")
        
        assert db1.get("key1") == "value1"
        assert db2.get("key2") == "value2"
        assert tx.committed is True
    
    def test_multi_rollback_all_on_failure(self) -> None:
        """Test that all databases roll back on failure."""
        db1 = SimpleDatabase()
        db2 = SimpleDatabase()
        db1.set("a", 1)
        db2.set("b", 2)
        
        try:
            with MultiResourceTransaction(db1, db2) as tx:
                tx.on(db1).set("a", 100)
                tx.on(db2).set("b", 200)
                raise ValueError("Test error")
        except ValueError:
            pass
        
        assert db1.get("a") == 1  # Rolled back
        assert db2.get("b") == 2  # Rolled back
    
    def test_multi_invalid_database_raises(self) -> None:
        """Test that accessing non-participating database raises error."""
        db1 = SimpleDatabase()
        db2 = SimpleDatabase()
        db3 = SimpleDatabase()
        
        with pytest.raises(ValueError) as exc_info:
            with MultiResourceTransaction(db1, db2) as tx:
                tx.on(db3).set("key", "value")
        
        assert "not part of this transaction" in str(exc_info.value)
    
    def test_multi_read_after_write(self) -> None:
        """Test reading a value after writing in transaction."""
        db = SimpleDatabase()
        
        with MultiResourceTransaction(db) as tx:
            tx.on(db).set("key", "value")
            assert tx.on(db).get("key") == "value"
    
    def test_multi_get_unmodified(self) -> None:
        """Test getting unmodified values from database."""
        db = SimpleDatabase()
        db.set("existing", "value")
        
        with MultiResourceTransaction(db) as tx:
            assert tx.on(db).get("existing") == "value"
