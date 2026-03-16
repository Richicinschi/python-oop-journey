"""Reference solution for Problem 09: Attribute History."""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class HistoryEntry:
    """A single entry in the attribute history."""
    value: Any
    timestamp: datetime
    previous_value: Any = None


class History:
    """A descriptor that tracks all value changes."""
    
    def __init__(self, default: Any = None, max_history: int = 0) -> None:
        self.default = default
        self.max_history = max_history
        self.name = ""
        self.storage_name = ""
        self.histories: dict[int, list[HistoryEntry]] = {}
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, self.default)
    
    def __set__(self, instance: object, value: Any) -> None:
        old_value = getattr(instance, self.storage_name, self.default)
        
        entry = HistoryEntry(
            value=value,
            timestamp=datetime.now(),
            previous_value=old_value
        )
        
        instance_id = id(instance)
        if instance_id not in self.histories:
            self.histories[instance_id] = []
        
        self.histories[instance_id].append(entry)
        
        if self.max_history > 0 and len(self.histories[instance_id]) > self.max_history:
            self.histories[instance_id] = self.histories[instance_id][-self.max_history:]
        
        setattr(instance, self.storage_name, value)
    
    def get_history(self, instance: object) -> list[HistoryEntry]:
        return self.histories.get(id(instance), [])
    
    def get_previous(self, instance: object) -> Any:
        history = self.get_history(instance)
        if len(history) >= 2:
            return history[-2].value
        return None
    
    def clear_history(self, instance: object) -> None:
        instance_id = id(instance)
        if instance_id in self.histories:
            current = self.get_history(instance)[-1].value if self.get_history(instance) else self.default
            self.histories[instance_id] = [HistoryEntry(
                value=current,
                timestamp=datetime.now(),
                previous_value=None
            )]
    
    def rollback(self, instance: object, steps: int = 1) -> bool:
        history = self.get_history(instance)
        if len(history) <= steps:
            return False
        
        target_entry = history[-(steps + 1)]
        setattr(instance, self.storage_name, target_entry.value)
        self.histories[id(instance)] = history[:-steps]
        return True


class Document:
    """A document with versioned content."""
    
    title: str = ""
    content = History()
    
    def __init__(self, title: str, content: str = "") -> None:
        self.title = title
        self.content = content
    
    def edit(self, new_content: str) -> None:
        self.content = new_content
    
    def get_versions(self) -> list[HistoryEntry]:
        return type(self).content.get_history(self)
    
    def undo(self) -> bool:
        return type(self).content.rollback(self, 1)


class Setting:
    """A user setting with change history."""
    
    name: str = ""
    description: str = ""
    value = History()
    
    def __init__(self, name: str, description: str, default_value: Any = None) -> None:
        self.name = name
        self.description = description
        self.value = default_value
    
    def update(self, new_value: Any) -> None:
        self.value = new_value
    
    def get_changes(self) -> list[HistoryEntry]:
        return type(self).value.get_history(self)
    
    def has_changed(self) -> bool:
        return len(self.get_changes()) > 1
