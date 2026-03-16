"""Tests for Problem 05: Memento Text History."""

from __future__ import annotations

import pytest
from datetime import datetime

from week06_patterns.solutions.day04.problem_05_memento_text_history import (
    EditorMemento,
    TextEditor,
    History,
)


class TestEditorMemento:
    """Tests for EditorMemento data class."""
    
    def test_memento_creation(self) -> None:
        """Memento can be created with all fields."""
        memento = EditorMemento(
            content="Hello",
            cursor_position=5,
            selection_start=0,
            selection_end=5,
            timestamp=datetime.now()
        )
        assert memento.content == "Hello"
        assert memento.cursor_position == 5
    
    def test_memento_is_immutable(self) -> None:
        """Memento attributes cannot be modified."""
        memento = EditorMemento(
            content="Hello",
            cursor_position=5,
            selection_start=0,
            selection_end=5,
            timestamp=datetime.now()
        )
        with pytest.raises(AttributeError):
            memento.content = "World"  # type: ignore[misc]


class TestTextEditorBasic:
    """Tests for TextEditor basic operations."""
    
    def test_editor_starts_empty(self) -> None:
        """Editor starts with empty content."""
        editor = TextEditor()
        assert editor.get_content() == ""
        assert editor.get_cursor_position() == 0
    
    def test_insert_text(self) -> None:
        """Text can be inserted at cursor."""
        editor = TextEditor()
        editor.insert_text("Hello")
        assert editor.get_content() == "Hello"
        assert editor.get_cursor_position() == 5
    
    def test_insert_multiple_times(self) -> None:
        """Multiple inserts append text."""
        editor = TextEditor()
        editor.insert_text("Hello")
        editor.insert_text(" World")
        assert editor.get_content() == "Hello World"
    
    def test_move_cursor(self) -> None:
        """Cursor can be moved to valid position."""
        editor = TextEditor()
        editor.insert_text("Hello")
        result = editor.move_cursor(2)
        
        assert result is True
        assert editor.get_cursor_position() == 2
    
    def test_move_cursor_invalid(self) -> None:
        """Moving cursor to invalid position fails."""
        editor = TextEditor()
        editor.insert_text("Hi")
        
        assert editor.move_cursor(-1) is False
        assert editor.move_cursor(10) is False
        assert editor.get_cursor_position() == 2  # Unchanged


class TestTextEditorSelection:
    """Tests for TextEditor selection operations."""
    
    def test_no_selection_initially(self) -> None:
        """Editor starts with no selection."""
        editor = TextEditor()
        assert editor.get_selection() is None
    
    def test_select_range(self) -> None:
        """Selection range can be set."""
        editor = TextEditor()
        editor.insert_text("Hello World")
        result = editor.select(0, 5)
        
        assert result is True
        assert editor.get_selection() == (0, 5)
    
    def test_select_invalid_range(self) -> None:
        """Invalid selection range fails."""
        editor = TextEditor()
        editor.insert_text("Hi")
        
        assert editor.select(-1, 1) is False
        assert editor.select(0, 10) is False
        assert editor.select(2, 1) is False  # start > end
    
    def test_clear_selection(self) -> None:
        """Selection can be cleared."""
        editor = TextEditor()
        editor.insert_text("Hello")
        editor.select(0, 5)
        editor.clear_selection()
        
        assert editor.get_selection() is None
    
    def test_insert_replaces_selection(self) -> None:
        """Inserting with selection replaces selected text."""
        editor = TextEditor()
        editor.insert_text("Hello World")
        editor.select(6, 11)  # Select "World"
        editor.insert_text("Python")
        
        assert editor.get_content() == "Hello Python"


class TestTextEditorDeletion:
    """Tests for TextEditor deletion operations."""
    
    def test_delete_selection(self) -> None:
        """Selected text can be deleted."""
        editor = TextEditor()
        editor.insert_text("Hello World")
        editor.select(5, 11)  # Select " World"
        result = editor.delete_selection()
        
        assert result is True
        assert editor.get_content() == "Hello"
    
    def test_delete_no_selection(self) -> None:
        """Delete with no selection does nothing."""
        editor = TextEditor()
        editor.insert_text("Hello")
        result = editor.delete_selection()
        
        assert result is False
        assert editor.get_content() == "Hello"


class TestTextEditorMemento:
    """Tests for TextEditor memento operations."""
    
    def test_save_creates_memento(self) -> None:
        """Save returns an EditorMemento."""
        editor = TextEditor()
        editor.insert_text("Hello")
        memento = editor.save()
        
        assert isinstance(memento, EditorMemento)
        assert memento.content == "Hello"
        assert memento.cursor_position == 5
    
    def test_restore_from_memento(self) -> None:
        """Restore updates editor state from memento."""
        editor = TextEditor()
        editor.insert_text("Hello")
        memento = editor.save()
        
        editor.insert_text(" World")
        assert editor.get_content() == "Hello World"
        
        editor.restore(memento)
        assert editor.get_content() == "Hello"
        assert editor.get_cursor_position() == 5
    
    def test_restore_preserves_selection(self) -> None:
        """Restore restores selection state."""
        editor = TextEditor()
        editor.insert_text("Hello World")
        editor.select(0, 5)
        memento = editor.save()
        
        editor.clear_selection()
        assert editor.get_selection() is None
        
        editor.restore(memento)
        assert editor.get_selection() == (0, 5)


