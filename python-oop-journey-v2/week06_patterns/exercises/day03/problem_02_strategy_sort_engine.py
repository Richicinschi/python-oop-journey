"""Problem 02: Strategy Sort Engine

Topic: Strategy Pattern
Difficulty: Medium

Implement the Strategy pattern for a sorting engine with multiple algorithms.

HINTS:
- Hint 1 (Conceptual): The SortEngine should not know which algorithm it's using.
  It just calls strategy.sort(data) and returns the result.
- Hint 2 (Structural): SortStrategy has sort() method. Each concrete strategy 
  implements its own sorting logic. SortEngine has set_strategy() to switch 
  algorithms at runtime.
- Hint 3 (Edge Case): Always work on a copy of the data to avoid modifying the 
  original list. Return a new sorted list, not the original.

PATTERN EXPLANATION:
The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable. Strategy lets the algorithm vary independently
from clients that use it.

STRUCTURE:
- Strategy (SortStrategy): Common interface for all algorithms
- ConcreteStrategy (BubbleSort, QuickSort, MergeSort): Specific implementations
- Context (SortEngine): Uses a strategy and delegates algorithm execution

WHEN TO USE:
- When you have multiple ways to do something (sorting, validation, etc.)
- When you need to switch algorithms at runtime
- To avoid conditional statements for selecting behavior

EXAMPLE USAGE:
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    
    # Use bubble sort
    engine = SortEngine(BubbleSortStrategy())
    result = engine.sort(data)
    
    # Switch to quicksort at runtime
    engine.strategy = QuickSortStrategy()
    result = engine.sort(data)
    
    print(engine.get_strategy_name())  # "Quick Sort"

TODO:
1. Create SortStrategy abstract base class with sort(self, data: list) method
2. Create SortEngine context class that uses a strategy
3. Implement BubbleSortStrategy
4. Implement QuickSortStrategy
5. Implement MergeSortStrategy
6. Allow runtime strategy switching in SortEngine
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class SortStrategy(ABC):
    """Abstract strategy for sorting algorithms."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data and return a new sorted list.
        
        Args:
            data: List of integers to sort.
        
        Returns:
            New sorted list in ascending order.
        """
        # TODO: Implement abstract sort method
        raise NotImplementedError("sort must be implemented")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the sorting algorithm.
        
        Returns:
            Algorithm name.
        """
        # TODO: Return algorithm name
        raise NotImplementedError("name must be implemented")


class BubbleSortStrategy(SortStrategy):
    """Bubble sort algorithm implementation."""
    
    @property
    def name(self) -> str:
        """Get algorithm name."""
        # TODO: Return "Bubble Sort"
        raise NotImplementedError("Return algorithm name")
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using bubble sort algorithm.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        # TODO: Implement bubble sort
        # Make a copy, then bubble sort in-place
        raise NotImplementedError("Implement bubble sort")


class QuickSortStrategy(SortStrategy):
    """Quick sort algorithm implementation."""
    
    @property
    def name(self) -> str:
        """Get algorithm name."""
        # TODO: Return "Quick Sort"
        raise NotImplementedError("Return algorithm name")
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using quick sort algorithm.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        # TODO: Implement quick sort
        # Use recursive approach or helper function
        raise NotImplementedError("Implement quick sort")


class MergeSortStrategy(SortStrategy):
    """Merge sort algorithm implementation."""
    
    @property
    def name(self) -> str:
        """Get algorithm name."""
        # TODO: Return "Merge Sort"
        raise NotImplementedError("Return algorithm name")
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using merge sort algorithm.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        # TODO: Implement merge sort
        # Use recursive divide-and-conquer approach
        raise NotImplementedError("Implement merge sort")


class SortEngine:
    """Context class that uses a sorting strategy."""
    
    def __init__(self, strategy: SortStrategy) -> None:
        """Initialize with a sorting strategy.
        
        Args:
            strategy: The sorting strategy to use.
        """
        # TODO: Store the strategy
        raise NotImplementedError("Initialize with strategy")
    
    @property
    def strategy(self) -> SortStrategy:
        """Get current strategy.
        
        Returns:
            Current sorting strategy.
        """
        # TODO: Return current strategy
        raise NotImplementedError("Return strategy")
    
    @strategy.setter
    def strategy(self, strategy: SortStrategy) -> None:
        """Change the sorting strategy.
        
        Args:
            strategy: New strategy to use.
        """
        # TODO: Update strategy
        raise NotImplementedError("Set strategy")
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort data using current strategy.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        # TODO: Delegate to strategy's sort method
        raise NotImplementedError("Delegate to strategy")
    
    def get_strategy_name(self) -> str:
        """Get the name of current strategy.
        
        Returns:
            Strategy name.
        """
        # TODO: Return strategy name
        raise NotImplementedError("Return strategy name")
