"""Reference solution for Problem 05: Memento Text History."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import override


@dataclass(frozen=True)
class EditorMemento:
    """Memento: Immutable snapshot of editor state."""
    content: str
    cursor_position: int
    selection_start: int
    selection_end: int
    timestamp: datetime


class TextEditor:
    """Originator: The text editor that creates and restores from mementos."""
    
    def __init__(self) -> None:
        self._content = ""
        self._cursor_position = 0
        self._selection_start = 0
        self._selection_end = 0
    
    def insert_text(self, text: str) -> None:
        """Insert text at current cursor position."""
        if self._selection_start != self._selection_end:
            # Replace selection
            self._content = (
                self._content[:self._selection_start] +
                text +
                self._content[self._selection_end:]
            )
            self._cursor_position = self._selection_start + len(text)
            self._selection_start = self._selection_end = self._cursor_position
        else:
            # Insert at cursor
            self._content = (
                self._content[:self._cursor_position] +
                text +
                self._content[self._cursor_position:]
            )
            self._cursor_position += len(text)
    
    def delete_selection(self) -> bool:
        """Delete the current selection."""
        if self._selection_start == self._selection_end:
            return False
        self._content = (
            self._content[:self._selection_start] +
            self._content[self._selection_end:]
        )
        self._cursor_position = self._selection_start
        self._selection_end = self._selection_start
        return True
    
    def select(self, start: int, end: int) -> bool:
        """Set selection range."""
        if start < 0 or end > len(self._content) or start > end:
            return False
        self._selection_start = start
        self._selection_end = end
        self._cursor_position = end
        return True
    
    def clear_selection(self) -> None:
        """Clear the current selection."""
        self._cursor_position = self._selection_end
        self._selection_start = self._selection_end = self._cursor_position
    
    def move_cursor(self, position: int) -> bool:
        """Move cursor to specified position."""
        if position < 0 or position > len(self._content):
            return False
        self._cursor_position = position
        self._selection_start = self._selection_end = position
        return True
    
    def get_content(self) -> str:
        """Get current text content."""
        return self._content
    
    def get_cursor_position(self) -> int:
        """Get current cursor position."""
        return self._cursor_position
    
    def get_selection(self) -> tuple[int, int] | None:
        """Get current selection range."""
        if self._selection_start == self._selection_end:
            return None
        return (self._selection_start, self._selection_end)
    
    def save(self) -> EditorMemento:
        """Create a memento of current state."""
        return EditorMemento(
            content=self._content,
            cursor_position=self._cursor_position,
            selection_start=self._selection_start,
            selection_end=self._selection_end,
            timestamp=datetime.now()
        )
    
    def restore(self, memento: EditorMemento) -> None:
        """Restore state from a memento."""
        self._content = memento.content
        self._cursor_position = memento.cursor_position
        self._selection_start = memento.selection_start
        self._selection_end = memento.selection_end


class History:
    """Caretaker: Manages editor mementos without accessing their contents."""
    
    def __init__(self, editor: TextEditor) -> None:
        self._editor = editor
        self._undo_stack: list[EditorMemento] = []
        self._redo_stack: list[EditorMemento] = []
    
    def backup(self) -> None:
        """Save current editor state to history."""
        self._undo_stack.append(self._editor.save())
        self._redo_stack.clear()  # Clear redo on new change
    
    def undo(self) -> bool:
        """Undo the last change."""
        if not self._undo_stack:
            return False
        # Save current state to redo stack first
        current = self._editor.save()
        self._redo_stack.append(current)
        # Get the state to restore and remove it from undo stack
        memento = self._undo_stack.pop()
        # Restore that state
        self._editor.restore(memento)
        return True
    
    def redo(self) -> bool:
        """Redo the last undone change."""
        if not self._redo_stack:
            return False
        # Restore the state from redo stack
        memento = self._redo_stack.pop()
        self._editor.restore(memento)
        # Add it back to undo stack
        self._undo_stack.append(memento)
        return True
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def get_undo_count(self) -> int:
        """Get number of available undo operations."""
        return len(self._undo_stack)
    
    def get_redo_count(self) -> int:
        """Get number of available redo operations."""
        return len(self._redo_stack)
    
    def clear(self) -> None:
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