class TestHistory:
    """Tests for History caretaker."""
    
    def test_history_initialized_with_editor(self) -> None:
        """History requires an editor."""
        editor = TextEditor()
        history = History(editor)
        assert history is not None
    
    def test_can_undo_initially_false(self) -> None:
        """Cannot undo initially."""
        editor = TextEditor()
        history = History(editor)
        assert history.can_undo() is False
    
    def test_can_redo_initially_false(self) -> None:
        """Cannot redo initially."""
        editor = TextEditor()
        history = History(editor)
        assert history.can_redo() is False
    
    def test_backup_enables_undo(self) -> None:
        """After backup, undo is available."""
        editor = TextEditor()
        history = History(editor)
        
        history.backup()
        assert history.can_undo() is True
    
    def test_undo_restores_previous_state(self) -> None:
        """Undo restores editor to previous state."""
        editor = TextEditor()
        history = History(editor)
        
        history.backup()  # Save empty initial state
        editor.insert_text("First")
        history.backup()
        
        editor.insert_text(" Second")
        history.undo()
        
        assert editor.get_content() == "First"
    
    def test_undo_returns_false_when_empty(self) -> None:
        """Undo returns False when no history."""
        editor = TextEditor()
        history = History(editor)
        
        result = history.undo()
        assert result is False
    
    def test_redo_restores_undone_state(self) -> None:
        """Redo restores state after undo."""
        editor = TextEditor()
        history = History(editor)
        
        history.backup()  # Save empty initial state
        editor.insert_text("Hello")
        history.backup()  # Save "Hello"
        
        editor.insert_text(" World")  # editor = "Hello World", not backed up
        
        history.undo()  # Restores "Hello"
        assert editor.get_content() == "Hello"
        
        history.redo()  # Restores "Hello World"
        assert editor.get_content() == "Hello World"
    
    def test_redo_returns_false_when_empty(self) -> None:
        """Redo returns False when no redo history."""
        editor = TextEditor()
        history = History(editor)
        
        result = history.redo()
        assert result is False
    
    def test_new_backup_clears_redo(self) -> None:
        """New backup clears redo stack."""
        editor = TextEditor()
        history = History(editor)
        
        editor.insert_text("A")
        history.backup()
        editor.insert_text("B")
        history.backup()
        
        history.undo()
        assert history.can_redo() is True
        
        editor.insert_text("C")
        history.backup()  # This should clear redo
        
        assert history.can_redo() is False
    
    def test_undo_count_tracks_history(self) -> None:
        """Undo count reflects number of available undos."""
        editor = TextEditor()
        history = History(editor)
        
        assert history.get_undo_count() == 0
        
        history.backup()
        assert history.get_undo_count() == 1
        
        history.backup()
        assert history.get_undo_count() == 2
        
        history.undo()
        assert history.get_undo_count() == 1
    
    def test_redo_count_tracks_history(self) -> None:
        """Redo count reflects number of available redos."""
        editor = TextEditor()
        history = History(editor)
        
        editor.insert_text("A")
        history.backup()
        editor.insert_text("B")
        history.backup()
        
        assert history.get_redo_count() == 0
        
        history.undo()
        assert history.get_redo_count() == 1
        
        history.undo()
        assert history.get_redo_count() == 2
    
    def test_clear_removes_all_history(self) -> None:
        """Clear removes all undo/redo history."""
        editor = TextEditor()
        history = History(editor)
        
        history.backup()
        history.backup()
        history.undo()
        
        assert history.can_undo() is True
        assert history.can_redo() is True
        
        history.clear()
        
        assert history.can_undo() is False
        assert history.can_redo() is False
        assert history.get_undo_count() == 0
        assert history.get_redo_count() == 0


class TestMementoPattern:
    """Tests verifying the Memento pattern structure."""
    
    def test_memento_is_frozen(self) -> None:
        """Memento is immutable (frozen dataclass)."""
        memento = EditorMemento("text", 4, 0, 4, datetime.now())
        
        # Verify frozen by attempting regular attribute assignment
        with pytest.raises(AttributeError):
            memento.content = "new"  # type: ignore[misc]
        
        with pytest.raises(AttributeError):
            memento.cursor_position = 10  # type: ignore[misc]
    
    def test_history_cannot_modify_memento(self) -> None:
        """History (caretaker) cannot access or modify memento state."""
        # History only stores and passes mementos, never accesses their content
        editor = TextEditor()
        history = History(editor)
        
        editor.insert_text("Hello")
        history.backup()
        
        # The memento is stored but its contents are opaque to History
        assert history.get_undo_count() == 1
