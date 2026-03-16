"""Solution: Command Text Editor.

Implements the Command pattern for undo/redo functionality.

WHY COMMAND?
The Command pattern encapsulates requests as objects, allowing:
- Parameterization of clients with different requests
- Queuing or logging of requests
- Undoable operations

KEY BENEFIT: Each action (insert, delete) is captured as an object containing
all information needed to execute or reverse the action. This enables the
history stack and undo/redo functionality.

UNDO/REDO MECHANISM:
- Undo stack: Commands that have been executed
- Redo stack: Commands that have been undone
- New command: Clears redo stack (branching history is discarded)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """Abstract command interface."""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""
        pass


class TextEditor:
    """Receiver class representing a text editor."""
    
    def __init__(self) -> None:
        """Initialize with empty content."""
        self._content = ""
    
    def insert(self, position: int, text: str) -> None:
        """Insert text at the given position.
        
        Args:
            position: Position to insert at.
            text: Text to insert.
        """
        # Clamp position to valid range
        position = max(0, min(position, len(self._content)))
        self._content = self._content[:position] + text + self._content[position:]
    
    def delete(self, position: int, length: int) -> str:
        """Delete text from the given position.
        
        Args:
            position: Position to start deletion.
            length: Number of characters to delete.
        
        Returns:
            The deleted text.
        """
        # Clamp position and length to valid range
        position = max(0, min(position, len(self._content)))
        length = max(0, min(length, len(self._content) - position))
        
        deleted = self._content[position:position + length]
        self._content = self._content[:position] + self._content[position + length:]
        return deleted
    
    def get_content(self) -> str:
        """Get current content.
        
        Returns:
            Current text content.
        """
        return self._content


class InsertCommand(Command):
    """Command to insert text into the editor."""
    
    def __init__(self, editor: TextEditor, position: int, text: str) -> None:
        """Initialize insert command.
        
        Args:
            editor: The text editor to modify.
            position: Position to insert at.
            text: Text to insert.
        """
        self._editor = editor
        self._position = position
        self._text = text
        self._actual_position = 0  # Set during execute
    
    def execute(self) -> None:
        """Execute the insert command."""
        self._actual_position = max(0, min(self._position, len(self._editor.get_content())))
        self._editor.insert(self._actual_position, self._text)
    
    def undo(self) -> None:
        """Undo the insert by deleting the inserted text."""
        self._editor.delete(self._actual_position, len(self._text))


class DeleteCommand(Command):
    """Command to delete text from the editor."""
    
    def __init__(self, editor: TextEditor, position: int, length: int) -> None:
        """Initialize delete command.
        
        Args:
            editor: The text editor to modify.
            position: Position to start deletion.
            length: Number of characters to delete.
        """
        self._editor = editor
        self._position = position
        self._length = length
        self._deleted_text = ""
    
    def execute(self) -> None:
        """Execute the delete command."""
        self._deleted_text = self._editor.delete(self._position, self._length)
    
    def undo(self) -> None:
        """Undo the delete by re-inserting the deleted text."""
        self._editor.insert(self._position, self._deleted_text)


class CommandHistory:
    """Manages the history of commands for undo/redo."""
    
    def __init__(self) -> None:
        """Initialize empty history."""
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
    
    def push(self, command: Command) -> None:
        """Push a command onto the undo stack.
        
        Args:
            command: Command to push.
        """
        self._undo_stack.append(command)
        self._redo_stack.clear()  # Clear redo on new command
    
    def undo(self) -> Command | None:
        """Pop a command from undo stack for undoing.
        
        Returns:
            Command to undo, or None if stack empty.
        """
        if not self._undo_stack:
            return None
        command = self._undo_stack.pop()
        self._redo_stack.append(command)
        return command
    
    def redo(self) -> Command | None:
        """Pop a command from redo stack for redoing.
        
        Returns:
            Command to redo, or None if stack empty.
        """
        if not self._redo_stack:
            return None
        command = self._redo_stack.pop()
        self._undo_stack.append(command)
        return command
    
    def can_undo(self) -> bool:
        """Check if undo is available.
        
        Returns:
            True if can undo.
        """
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available.
        
        Returns:
            True if can redo.
        """
        return len(self._redo_stack) > 0


class TextEditorInvoker:
    """Invoker that manages command execution and history."""
    
    def __init__(self, editor: TextEditor) -> None:
        """Initialize with editor and history.
        
        Args:
            editor: The text editor to control.
        """
        self._editor = editor
        self._history = CommandHistory()
    
    def insert(self, position: int, text: str) -> None:
        """Execute insert command.
        
        Args:
            position: Position to insert at.
            text: Text to insert.
        """
        command = InsertCommand(self._editor, position, text)
        command.execute()
        self._history.push(command)
    
    def delete(self, position: int, length: int) -> None:
        """Execute delete command.
        
        Args:
            position: Position to start deletion.
            length: Number of characters to delete.
        """
        command = DeleteCommand(self._editor, position, length)
        command.execute()
        self._history.push(command)
    
    def undo(self) -> bool:
        """Undo last command.
        
        Returns:
            True if undo was performed.
        """
        command = self._history.undo()
        if command:
            command.undo()
            return True
        return False
    
    def redo(self) -> bool:
        """Redo last undone command.
        
        Returns:
            True if redo was performed.
        """
        command = self._history.redo()
        if command:
            command.execute()
            return True
        return False
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._history.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._history.can_redo()
    
    def get_content(self) -> str:
        """Get editor content."""
        return self._editor.get_content()
