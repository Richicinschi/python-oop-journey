"""Reference solution for Problem 05: History Buffer."""

from __future__ import annotations
from typing import Iterator


class HistoryBuffer:
    """A fixed-size ring buffer with iteration support."""
    
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._buffer: list = [None] * capacity
        self._size = 0
        self._head = 0  # Position of oldest item
        self._tail = 0  # Position for next insert
    
    def append(self, item: any) -> None:
        """Add an item to the buffer."""
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        
        if self._size < self._capacity:
            self._size += 1
        else:
            # Buffer is full, head moves forward
            self._head = (self._head + 1) % self._capacity
    
    def __iter__(self) -> Iterator[any]:
        """Iterate from oldest to newest."""
        for i in range(self._size):
            idx = (self._head + i) % self._capacity
            yield self._buffer[idx]
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> any:
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        
        idx = (self._head + index) % self._capacity
        return self._buffer[idx]
    
    def is_full(self) -> bool:
        return self._size == self._capacity
    
    def clear(self) -> None:
        self._size = 0
        self._head = 0
        self._tail = 0
        self._buffer = [None] * self._capacity
    
    def peek_newest(self) -> any:
        if self._size == 0:
            raise IndexError("buffer is empty")
        idx = (self._tail - 1) % self._capacity
        return self._buffer[idx]
    
    def peek_oldest(self) -> any:
        if self._size == 0:
            raise IndexError("buffer is empty")
        return self._buffer[self._head]


class ReversibleHistoryBuffer(HistoryBuffer):
    """History buffer that supports reverse iteration."""
    
    def __reversed__(self) -> Iterator[any]:
        """Iterate from newest to oldest."""
        for i in range(self._size - 1, -1, -1):
            idx = (self._head + i) % self._capacity
            yield self._buffer[idx]
