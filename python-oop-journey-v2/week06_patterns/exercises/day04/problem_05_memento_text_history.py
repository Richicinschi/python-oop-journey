"""Problem 05: Memento Text History

Topic: Memento Pattern
Difficulty: Medium

Implement a text editor with undo functionality using the Memento pattern.
The editor can save and restore its state without exposing internal details.

HINTS:
- Hint 1 (Conceptual): Memento captures state without exposing internals. Only 
  the Originator (TextEditor) can create and use mementos. Caretaker (History) 
  just stores them.
- Hint 2 (Structural): TextEditor has save() -> Memento and restore(memento). 
  History manages a stack of mementos. Memento is immutable (frozen dataclass).
- Hint 3 (Edge Case): Handle undo when history is empty (return None or raise?). 
  Cursor position should be restored along with content. Don't expose memento 
  internals to Caretaker.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import override


@dataclass(frozen=True)
class EditorMemento:
    """Memento: Immutable snapshot of editor state.
    
    The frozen dataclass ensures the state cannot be modified after creation.
    The Caretaker (History) stores these but cannot modify them.
    
    Attributes:
        content: The text content at snapshot time
        cursor_position: Cursor position at snapshot time
        selection_start: Start of selection (if any)
        selection_end: End of selection (if any)
        timestamp: When the snapshot was created
    """
    content: str
    cursor_position: int
    selection_start: int
    selection_end: int
    timestamp: datetime


class TextEditor:
    """Originator: The text editor that creates and restores from mementos.
    
    Manages text content, cursor position, and selection state.
    Can save its state to a memento and restore from one.
    """
    
    def __init__(self) -> None:
        """Initialize an empty text editor."""
        raise NotImplementedError("Implement TextEditor.__init__")
    
    def insert_text(self, text: str) -> None:
        """Insert text at current cursor position.
        
        If there's a selection, it should be replaced.
        Cursor moves to end of inserted text.
        
        Args:
            text: Text to insert
        """
        raise NotImplementedError("Implement TextEditor.insert_text")
    
    def delete_selection(self) -> bool:
        """Delete the current selection.
        
        Returns:
            True if selection was deleted, False if no selection
        """
        raise NotImplementedError("Implement TextEditor.delete_selection")
    
    def select(self, start: int, end: int) -> bool:
        """Set selection range.
        
        Args:
            start: Selection start index (inclusive)
            end: Selection end index (exclusive)
            
        Returns:
            True if valid selection, False if indices out of bounds
        """
        raise NotImplementedError("Implement TextEditor.select")
    
    def clear_selection(self) -> None:
        """Clear the current selection."""
        raise NotImplementedError("Implement TextEditor.clear_selection")
    
    def move_cursor(self, position: int) -> bool:
        """Move cursor to specified position.
        
        Args:
            position: New cursor position
            
        Returns:
            True if position is valid, False otherwise
        """
        raise NotImplementedError("Implement TextEditor.move_cursor")
    
    def get_content(self) -> str:
        """Get current text content.
        
        Returns:
            Current text content
        """
        raise NotImplementedError("Implement TextEditor.get_content")
    
    def get_cursor_position(self) -> int:
        """Get current cursor position.
        
        Returns:
            Current cursor position (0 to len(content))
        """
        raise NotImplementedError("Implement TextEditor.get_cursor_position")
    
    def get_selection(self) -> tuple[int, int] | None:
        """Get current selection range.
        
        Returns:
            Tuple of (start, end) if selection exists, None otherwise
        """
        raise NotImplementedError("Implement TextEditor.get_selection")
    
    def save(self) -> EditorMemento:
        """Create a memento of current state.
        
        Returns:
            Memento containing current state snapshot
        """
        raise NotImplementedError("Implement TextEditor.save")
    
    def restore(self, memento: EditorMemento) -> None:
        """Restore state from a memento.
        
        Args:
            memento: Memento to restore from
        """
        raise NotImplementedError("Implement TextEditor.restore")


class History:
    """Caretaker: Manages editor mementos without accessing their contents.
    
    Provides undo/redo functionality by managing a stack of mementos.
    """
    
    def __init__(self, editor: TextEditor) -> None:
        """Initialize history for an editor.
        
        Args:
            editor: The text editor to manage history for
        """
        raise NotImplementedError("Implement History.__init__")
    
    def backup(self) -> None:
        """Save current editor state to history.
        
        Creates a memento and pushes it onto the undo stack.
        Clears the redo stack (new branch in history).
        """
        raise NotImplementedError("Implement History.backup")
    
    def undo(self) -> bool:
        """Undo the last change.
        
        Returns:
            True if undo was successful, False if nothing to undo
        """
        raise NotImplementedError("Implement History.undo")
    
    def redo(self) -> bool:
        """Redo the last undone change.
        
        Returns:
            True if redo was successful, False if nothing to redo
        """
        raise NotImplementedError("Implement History.redo")
    
    def can_undo(self) -> bool:
        """Check if undo is available.
        
        Returns:
            True if undo can be performed
        """
        raise NotImplementedError("Implement History.can_undo")
    
    def can_redo(self) -> bool:
        """Check if redo is available.
        
        Returns:
            True if redo can be performed
        """
        raise NotImplementedError("Implement History.can_redo")
    
    def get_undo_count(self) -> int:
        """Get number of available undo operations.
        
        Returns:
            Count of states in undo stack
        """
        raise NotImplementedError("Implement History.get_undo_count")
    
    def get_redo_count(self) -> int:
        """Get number of available redo operations.
        
        Returns:
            Count of states in redo stack
        """
        raise NotImplementedError("Implement History.get_redo_count")
    
    def clear(self) -> None:
        """Clear all history (both undo and redo stacks)."""
        raise NotImplementedError("Implement History.clear")
