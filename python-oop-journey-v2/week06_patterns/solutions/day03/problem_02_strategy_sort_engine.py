"""Solution: Strategy Sort Engine.

Implements the Strategy pattern for sorting algorithms.
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
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the sorting algorithm.
        
        Returns:
            Algorithm name.
        """
        pass


class BubbleSortStrategy(SortStrategy):
    """Bubble sort algorithm implementation."""
    
    @property
    def name(self) -> str:
        """Get algorithm name."""
        return "Bubble Sort"
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using bubble sort algorithm.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        result = data.copy()
        n = len(result)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
                    swapped = True
            if not swapped:
                break
        return result


class QuickSortStrategy(SortStrategy):
    """Quick sort algorithm implementation."""
    
    @property
    def name(self) -> str:
        """Get algorithm name."""
        return "Quick Sort"
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using quick sort algorithm.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        if len(data) <= 1:
            return data.copy()
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return self.sort(left) + middle + self.sort(right)


class MergeSortStrategy(SortStrategy):
    """Merge sort algorithm implementation."""
    
    @property
    def name(self) -> str:
        """Get algorithm name."""
        return "Merge Sort"
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using merge sort algorithm.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        if len(data) <= 1:
            return data.copy()
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        """Merge two sorted lists.
        
        Args:
            left: Left sorted list.
            right: Right sorted list.
        
        Returns:
            Merged sorted list.
        """
        result: List[int] = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class SortEngine:
    """Context class that uses a sorting strategy."""
    
    def __init__(self, strategy: SortStrategy) -> None:
        """Initialize with a sorting strategy.
        
        Args:
            strategy: The sorting strategy to use.
        """
        self._strategy = strategy
    
    @property
    def strategy(self) -> SortStrategy:
        """Get current strategy.
        
        Returns:
            Current sorting strategy.
        """
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: SortStrategy) -> None:
        """Change the sorting strategy.
        
        Args:
            strategy: New strategy to use.
        """
        self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort data using current strategy.
        
        Args:
            data: List to sort.
        
        Returns:
            Sorted list.
        """
        return self._strategy.sort(data)
    
    def get_strategy_name(self) -> str:
        """Get the name of current strategy.
        
        Returns:
            Strategy name.
        """
        return self._strategy.name
