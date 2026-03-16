"""Tests for Problem 03: Attribute Diff Tool."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day06.problem_03_attribute_diff_tool import (
    AttributeWatcher,
    DiffResult,
    TrackedObject,
)


class TestDiffResult:
    """Tests for the DiffResult dataclass."""
    
    def test_has_changes_true(self) -> None:
        """Test has_changes returns True when changes exist."""
        diff = DiffResult(
            added={'new': 1},
            removed={},
            modified={},
            unchanged={}
        )
        assert diff.has_changes() is True
    
    def test_has_changes_false(self) -> None:
        """Test has_changes returns False when no changes exist."""
        diff = DiffResult({}, {}, {}, {})
        assert diff.has_changes() is False
    
    def test_str_representation(self) -> None:
        """Test string representation includes all changes."""
        diff = DiffResult(
            added={'a': 1},
            removed={'b': 2},
            modified={'c': (1, 2)},
            unchanged={'d': 3}
        )
        result = str(diff)
        
        assert "Added" in result
        assert "Removed" in result
        assert "Modified" in result
        assert "Unchanged" in result


class TestTrackedObject:
    """Tests for the TrackedObject class."""
    
    def test_init(self) -> None:
        """Test initialization."""
        obj = TrackedObject()
        changes = obj.get_changes()
        
        assert changes.added == {}
        assert changes.removed == {}
        assert changes.modified == {}
        assert changes.unchanged == {}
    
    def test_setattr_tracks_additions(self) -> None:
        """Test that setting attributes tracks additions."""
        obj = TrackedObject()
        obj.name = "Alice"
        
        history = obj.get_history()
        
        assert len(history) == 1
        assert history[0]['action'] == 'added'
        assert history[0]['name'] == 'name'
        assert history[0]['new'] == 'Alice'
    
    def test_setattr_tracks_modifications(self) -> None:
        """Test that modifying attributes is tracked."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        obj.name = "Bob"
        
        changes = obj.get_changes()
        
        assert 'name' in changes.modified
        assert changes.modified['name'] == ('Alice', 'Bob')
    
    def test_delattr_tracks_removals(self) -> None:
        """Test that deleting attributes is tracked."""
        obj = TrackedObject()
        obj.name = "Alice"
        del obj.name
        
        history = obj.get_history()
        
        assert len(history) == 2
        assert history[1]['action'] == 'removed'
        assert history[1]['name'] == 'name'
        assert history[1]['old'] == 'Alice'
    
    def test_delattr_nonexistent_raises(self) -> None:
        """Test deleting non-existent attribute raises error."""
        obj = TrackedObject()
        
        with pytest.raises(AttributeError):
            del obj.nonexistent
    
    def test_checkpoint_clears_changes(self) -> None:
        """Test that checkpoint resets the change baseline."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        
        changes = obj.get_changes()
        
        assert not changes.has_changes()
        assert 'name' in changes.unchanged
    
    def test_get_changes_detects_added(self) -> None:
        """Test get_changes detects added attributes."""
        obj = TrackedObject()
        obj.checkpoint()
        obj.name = "Alice"
        obj.age = 30
        
        changes = obj.get_changes()
        
        assert 'name' in changes.added
        assert 'age' in changes.added
        assert changes.added['name'] == 'Alice'
        assert changes.added['age'] == 30
    
    def test_get_changes_detects_removed(self) -> None:
        """Test get_changes detects removed attributes."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        del obj.name
        
        changes = obj.get_changes()
        
        assert 'name' in changes.removed
        assert changes.removed['name'] == 'Alice'
    
    def test_get_changes_detects_modified(self) -> None:
        """Test get_changes detects modified attributes."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        obj.name = "Bob"
        
        changes = obj.get_changes()
        
        assert 'name' in changes.modified
        assert changes.modified['name'] == ('Alice', 'Bob')
    
    def test_rollback_restores_checkpoint(self) -> None:
        """Test rollback restores checkpoint state."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        obj.name = "Bob"
        obj.age = 30
        
        obj.rollback()
        
        assert obj.name == "Alice"
        assert not hasattr(obj, 'age')
    
    def test_rollback_clears_history(self) -> None:
        """Test rollback clears the history."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        obj.name = "Bob"
        
        obj.rollback()
        
        assert obj.get_history() == []
    
    def test_clear_history(self) -> None:
        """Test clear_history resets everything."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.checkpoint()
        obj.name = "Bob"
        
        obj.clear_history()
        
        assert obj.get_history() == []
        changes = obj.get_changes()
        assert not changes.has_changes()
    
    def test_private_attrs_not_tracked(self) -> None:
        """Test that private attributes (starting with _) are not tracked."""
        obj = TrackedObject()
        obj._private = "secret"
        
        history = obj.get_history()
        
        # Should not have tracking entry for private attr
        assert not any(h['name'] == '_private' for h in history)
    
    def test_multiple_modifications(self) -> None:
        """Test tracking multiple modifications to same attribute."""
        obj = TrackedObject()
        obj.name = "Alice"
        obj.name = "Bob"
        obj.name = "Charlie"
        
        history = obj.get_history()
        
        # Should have 3 entries (one add, two modifications)
        assert len(history) == 3
        assert history[0]['action'] == 'added'
        assert history[1]['action'] == 'modified'
        assert history[2]['action'] == 'modified'


class TestAttributeWatcher:
    """Tests for the AttributeWatcher class."""
    
    def test_init(self) -> None:
        """Test watcher initialization."""
        target = type('Target', (), {'name': 'Alice'})()
        watcher = AttributeWatcher(target)
        
        assert watcher._target is target
    
    def test_snapshot_captures_state(self) -> None:
        """Test snapshot captures current state."""
        class Target:
            def __init__(self) -> None:
                self.name = 'Alice'
        
        target = Target()
        watcher = AttributeWatcher(target)
        
        watcher.snapshot()
        target.name = "Bob"
        
        changes = watcher.get_changes()
        
        assert 'name' in changes.modified
        assert changes.modified['name'] == ('Alice', 'Bob')
    
    def test_get_changes_no_changes(self) -> None:
        """Test get_changes when nothing changed."""
        target = type('Target', (), {'name': 'Alice'})()
        watcher = AttributeWatcher(target)
        
        watcher.snapshot()
        
        changes = watcher.get_changes()
        
        assert not changes.has_changes()
    
    def test_get_changes_detects_added(self) -> None:
        """Test watcher detects added attributes."""
        target = type('Target', (), {})()
        watcher = AttributeWatcher(target)
        
        watcher.snapshot()
        target.name = "Alice"
        
        changes = watcher.get_changes()
        
        assert 'name' in changes.added
    
    def test_get_changes_detects_removed(self) -> None:
        """Test watcher detects removed attributes."""
        class Target:
            def __init__(self) -> None:
                self.name = 'Alice'
        
        target = Target()
        watcher = AttributeWatcher(target)
        
        watcher.snapshot()
        del target.name
        
        changes = watcher.get_changes()
        
        assert 'name' in changes.removed
