"""Tests for Problem 03: Command Text Editor."""

from __future__ import annotations

import pytest
from abc import ABC

from week06_patterns.solutions.day03.problem_03_command_text_editor import (
    Command,
    TextEditor,
    InsertCommand,
    DeleteCommand,
    CommandHistory,
    TextEditorInvoker,
)


class TestCommand:
    """Test Command abstract base class."""
    
    def test_command_is_abstract(self) -> None:
        """Test that Command cannot be instantiated."""
        assert issubclass(Command, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Command()
    
    def test_command_has_required_methods(self) -> None:
        """Test that Command defines required methods."""
        assert hasattr(Command, 'execute')
        assert hasattr(Command, 'undo')


class TestTextEditor:
    """Test TextEditor receiver class."""
    
    def test_initialization(self) -> None:
        """Test editor initializes with empty content."""
        editor = TextEditor()
        assert editor.get_content() == ""
    
    def test_insert_at_beginning(self) -> None:
        """Test inserting at position 0."""
        editor = TextEditor()
        editor.insert(0, "Hello")
        assert editor.get_content() == "Hello"
    
    def test_insert_at_end(self) -> None:
        """Test inserting at end of content."""
        editor = TextEditor()
        editor.insert(0, "Hello")
        editor.insert(5, " World")
        assert editor.get_content() == "Hello World"
    
    def test_insert_in_middle(self) -> None:
        """Test inserting in the middle."""
        editor = TextEditor()
        editor.insert(0, "Hello World")
        editor.insert(5, " Beautiful")
        assert editor.get_content() == "Hello Beautiful World"
    
    def test_insert_beyond_end_clamps(self) -> None:
        """Test inserting beyond end clamps to end."""
        editor = TextEditor()
        editor.insert(0, "Hi")
        editor.insert(100, " There")  # Beyond end
        assert editor.get_content() == "Hi There"
    
    def test_insert_negative_position_clamps(self) -> None:
        """Test inserting at negative position clamps to 0."""
        editor = TextEditor()
        editor.insert(-10, "Hello")
        assert editor.get_content() == "Hello"
    
    def test_delete_from_beginning(self) -> None:
        """Test deleting from beginning."""
        editor = TextEditor()
        editor.insert(0, "Hello World")
        deleted = editor.delete(0, 5)
        assert deleted == "Hello"
        assert editor.get_content() == " World"
    
    def test_delete_from_middle(self) -> None:
        """Test deleting from middle."""
        editor = TextEditor()
        editor.insert(0, "Hello Beautiful World")
        deleted = editor.delete(6, 10)  # Delete "Beautiful "
        assert deleted == "Beautiful "
        assert editor.get_content() == "Hello World"
    
    def test_delete_returns_deleted_text(self) -> None:
        """Test delete returns the deleted text."""
        editor = TextEditor()
        editor.insert(0, "Hello")
        deleted = editor.delete(1, 3)
        assert deleted == "ell"
    
    def test_delete_beyond_content_clamps(self) -> None:
        """Test deleting beyond content clamps."""
        editor = TextEditor()
        editor.insert(0, "Hi")
        deleted = editor.delete(0, 100)
        assert deleted == "Hi"
        assert editor.get_content() == ""


class TestInsertCommand:
    """Test InsertCommand."""
    
    def test_execute_inserts_text(self) -> None:
        """Test execute inserts text."""
        editor = TextEditor()
        command = InsertCommand(editor, 0, "Hello")
        command.execute()
        assert editor.get_content() == "Hello"
    
    def test_undo_removes_inserted_text(self) -> None:
        """Test undo removes inserted text."""
        editor = TextEditor()
        command = InsertCommand(editor, 0, "Hello")
        command.execute()
        command.undo()
        assert editor.get_content() == ""
    
    def test_undo_restores_previous_state(self) -> None:
        """Test undo restores state before insert."""
        editor = TextEditor()
        editor.insert(0, "World")
        command = InsertCommand(editor, 0, "Hello ")
        command.execute()
        assert editor.get_content() == "Hello World"
        command.undo()
        assert editor.get_content() == "World"


class TestDeleteCommand:
    """Test DeleteCommand."""
    
    def test_execute_deletes_text(self) -> None:
        """Test execute deletes text."""
        editor = TextEditor()
        editor.insert(0, "Hello World")
        command = DeleteCommand(editor, 0, 5)
        command.execute()
        assert editor.get_content() == " World"
    
    def test_undo_restores_deleted_text(self) -> None:
        """Test undo restores deleted text."""
        editor = TextEditor()
        editor.insert(0, "Hello World")
        command = DeleteCommand(editor, 0, 5)
        command.execute()
        command.undo()
        assert editor.get_content() == "Hello World"
    
    def test_undo_restores_at_correct_position(self) -> None:
        """Test undo restores text at correct position."""
        editor = TextEditor()
        editor.insert(0, "Hello Beautiful World")
        command = DeleteCommand(editor, 6, 9)  # Delete "Beautiful"
        command.execute()
        assert editor.get_content() == "Hello  World"
        command.undo()
        assert editor.get_content() == "Hello Beautiful World"


class TestCommandHistory:
    """Test CommandHistory."""
    
    def test_initialization(self) -> None:
        """Test history initializes empty."""
        history = CommandHistory()
        assert not history.can_undo()
        assert not history.can_redo()
    
    def test_push_adds_to_undo_stack(self) -> None:
        """Test push adds command to undo stack."""
        history = CommandHistory()
        editor = TextEditor()
        command = InsertCommand(editor, 0, "Hello")
        
        history.push(command)
        assert history.can_undo()
        assert not history.can_redo()
    
    def test_undo_moves_to_redo(self) -> None:
        """Test undo moves command to redo stack."""
        history = CommandHistory()
        editor = TextEditor()
        command = InsertCommand(editor, 0, "Hello")
        
        history.push(command)
        result = history.undo()
        
        assert result == command
        assert not history.can_undo()
        assert history.can_redo()
    
    def test_undo_empty_returns_none(self) -> None:
        """Test undo on empty stack returns None."""
        history = CommandHistory()
        assert history.undo() is None
    
    def test_redo_moves_to_undo(self) -> None:
        """Test redo moves command back to undo stack."""
        history = CommandHistory()
        editor = TextEditor()
        command = InsertCommand(editor, 0, "Hello")
        
        history.push(command)
        history.undo()
        result = history.redo()
        
        assert result == command
        assert history.can_undo()
        assert not history.can_redo()
    
    def test_redo_empty_returns_none(self) -> None:
        """Test redo on empty stack returns None."""
        history = CommandHistory()
        assert history.redo() is None
    
    def test_push_clears_redo_stack(self) -> None:
        """Test push clears redo stack."""
        history = CommandHistory()
        editor = TextEditor()
        
        command1 = InsertCommand(editor, 0, "Hello")
        command2 = InsertCommand(editor, 5, " World")
        
        history.push(command1)
        history.undo()
        assert history.can_redo()
        
        history.push(command2)  # Should clear redo
        assert not history.can_redo()
    
    def test_multiple_undo_redo(self) -> None:
        """Test multiple undo and redo operations."""
        history = CommandHistory()
        editor = TextEditor()
        
        commands = [
            InsertCommand(editor, 0, "a"),
            InsertCommand(editor, 1, "b"),
            InsertCommand(editor, 2, "c"),
        ]
        
        for cmd in commands:
            history.push(cmd)
        
        # Undo all
        for _ in range(3):
            history.undo()
        
        assert not history.can_undo()
        assert history.can_redo()
        
        # Redo all
        for _ in range(3):
            history.redo()
        
        assert history.can_undo()
        assert not history.can_redo()


class TestTextEditorInvoker:
    """Test TextEditorInvoker."""
    
    def test_initialization(self) -> None:
        """Test invoker initialization."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        assert invoker.get_content() == ""
        assert not invoker.can_undo()
    
    def test_insert(self) -> None:
        """Test insert through invoker."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        invoker.insert(0, "Hello")
        assert invoker.get_content() == "Hello"
        assert invoker.can_undo()
    
    def test_delete(self) -> None:
        """Test delete through invoker."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        invoker.insert(0, "Hello World")
        invoker.delete(0, 6)
        
        assert invoker.get_content() == "World"
        assert invoker.can_undo()
    
    def test_undo_insert(self) -> None:
        """Test undo insert."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        invoker.insert(0, "Hello")
        result = invoker.undo()
        
        assert result is True
        assert invoker.get_content() == ""
        assert not invoker.can_undo()
        assert invoker.can_redo()
    
    def test_undo_delete(self) -> None:
        """Test undo delete."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        invoker.insert(0, "Hello")
        invoker.delete(0, 3)
        invoker.undo()
        
        assert invoker.get_content() == "Hello"
    
    def test_redo(self) -> None:
        """Test redo."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        invoker.insert(0, "Hello")
        invoker.undo()
        result = invoker.redo()
        
        assert result is True
        assert invoker.get_content() == "Hello"
        assert invoker.can_undo()
        assert not invoker.can_redo()
    
    def test_undo_empty_returns_false(self) -> None:
        """Test undo when nothing to undo returns False."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        assert invoker.undo() is False
    
    def test_redo_empty_returns_false(self) -> None:
        """Test redo when nothing to redo returns False."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        assert invoker.redo() is False
    
    def test_undo_redo_sequence(self) -> None:
        """Test complex undo/redo sequence."""
        editor = TextEditor()
        invoker = TextEditorInvoker(editor)
        
        # Add some text
        invoker.insert(0, "Hello")
        invoker.insert(5, " ")
        invoker.insert(6, "World")
        
        assert invoker.get_content() == "Hello World"
        
        # Undo twice
        invoker.undo()
        assert invoker.get_content() == "Hello "
        
        invoker.undo()
        assert invoker.get_content() == "Hello"
        
        # Redo once
        invoker.redo()
        assert invoker.get_content() == "Hello "
        
        # New command clears redo
        invoker.insert(6, "Python")
        assert invoker.get_content() == "Hello Python"
        assert not invoker.can_redo()
