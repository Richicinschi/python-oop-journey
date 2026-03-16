"""Tests for Problem 05: History Buffer."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day05.problem_05_history_buffer import (
    HistoryBuffer, ReversibleHistoryBuffer
)


class TestHistoryBufferInit:
    """Tests for HistoryBuffer initialization."""
    
    def test_init_basic(self) -> None:
        hb = HistoryBuffer(5)
        assert len(hb) == 0
    
    def test_init_invalid_capacity_zero(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            HistoryBuffer(0)
    
    def test_init_invalid_capacity_negative(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            HistoryBuffer(-5)


class TestHistoryBufferAppend:
    """Tests for append method."""
    
    def test_append_single_item(self) -> None:
        hb = HistoryBuffer(5)
        hb.append("a")
        assert len(hb) == 1
    
    def test_append_multiple_items(self) -> None:
        hb = HistoryBuffer(5)
        for i in range(3):
            hb.append(i)
        assert len(hb) == 3
    
    def test_append_at_capacity(self) -> None:
        hb = HistoryBuffer(3)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        assert len(hb) == 3
    
    def test_append_overwrites_oldest(self) -> None:
        hb = HistoryBuffer(3)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        hb.append(4)  # Overwrites 1
        assert list(hb) == [2, 3, 4]


class TestHistoryBufferIteration:
    """Tests for iteration (oldest to newest)."""
    
    def test_iteration_order(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        assert list(hb) == [1, 2, 3]
    
    def test_iteration_after_overwrite(self) -> None:
        hb = HistoryBuffer(3)
        for i in range(5):
            hb.append(i)
        assert list(hb) == [2, 3, 4]
    
    def test_iteration_empty(self) -> None:
        hb = HistoryBuffer(5)
        assert list(hb) == []


class TestHistoryBufferGetItem:
    """Tests for __getitem__ method."""
    
    def test_getitem_positive_index(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(10)
        hb.append(20)
        hb.append(30)
        assert hb[0] == 10  # oldest
        assert hb[1] == 20
        assert hb[2] == 30  # newest
    
    def test_getitem_negative_index(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(10)
        hb.append(20)
        hb.append(30)
        assert hb[-1] == 30  # newest
        assert hb[-2] == 20
        assert hb[-3] == 10  # oldest
    
    def test_getitem_out_of_range(self) -> None:
        hb = HistoryBuffer(3)
        hb.append(1)
        hb.append(2)
        with pytest.raises(IndexError):
            hb[5]
    
    def test_getitem_empty_buffer(self) -> None:
        hb = HistoryBuffer(3)
        with pytest.raises(IndexError):
            hb[0]


class TestHistoryBufferIsFull:
    """Tests for is_full method."""
    
    def test_is_full_false(self) -> None:
        hb = HistoryBuffer(3)
        hb.append(1)
        assert not hb.is_full()
    
    def test_is_full_true(self) -> None:
        hb = HistoryBuffer(2)
        hb.append(1)
        hb.append(2)
        assert hb.is_full()
    
    def test_is_full_after_overwrite(self) -> None:
        hb = HistoryBuffer(2)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        assert hb.is_full()


class TestHistoryBufferClear:
    """Tests for clear method."""
    
    def test_clear_removes_all_items(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(1)
        hb.append(2)
        hb.clear()
        assert len(hb) == 0
    
    def test_clear_allows_reuse(self) -> None:
        hb = HistoryBuffer(3)
        hb.append(1)
        hb.append(2)
        hb.clear()
        hb.append(3)
        assert list(hb) == [3]


class TestHistoryBufferPeek:
    """Tests for peek methods."""
    
    def test_peek_newest(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(10)
        hb.append(20)
        assert hb.peek_newest() == 20
    
    def test_peek_oldest(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(10)
        hb.append(20)
        assert hb.peek_oldest() == 10
    
    def test_peek_newest_empty_raises(self) -> None:
        hb = HistoryBuffer(3)
        with pytest.raises(IndexError, match="empty"):
            hb.peek_newest()
    
    def test_peek_oldest_empty_raises(self) -> None:
        hb = HistoryBuffer(3)
        with pytest.raises(IndexError, match="empty"):
            hb.peek_oldest()
    
    def test_peek_after_overwrite(self) -> None:
        hb = HistoryBuffer(2)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        assert hb.peek_oldest() == 2
        assert hb.peek_newest() == 3


class TestReversibleHistoryBuffer:
    """Tests for ReversibleHistoryBuffer class."""
    
    def test_reverse_iteration(self) -> None:
        hb = ReversibleHistoryBuffer(5)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        assert list(reversed(hb)) == [3, 2, 1]
    
    def test_reverse_iteration_after_overwrite(self) -> None:
        hb = ReversibleHistoryBuffer(3)
        for i in range(5):
            hb.append(i)
        assert list(reversed(hb)) == [4, 3, 2]
    
    def test_reverse_empty(self) -> None:
        hb = ReversibleHistoryBuffer(3)
        assert list(reversed(hb)) == []
    
    def test_inherits_from_history_buffer(self) -> None:
        hb = ReversibleHistoryBuffer(3)
        assert isinstance(hb, HistoryBuffer)
    
    def test_normal_iteration_still_works(self) -> None:
        hb = ReversibleHistoryBuffer(3)
        hb.append(1)
        hb.append(2)
        hb.append(3)
        assert list(hb) == [1, 2, 3]
        assert list(reversed(hb)) == [3, 2, 1]


class TestHistoryBufferIntegration:
    """Integration tests."""
    
    def test_full_buffer_lifecycle(self) -> None:
        hb = HistoryBuffer(3)
        
        # Fill buffer
        hb.append("a")
        hb.append("b")
        hb.append("c")
        assert len(hb) == 3
        assert hb.is_full()
        assert list(hb) == ["a", "b", "c"]
        
        # Overwrite oldest
        hb.append("d")
        assert len(hb) == 3
        assert list(hb) == ["b", "c", "d"]
        
        # Clear and refill
        hb.clear()
        hb.append("x")
        assert list(hb) == ["x"]
    
    def test_buffer_with_different_types(self) -> None:
        hb = HistoryBuffer(5)
        hb.append(1)
        hb.append("string")
        hb.append([1, 2, 3])
        hb.append({"key": "value"})
        assert len(hb) == 4
