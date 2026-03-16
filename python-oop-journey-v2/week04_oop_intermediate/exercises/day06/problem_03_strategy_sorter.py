"""Problem 03: Strategy Sorter

Topic: Composition vs Inheritance (Strategy Pattern)
Difficulty: Medium

Implement a sorting system that uses the Strategy pattern to
allow runtime selection of sorting algorithms.

Classes to implement:
- SortStrategy (abstract sorting interface)
- BubbleSortStrategy, QuickSortStrategy, MergeSortStrategy
- Sorter (context class that uses a strategy)

This demonstrates the Strategy pattern, a classic use of composition
to vary algorithms without inheritance.

Hints:
    Hint 1: The Strategy pattern uses composition - the Sorter class HAS-A
    SortStrategy, not IS-A SortStrategy. Store the strategy in an instance
    variable and delegate sorting to it.
    
    Hint 2: For comparison counting in sort methods, increment a counter
    every time you compare two elements. Return (sorted_list, comparison_count)
    as a tuple. Work with a copy of the input data (data.copy()) to avoid
    modifying the original list.
    
    Hint 3: Bubble sort uses nested loops comparing adjacent elements.
    Quick sort picks a pivot and partitions elements. Merge sort recursively
    divides and merges. Quick and merge sorts are naturally recursive.
    The Sorter.sort() method should delegate to strategy.sort() and format
    the result with strategy name and complexity.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SortStrategy(ABC):
    """Abstract strategy for sorting."""

    @abstractmethod
    def sort(self, data: list[int]) -> tuple[list[int], int]:
        """Sort the data and return (sorted_list, comparison_count).
        
        Returns:
            Tuple of (sorted_list, number_of_comparisons)
        """
        raise NotImplementedError("Implement sort")

    @property
    @abstractmethod
    def name(self) -> str:
        """Return strategy name."""
        raise NotImplementedError("Implement name")

    @property
    @abstractmethod
    def complexity(self) -> str:
        """Return time complexity notation."""
        raise NotImplementedError("Implement complexity")


class BubbleSortStrategy(SortStrategy):
    """Bubble sort implementation."""

    def sort(self, data: list[int]) -> tuple[list[int], int]:
        """Sort using bubble sort.
        
        Count every comparison between elements.
        """
        raise NotImplementedError("Implement sort")

    @property
    def name(self) -> str:
        raise NotImplementedError("Implement name")

    @property
    def complexity(self) -> str:
        return "O(n²)"


class QuickSortStrategy(SortStrategy):
    """Quick sort implementation."""

    def sort(self, data: list[int]) -> tuple[list[int], int]:
        """Sort using quick sort with comparison counting."""
        raise NotImplementedError("Implement sort")

    @property
    def name(self) -> str:
        raise NotImplementedError("Implement name")

    @property
    def complexity(self) -> str:
        return "O(n log n)"


class MergeSortStrategy(SortStrategy):
    """Merge sort implementation."""

    def sort(self, data: list[int]) -> tuple[list[int], int]:
        """Sort using merge sort with comparison counting."""
        raise NotImplementedError("Implement sort")

    @property
    def name(self) -> str:
        raise NotImplementedError("Implement name")

    @property
    def complexity(self) -> str:
        return "O(n log n)"


class Sorter:
    """Context class that uses a sorting strategy.
    
    This class demonstrates composition by delegating the sorting
    operation to a strategy object rather than implementing
    sorting algorithms directly or inheriting them.
    """

    def __init__(self, strategy: SortStrategy) -> None:
        raise NotImplementedError("Implement __init__")

    def sort(self, data: list[int]) -> dict[str, Any]:
        """Sort data using current strategy.
        
        Returns dict with:
            sorted_data, comparison_count, strategy_name, complexity
        """
        raise NotImplementedError("Implement sort")

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Change sorting strategy at runtime."""
        raise NotImplementedError("Implement set_strategy")

    def compare_strategies(
        self,
        data: list[int],
        strategies: list[SortStrategy],
    ) -> list[dict[str, Any]]:
        """Run multiple strategies and compare results.
        
        Returns list of results from each strategy.
        """
        raise NotImplementedError("Implement compare_strategies")

    def get_current_strategy_info(self) -> dict[str, str]:
        raise NotImplementedError("Implement get_current_strategy_info")
