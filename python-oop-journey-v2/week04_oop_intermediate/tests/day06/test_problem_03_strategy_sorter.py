"""Tests for Problem 03: Strategy Sorter."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day06.problem_03_strategy_sorter import (
    BubbleSort,
    MergeSort,
    QuickSort,
    SortStrategy,
    Sorter,
)


class TestBubbleSort:
    """Tests for the BubbleSort strategy."""
    
    def test_bubble_sort_basic(self) -> None:
        """Test basic bubble sort functionality."""
        sorter = BubbleSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
    
    def test_bubble_sort_empty(self) -> None:
        """Test sorting empty list."""
        sorter = BubbleSort()
        assert sorter.sort([]) == []
    
    def test_bubble_sort_single_element(self) -> None:
        """Test sorting single element."""
        sorter = BubbleSort()
        assert sorter.sort([42]) == [42]
    
    def test_bubble_sort_already_sorted(self) -> None:
        """Test sorting already sorted list."""
        sorter = BubbleSort()
        data = [1, 2, 3, 4, 5]
        assert sorter.sort(data) == [1, 2, 3, 4, 5]
    
    def test_bubble_sort_reverse_sorted(self) -> None:
        """Test sorting reverse sorted list."""
        sorter = BubbleSort()
        data = [5, 4, 3, 2, 1]
        assert sorter.sort(data) == [1, 2, 3, 4, 5]
    
    def test_bubble_sort_does_not_modify_original(self) -> None:
        """Test that original list is not modified."""
        sorter = BubbleSort()
        data = [3, 1, 2]
        original = data.copy()
        sorter.sort(data)
        assert data == original
    
    def test_bubble_sort_get_name(self) -> None:
        """Test getting algorithm name."""
        sorter = BubbleSort()
        assert sorter.get_name() == "Bubble Sort"


class TestQuickSort:
    """Tests for the QuickSort strategy."""
    
    def test_quick_sort_basic(self) -> None:
        """Test basic quick sort functionality."""
        sorter = QuickSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
    
    def test_quick_sort_empty(self) -> None:
        """Test sorting empty list."""
        sorter = QuickSort()
        assert sorter.sort([]) == []
    
    def test_quick_sort_single_element(self) -> None:
        """Test sorting single element."""
        sorter = QuickSort()
        assert sorter.sort([42]) == [42]
    
    def test_quick_sort_duplicates(self) -> None:
        """Test sorting with duplicate values."""
        sorter = QuickSort()
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        assert sorter.sort(data) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_quick_sort_does_not_modify_original(self) -> None:
        """Test that original list is not modified."""
        sorter = QuickSort()
        data = [3, 1, 2]
        original = data.copy()
        sorter.sort(data)
        assert data == original
    
    def test_quick_sort_get_name(self) -> None:
        """Test getting algorithm name."""
        sorter = QuickSort()
        assert sorter.get_name() == "Quick Sort"


class TestMergeSort:
    """Tests for the MergeSort strategy."""
    
    def test_merge_sort_basic(self) -> None:
        """Test basic merge sort functionality."""
        sorter = MergeSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
    
    def test_merge_sort_empty(self) -> None:
        """Test sorting empty list."""
        sorter = MergeSort()
        assert sorter.sort([]) == []
    
    def test_merge_sort_single_element(self) -> None:
        """Test sorting single element."""
        sorter = MergeSort()
        assert sorter.sort([42]) == [42]
    
    def test_merge_sort_stability(self) -> None:
        """Test merge sort stability (not directly testable with ints)."""
        sorter = MergeSort()
        data = [5, 2, 8, 2, 9, 1]
        result = sorter.sort(data)
        assert result == [1, 2, 2, 5, 8, 9]
    
    def test_merge_sort_does_not_modify_original(self) -> None:
        """Test that original list is not modified."""
        sorter = MergeSort()
        data = [3, 1, 2]
        original = data.copy()
        sorter.sort(data)
        assert data == original
    
    def test_merge_sort_get_name(self) -> None:
        """Test getting algorithm name."""
        sorter = MergeSort()
        assert sorter.get_name() == "Merge Sort"


class TestSorter:
    """Tests for the Sorter context class."""
    
    def test_sorter_init(self) -> None:
        """Test Sorter initialization."""
        strategy = BubbleSort()
        sorter = Sorter(strategy)
        assert sorter.get_strategy() == strategy
    
    def test_sorter_sort_delegates_to_strategy(self) -> None:
        """Test that sort delegates to the strategy."""
        sorter = Sorter(BubbleSort())
        data = [3, 1, 2]
        assert sorter.sort(data) == [1, 2, 3]
    
    def test_sorter_set_strategy(self) -> None:
        """Test changing strategy."""
        sorter = Sorter(BubbleSort())
        new_strategy = QuickSort()
        sorter.set_strategy(new_strategy)
        assert sorter.get_strategy() == new_strategy
    
    def test_sorter_get_strategy_name(self) -> None:
        """Test getting strategy name."""
        sorter = Sorter(QuickSort())
        assert sorter.get_strategy_name() == "Quick Sort"
    
    def test_sorter_is_strategy(self) -> None:
        """Test checking strategy type."""
        sorter = Sorter(BubbleSort())
        assert sorter.is_strategy(BubbleSort) is True
        assert sorter.is_strategy(QuickSort) is False
    
    def test_sorter_strategy_switching(self) -> None:
        """Test that strategy can be switched and produces correct results."""
        sorter = Sorter(BubbleSort())
        data = [5, 2, 8, 1, 9]
        
        # Sort with BubbleSort
        assert sorter.sort(data) == [1, 2, 5, 8, 9]
        
        # Switch to QuickSort
        sorter.set_strategy(QuickSort())
        assert sorter.sort(data) == [1, 2, 5, 8, 9]
        
        # Switch to MergeSort
        sorter.set_strategy(MergeSort())
        assert sorter.sort(data) == [1, 2, 5, 8, 9]
    
    def test_sorter_uses_composition(self) -> None:
        """Test that Sorter uses composition."""
        assert not issubclass(Sorter, BubbleSort)
        assert not issubclass(Sorter, QuickSort)
        assert not issubclass(Sorter, MergeSort)
