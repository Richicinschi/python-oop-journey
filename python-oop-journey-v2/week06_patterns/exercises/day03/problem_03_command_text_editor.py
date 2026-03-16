"""Problem 03: Command Text Editor

Topic: Command Pattern
Difficulty: Medium

Implement the Command pattern for a text editor with undo/redo functionality.

HINTS:
- Hint 1 (Conceptual): Commands encapsulate both the action AND the information 
  needed to undo it. Store the state before executing so you can restore it.
- Hint 2 (Structural): Each command needs: execute(), undo(), and constructor 
  parameters (position, text). CommandHistory maintains two stacks: undo_stack 
  and redo_stack.
- Hint 3 (Edge Case): After undo(), clear the redo stack (new actions should 
  overwrite redo history). Handle empty undo/redo gracefully.

PATTERN EXPLANATION:
The Command pattern encapsulates a request as an object, thereby letting you
parameterize clients with different requests, queue or log requests, and
support undoable operations.

STRUCTURE:
- Command: Interface for executing operations (execute(), undo())
- ConcreteCommand (InsertCommand, DeleteCommand): Binds action to receiver
- Receiver (TextEditor): Knows how to perform operations
- Invoker (TextEditorInvoker): Asks command to carry out request
- Caretaker (CommandHistory): Manages command history for undo/redo

WHEN TO USE:
- For undo/redo functionality
- When you need to queue operations
- For logging changes or transactional systems
- To parameterize objects with operations

EXAMPLE USAGE:
    editor = TextEditor()
    invoker = TextEditorInvoker(editor)
    
    invoker.insert(0, "Hello ")
    invoker.insert(6, "World")
    print(invoker.get_content())  # "Hello World"
    
    invoker.undo()  # Removes "World"
    print(invoker.get_content())  # "Hello "
    
    invoker.redo()  # Restores "World"
    print(invoker.get_content())  # "Hello World"

TODO:
1. Create Command abstract base class with execute() and undo() methods
2. Create TextEditor receiver class with insert, delete, and get_content methods
3. Implement InsertCommand that inserts text at a position
4. Implement DeleteCommand that deletes text from a position
5. Create CommandHistory to manage undo/redo stack
6. Create TextEditorInvoker to execute commands and manage history
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """Abstract command interface."""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        # TODO: Implement abstract execute
        raise NotImplementedError("execute must be implemented")
    
    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""
        # TODO: Implement abstract undo
        raise NotImplementedError("undo must be implemented")


class TextEditor:
    """Receiver class representing a text editor."""
    
    def __init__(self) -> None:
        """Initialize with empty content."""
        # TODO: Initialize empty content string
        raise NotImplementedError("Initialize editor")
    
    def insert(self, position: int, text: str) -> None:
        """Insert text at the given position.
        
        Args:
            position: Position to insert at.
            text: Text to insert.
        """
        # TODO: Insert text at position
        raise NotImplementedError("Insert text")
    
    def delete(self, position: int, length: int) -> str:
        """Delete text from the given position.
        
        Args:
            position: Position to start deletion.
            length: Number of characters to delete.
        
        Returns:
            The deleted text.
        """
        # TODO: Delete and return text
        raise NotImplementedError("Delete text")
    
    def get_content(self) -> str:
        """Get current content.
        
        Returns:
            Current text content.
        """
        # TODO: Return content
        raise NotImplementedError("Return content")


class InsertCommand(Command):
    """Command to insert text into the editor."""
    
    def __init__(self, editor: TextEditor, position: int, text: str) -> None:
        """Initialize insert command.
        
        Args:
            editor: The text editor to modify.
            position: Position to insert at.
            text: Text to insert.
        """
        # TODO: Store editor, position, and text
        raise NotImplementedError("Initialize command")
    
    def execute(self) -> None:
        """Execute the insert command."""
        # TODO: Insert text at position
        raise NotImplementedError("Execute insert")
    
    def undo(self) -> None:
        """Undo the insert by deleting the inserted text."""
        # TODO: Delete the inserted text
        raise NotImplementedError("Undo insert")


class DeleteCommand(Command):
    """Command to delete text from the editor."""
    
    def __init__(self, editor: TextEditor, position: int, length: int) -> None:
        """Initialize delete command.
        
        Args:
            editor: The text editor to modify.
            position: Position to start deletion.
            length: Number of characters to delete.
        """
        # TODO: Store editor, position, length
        # TODO: Initialize deleted_text as empty
        raise NotImplementedError("Initialize command")
    
    def execute(self) -> None:
        """Execute the delete command."""
        # TODO: Delete text and store it for undo
        raise NotImplementedError("Execute delete")
    
    def undo(self) -> None:
        """Undo the delete by re-inserting the deleted text."""
        # TODO: Re-insert deleted text
        raise NotImplementedError("Undo delete")


class CommandHistory:
    """Manages the history of commands for undo/redo."""
    
    def __init__(self) -> None:
        """Initialize empty history."""
        # TODO: Initialize undo and redo stacks
        raise NotImplementedError("Initialize history")
    
    def push(self, command: Command) -> None:
        """Push a command onto the undo stack.
        
        Args:
            command: Command to push.
        """
        # TODO: Push to undo stack and clear redo stack
        raise NotImplementedError("Push command")
    
    def undo(self) -> Command | None:
        """Pop a command from undo stack for undoing.
        
        Returns:
            Command to undo, or None if stack empty.
        """
        # TODO: Pop from undo, push to redo, return command
        raise NotImplementedError("Undo")
    
    def redo(self) -> Command | None:
        """Pop a command from redo stack for redoing.
        
        Returns:
            Command to redo, or None if stack empty.
        """
        # TODO: Pop from redo, push to undo, return command
        raise NotImplementedError("Redo")
    
    def can_undo(self) -> bool:
        """Check if undo is available.
        
        Returns:
            True if can undo.
        """
        # TODO: Check if undo stack is not empty
        raise NotImplementedError("Can undo")
    
    def can_redo(self) -> bool:
        """Check if redo is available.
        
        Returns:
            True if can redo.
        """
        # TODO: Check if redo stack is not empty
        raise NotImplementedError("Can redo")


class TextEditorInvoker:
    """Invoker that manages command execution and history."""
    
    def __init__(self, editor: TextEditor) -> None:
        """Initialize with editor and history.
        
        Args:
            editor: The text editor to control.
        """
        # TODO: Store editor and create history
        raise NotImplementedError("Initialize invoker")
    
    def insert(self, position: int, text: str) -> None:
        """Execute insert command.
        
        Args:
            position: Position to insert at.
            text: Text to insert.
        """
        # TODO: Create and execute InsertCommand
        raise NotImplementedError("Insert")
    
    def delete(self, position: int, length: int) -> None:
        """Execute delete command.
        
        Args:
            position: Position to start deletion.
            length: Number of characters to delete.
        """
        # TODO: Create and execute DeleteCommand
        raise NotImplementedError("Delete")
    
    def undo(self) -> bool:
        """Undo last command.
        
        Returns:
            True if undo was performed.
        """
        # TODO: Undo last command if available
        raise NotImplementedError("Undo")
    
    def redo(self) -> bool:
        """Redo last undone command.
        
        Returns:
            True if redo was performed.
        """
        # TODO: Redo last undone command if available
        raise NotImplementedError("Redo")
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        # TODO: Delegate to history
        raise NotImplementedError("Can undo")
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        # TODO: Delegate to history
        raise NotImplementedError("Can redo")
    
    def get_content(self) -> str:
        """Get editor content."""
        # TODO: Return editor content
        raise NotImplementedError("Get content")
