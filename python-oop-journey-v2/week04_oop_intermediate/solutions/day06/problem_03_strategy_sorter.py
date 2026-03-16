"""Problem 03: Strategy Sorter.

Implement the Strategy pattern with composition to allow runtime
swapping of sorting algorithms.

Classes to implement:
- SortStrategy (Protocol): Interface for sorting strategies
- BubbleSort: O(n²) simple sorting algorithm
- QuickSort: O(n log n) efficient sorting algorithm
- MergeSort: O(n log n) stable sorting algorithm
- Sorter: Context class that uses a SortStrategy

Example:
    >>> data = [64, 34, 25, 12, 22, 11, 90]
    >>> sorter = Sorter(QuickSort())
    >>> sorter.sort(data)
    [11, 12, 22, 25, 34, 64, 90]
    >>> sorter.set_strategy(BubbleSort())
    >>> sorter.sort(data)
    [11, 12, 22, 25, 34, 64, 90]
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SortStrategy(Protocol):
    """Protocol for sorting strategies.
    
    Any class implementing sort() with the correct signature
    can be used as a sort strategy.
    """
    
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        """Sort a list of integers.
        
        Args:
            data: The list to sort.
        
        Returns:
            A new sorted list (original should not be modified).
        """
        ...
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the sorting algorithm.
        
        Returns:
            Human-readable algorithm name.
        """
        ...


class BubbleSort:
    """Bubble sort algorithm implementation.
    
    Simple O(n²) algorithm, good for educational purposes
    or very small datasets.
    """
    
    def sort(self, data: list[int]) -> list[int]:
        """Sort using bubble sort algorithm.
        
        Args:
            data: The list to sort.
        
        Returns:
            A new sorted list.
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
    
    def get_name(self) -> str:
        """Get algorithm name.
        
        Returns:
            "Bubble Sort"
        """
        return "Bubble Sort"


class QuickSort:
    """Quick sort algorithm implementation.
    
    Efficient O(n log n) algorithm, good for general use.
    """
    
    def sort(self, data: list[int]) -> list[int]:
        """Sort using quick sort algorithm.
        
        Args:
            data: The list to sort.
        
        Returns:
            A new sorted list.
        """
        if len(data) <= 1:
            return data.copy()
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return self.sort(left) + middle + self.sort(right)
    
    def get_name(self) -> str:
        """Get algorithm name.
        
        Returns:
            "Quick Sort"
        """
        return "Quick Sort"


class MergeSort:
    """Merge sort algorithm implementation.
    
    Stable O(n log n) algorithm, good when stability matters.
    """
    
    def sort(self, data: list[int]) -> list[int]:
        """Sort using merge sort algorithm.
        
        Args:
            data: The list to sort.
        
        Returns:
            A new sorted list.
        """
        result = data.copy()
        self._merge_sort(result, 0, len(result) - 1)
        return result
    
    def _merge_sort(self, arr: list[int], left: int, right: int) -> None:
        """Recursive merge sort helper.
        
        Args:
            arr: The array being sorted.
            left: Left index.
            right: Right index.
        """
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(arr, left, mid)
            self._merge_sort(arr, mid + 1, right)
            self._merge(arr, left, mid, right)
    
    def _merge(self, arr: list[int], left: int, mid: int, right: int) -> None:
        """Merge two sorted subarrays.
        
        Args:
            arr: The array being merged.
            left: Left index.
            mid: Middle index.
            right: Right index.
        """
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
    
    def get_name(self) -> str:
        """Get algorithm name.
        
        Returns:
            "Merge Sort"
        """
        return "Merge Sort"


class Sorter:
    """Context class that uses a sorting strategy.
    
    This class demonstrates the Strategy pattern - it can work with
    any SortStrategy, and the strategy can be changed at runtime.
    
    Attributes:
        strategy: The current sorting strategy.
    """
    
    def __init__(self, strategy: SortStrategy) -> None:
        """Initialize with a sorting strategy.
        
        Args:
            strategy: The initial sorting strategy.
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        """Change the sorting strategy.
        
        Args:
            strategy: The new strategy to use.
        """
        self._strategy = strategy
    
    def get_strategy(self) -> SortStrategy:
        """Get the current strategy.
        
        Returns:
            The current sorting strategy.
        """
        return self._strategy
    
    def sort(self, data: list[int]) -> list[int]:
        """Sort data using the current strategy.
        
        Args:
            data: The list to sort.
        
        Returns:
            A new sorted list.
        """
        return self._strategy.sort(data)
    
    def get_strategy_name(self) -> str:
        """Get the name of the current strategy.
        
        Returns:
            Human-readable strategy name.
        """
        return self._strategy.get_name()
    
    def is_strategy(self, strategy_type: type) -> bool:
        """Check if current strategy is of a specific type.
        
        Args:
            strategy_type: The type to check against.
        
        Returns:
            True if strategy matches the type.
        """
        return isinstance(self._strategy, strategy_type)
