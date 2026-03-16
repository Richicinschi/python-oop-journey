"""Reference solution for Problem 03: Attribute Diff Tool."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


@dataclass
class DiffResult:
    """Result of comparing two states.
    
    Attributes:
        added: Attributes that exist now but didn't before.
        removed: Attributes that existed before but don't now.
        modified: Attributes with changed values (name -> (old, new)).
        unchanged: Attributes that stayed the same.
    """
    added: dict[str, Any]
    removed: dict[str, Any]
    modified: dict[str, tuple[Any, Any]]
    unchanged: dict[str, Any]
    
    def has_changes(self) -> bool:
        """Check if any changes were detected."""
        return bool(self.added or self.removed or self.modified)
    
    def __str__(self) -> str:
        """String representation of the diff."""
        lines = ["DiffResult:"]
        if self.added:
            lines.append(f"  Added: {list(self.added.keys())}")
        if self.removed:
            lines.append(f"  Removed: {list(self.removed.keys())}")
        if self.modified:
            lines.append(f"  Modified: {list(self.modified.keys())}")
        if self.unchanged:
            lines.append(f"  Unchanged: {len(self.unchanged)} attributes")
        if not self.has_changes():
            lines.append("  No changes")
        return "\n".join(lines)


class TrackedObject:
    """An object that tracks attribute changes.
    
    This class intercepts attribute modifications and maintains
    a history of changes for debugging and auditing.
    """
    
    def __init__(self) -> None:
        """Initialize the tracked object."""
        # Use object.__setattr__ to avoid triggering our override
        object.__setattr__(self, '_checkpoint', {})
        object.__setattr__(self, '_history', [])
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Track attribute assignments.
        
        Args:
            name: The attribute name.
            value: The new value.
        """
        # Skip tracking for private attributes
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        
        # Get the old value if it exists
        old_value = None
        has_old = False
        try:
            old_value = object.__getattribute__(self, name)
            has_old = True
        except AttributeError:
            pass
        
        # Set the new value
        object.__setattr__(self, name, value)
        
        # Record the change
        history = object.__getattribute__(self, '_history')
        if has_old:
            history.append({
                'action': 'modified',
                'name': name,
                'old': old_value,
                'new': value,
            })
        else:
            history.append({
                'action': 'added',
                'name': name,
                'old': None,
                'new': value,
            })
    
    def __delattr__(self, name: str) -> None:
        """Track attribute deletions.
        
        Args:
            name: The attribute name.
        
        Raises:
            AttributeError: If the attribute doesn't exist.
        """
        # Skip tracking for private attributes
        if name.startswith('_'):
            object.__delattr__(self, name)
            return
        
        # Get the old value before deleting
        try:
            old_value = object.__getattribute__(self, name)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
        
        # Delete the attribute
        object.__delattr__(self, name)
        
        # Record the change
        history = object.__getattribute__(self, '_history')
        history.append({
            'action': 'removed',
            'name': name,
            'old': old_value,
            'new': None,
        })
    
    def _get_public_attrs(self) -> dict[str, Any]:
        """Get all public attributes as a dictionary."""
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }
    
    def checkpoint(self) -> None:
        """Save the current state as the baseline for future comparisons."""
        # Use deepcopy to capture values, not references
        object.__setattr__(
            self,
            '_checkpoint',
            deepcopy(self._get_public_attrs())
        )
    
    def get_changes(self) -> DiffResult:
        """Get changes since the last checkpoint.
        
        Returns:
            DiffResult showing added, removed, modified, and unchanged attrs.
        """
        checkpoint = object.__getattribute__(self, '_checkpoint')
        current = self._get_public_attrs()
        
        added = {}
        removed = {}
        modified = {}
        unchanged = {}
        
        # Find added and check for modifications
        for name, value in current.items():
            if name not in checkpoint:
                added[name] = value
            elif checkpoint[name] != value:
                modified[name] = (checkpoint[name], value)
            else:
                unchanged[name] = value
        
        # Find removed
        for name, value in checkpoint.items():
            if name not in current:
                removed[name] = value
        
        return DiffResult(added, removed, modified, unchanged)
    
    def get_history(self) -> list[dict[str, Any]]:
        """Get the full change history.
        
        Returns:
            List of change records.
        """
        return deepcopy(object.__getattribute__(self, '_history'))
    
    def rollback(self) -> None:
        """Revert all changes since the last checkpoint."""
        checkpoint = object.__getattribute__(self, '_checkpoint')
        current = self._get_public_attrs()
        
        # Remove attributes not in checkpoint
        for name in list(current.keys()):
            if name not in checkpoint:
                object.__delattr__(self, name)
        
        # Restore checkpoint values
        for name, value in checkpoint.items():
            object.__setattr__(self, name, deepcopy(value))
        
        # Clear history
        object.__setattr__(self, '_history', [])
    
    def clear_history(self) -> None:
        """Clear the change history and reset checkpoint."""
        # Take a new checkpoint of current state
        object.__setattr__(
            self,
            '_checkpoint',
            deepcopy(self._get_public_attrs())
        )
        object.__setattr__(self, '_history', [])


class AttributeWatcher:
    """Watch attribute changes on an external object.
    
    Unlike TrackedObject, this wraps an existing object and
    monitors changes without modifying the target class.
    """
    
    def __init__(self, target: object) -> None:
        """Initialize the watcher for a target object.
        
        Args:
            target: The object to watch.
        """
        self._target = target
        self._snapshot: dict[str, Any] = {}
    
    def _get_attrs(self, obj: object) -> dict[str, Any]:
        """Extract public attributes from an object."""
        attrs: dict[str, Any] = {}
        for k in dir(obj):
            # Skip private and dunder
            if k.startswith('_'):
                continue
            try:
                v = getattr(obj, k)
                # Skip methods/callables - only track data
                if not callable(v):
                    attrs[k] = v
            except Exception:
                pass
        return attrs
    
    def snapshot(self) -> None:
        """Take a snapshot of the current state."""
        self._snapshot = deepcopy(self._get_attrs(self._target))
    
    def get_changes(self) -> DiffResult:
        """Compare current state to the last snapshot.
        
        Returns:
            DiffResult showing differences.
        """
        current = self._get_attrs(self._target)
        snapshot = self._snapshot
        
        added = {}
        removed = {}
        modified = {}
        unchanged = {}
        
        # Find added and check for modifications
        for name, value in current.items():
            if name not in snapshot:
                added[name] = value
            elif snapshot[name] != value:
                modified[name] = (snapshot[name], value)
            else:
                unchanged[name] = value
        
        # Find removed
        for name, value in snapshot.items():
            if name not in current:
                removed[name] = value
        
        return DiffResult(added, removed, modified, unchanged)
