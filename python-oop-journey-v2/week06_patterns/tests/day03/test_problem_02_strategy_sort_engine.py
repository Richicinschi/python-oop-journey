"""Tests for Problem 02: Strategy Sort Engine."""

from __future__ import annotations

import pytest
from abc import ABC

from week06_patterns.solutions.day03.problem_02_strategy_sort_engine import (
    SortStrategy,
    BubbleSortStrategy,
    QuickSortStrategy,
    MergeSortStrategy,
    SortEngine,
)


class TestSortStrategy:
    """Test SortStrategy abstract base class."""
    
    def test_sort_strategy_is_abstract(self) -> None:
        """Test that SortStrategy cannot be instantiated."""
        assert issubclass(SortStrategy, ABC)
        with pytest.raises(TypeError, match="abstract"):
            SortStrategy()
    
    def test_sort_strategy_has_required_methods(self) -> None:
        """Test that SortStrategy defines required methods."""
        assert hasattr(SortStrategy, 'sort')
        assert hasattr(SortStrategy, 'name')


class TestBubbleSortStrategy:
    """Test BubbleSortStrategy."""
    
    def test_name(self) -> None:
        """Test algorithm name."""
        strategy = BubbleSortStrategy()
        assert strategy.name == "Bubble Sort"
    
    def test_sort_empty_list(self) -> None:
        """Test sorting empty list."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([]) == []
    
    def test_sort_single_element(self) -> None:
        """Test sorting single element."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([42]) == [42]
    
    def test_sort_already_sorted(self) -> None:
        """Test sorting already sorted list."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    
    def test_sort_unsorted(self) -> None:
        """Test sorting unsorted list."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_sort_reverse_order(self) -> None:
        """Test sorting reverse ordered list."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    def test_sort_does_not_modify_original(self) -> None:
        """Test that original list is not modified."""
        strategy = BubbleSortStrategy()
        original = [3, 1, 4, 1, 5]
        strategy.sort(original)
        assert original == [3, 1, 4, 1, 5]
    
    def test_sort_with_duplicates(self) -> None:
        """Test sorting list with duplicates."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([3, 3, 3, 1, 1]) == [1, 1, 3, 3, 3]
    
    def test_sort_with_negatives(self) -> None:
        """Test sorting list with negative numbers."""
        strategy = BubbleSortStrategy()
        assert strategy.sort([3, -1, 4, -5, 0]) == [-5, -1, 0, 3, 4]


class TestQuickSortStrategy:
    """Test QuickSortStrategy."""
    
    def test_name(self) -> None:
        """Test algorithm name."""
        strategy = QuickSortStrategy()
        assert strategy.name == "Quick Sort"
    
    def test_sort_empty_list(self) -> None:
        """Test sorting empty list."""
        strategy = QuickSortStrategy()
        assert strategy.sort([]) == []
    
    def test_sort_single_element(self) -> None:
        """Test sorting single element."""
        strategy = QuickSortStrategy()
        assert strategy.sort([42]) == [42]
    
    def test_sort_already_sorted(self) -> None:
        """Test sorting already sorted list."""
        strategy = QuickSortStrategy()
        assert strategy.sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    
    def test_sort_unsorted(self) -> None:
        """Test sorting unsorted list."""
        strategy = QuickSortStrategy()
        assert strategy.sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_sort_reverse_order(self) -> None:
        """Test sorting reverse ordered list."""
        strategy = QuickSortStrategy()
        assert strategy.sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    def test_sort_does_not_modify_original(self) -> None:
        """Test that original list is not modified."""
        strategy = QuickSortStrategy()
        original = [3, 1, 4, 1, 5]
        strategy.sort(original)
        assert original == [3, 1, 4, 1, 5]


class TestMergeSortStrategy:
    """Test MergeSortStrategy."""
    
    def test_name(self) -> None:
        """Test algorithm name."""
        strategy = MergeSortStrategy()
        assert strategy.name == "Merge Sort"
    
    def test_sort_empty_list(self) -> None:
        """Test sorting empty list."""
        strategy = MergeSortStrategy()
        assert strategy.sort([]) == []
    
    def test_sort_single_element(self) -> None:
        """Test sorting single element."""
        strategy = MergeSortStrategy()
        assert strategy.sort([42]) == [42]
    
    def test_sort_already_sorted(self) -> None:
        """Test sorting already sorted list."""
        strategy = MergeSortStrategy()
        assert strategy.sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    
    def test_sort_unsorted(self) -> None:
        """Test sorting unsorted list."""
        strategy = MergeSortStrategy()
        assert strategy.sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_sort_large_list(self) -> None:
        """Test sorting larger list."""
        strategy = MergeSortStrategy()
        data = [64, 34, 25, 12, 22, 11, 90, 5]
        assert strategy.sort(data) == [5, 11, 12, 22, 25, 34, 64, 90]
    
    def test_sort_does_not_modify_original(self) -> None:
        """Test that original list is not modified."""
        strategy = MergeSortStrategy()
        original = [3, 1, 4, 1, 5]
        strategy.sort(original)
        assert original == [3, 1, 4, 1, 5]


class TestSortEngine:
    """Test SortEngine context class."""
    
    def test_initialization(self) -> None:
        """Test engine initialization with strategy."""
        strategy = BubbleSortStrategy()
        engine = SortEngine(strategy)
        assert engine.strategy == strategy
        assert engine.get_strategy_name() == "Bubble Sort"
    
    def test_sort_delegates_to_strategy(self) -> None:
        """Test that sort delegates to strategy."""
        strategy = QuickSortStrategy()
        engine = SortEngine(strategy)
        result = engine.sort([3, 1, 4, 1, 5])
        assert result == [1, 1, 3, 4, 5]
    
    def test_strategy_switching(self) -> None:
        """Test switching strategies at runtime."""
        engine = SortEngine(BubbleSortStrategy())
        assert engine.get_strategy_name() == "Bubble Sort"
        
        engine.strategy = QuickSortStrategy()
        assert engine.get_strategy_name() == "Quick Sort"
        
        engine.strategy = MergeSortStrategy()
        assert engine.get_strategy_name() == "Merge Sort"
    
    def test_sort_after_switching(self) -> None:
        """Test sorting works after strategy switch."""
        engine = SortEngine(BubbleSortStrategy())
        data = [5, 2, 8, 1, 9]
        
        # Sort with bubble sort
        result1 = engine.sort(data)
        assert result1 == [1, 2, 5, 8, 9]
        
        # Switch to quick sort
        engine.strategy = QuickSortStrategy()
        result2 = engine.sort([5, 2, 8, 1, 9])
        assert result2 == [1, 2, 5, 8, 9]
    
    def test_all_strategies_produce_same_result(self) -> None:
        """Test that all strategies produce the same sorted output."""
        data = [64, 34, 25, 12, 22, 11, 90, 5, 42, 17]
        
        bubble = BubbleSortStrategy()
        quick = QuickSortStrategy()
        merge = MergeSortStrategy()
        
        assert bubble.sort(data) == quick.sort(data) == merge.sort(data)
