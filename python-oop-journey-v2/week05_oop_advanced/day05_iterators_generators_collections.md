# Day 5: Iterators, Generators, and Custom Collections

## Learning Objectives

By the end of this day, you will be able to:

1. Implement the iterator protocol with `__iter__` and `__next__`
2. Create generators using `yield` for memory-efficient iteration
3. Build custom collection classes that support iteration
4. Understand the difference between iterators and iterables
5. Use generator expressions for concise data processing
6. Implement the `collections.abc` interfaces for custom containers
7. Handle iteration edge cases like `StopIteration`

---

## Key Concepts

### 1. Iterator Protocol: `__iter__` and `__next__`

Python's iterator protocol requires two special methods:

```python
class CountDown:
    """A custom iterator that counts down from a number."""
    
    def __init__(self, start: int) -> None:
        self.start = start
        self.current = start
    
    def __iter__(self) -> "CountDown":
        """Return the iterator object itself."""
        self.current = self.start  # Reset for reuse
        return self
    
    def __next__(self) -> int:
        """Return the next value or raise StopIteration."""
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# Usage
countdown = CountDown(5)
for num in countdown:
    print(num)  # 5, 4, 3, 2, 1
```

**Key differences:**
- **Iterable**: Has `__iter__()` method, returns an iterator
- **Iterator**: Has `__iter__()` and `__next__()` methods
- **Iteration**: The process of calling `__next__()` until `StopIteration`

### 2. Generators with `yield`

Generators are a simpler way to create iterators:

```python
def fibonacci(n: int):
    """Generate first n Fibonacci numbers."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Usage - memory efficient!
for num in fibonacci(1000):
    print(num)  # Each number computed on demand
```

**Generator advantages:**
- Lazy evaluation: values computed only when needed
- Memory efficient: don't store entire sequence
- Cleaner syntax than `__iter__`/`__next__`
- Can represent infinite sequences

### 3. Generator Expressions

Concise syntax similar to list comprehensions:

```python
# List comprehension - creates entire list in memory
squares_list = [x**2 for x in range(1000000)]

# Generator expression - lazy evaluation
squares_gen = (x**2 for x in range(1000000))

# Usage
for sq in squares_gen:
    if sq > 100:
        break
```

### 4. Building Custom Collections

Custom collections can implement `collections.abc` interfaces:

```python
from collections.abc import MutableSequence
from typing import Iterator, overload

class SmartList(MutableSequence):
    """A list that logs all operations."""
    
    def __init__(self, initial: list | None = None) -> None:
        self._data: list = list(initial) if initial else []
        self._log: list[str] = []
    
    def __len__(self) -> int:
        return len(self._data)
    
    @overload
    def __getitem__(self, index: int) -> any: ...
    
    @overload
    def __getitem__(self, index: slice) -> list: ...
    
    def __getitem__(self, index: int | slice) -> any:
        self._log.append(f"Get item at {index}")
        return self._data[index]
    
    def __setitem__(self, index: int, value: any) -> None:
        self._log.append(f"Set item at {index} = {value}")
        self._data[index] = value
    
    def __delitem__(self, index: int) -> None:
        self._log.append(f"Delete item at {index}")
        del self._data[index]
    
    def insert(self, index: int, value: any) -> None:
        self._log.append(f"Insert {value} at {index}")
        self._data.insert(index, value)
    
    def __iter__(self) -> Iterator[any]:
        return iter(self._data)
```

### 5. Iterator States and StopIteration

Understanding iteration flow:

```python
class RangeIterator:
    """Custom range-like iterator."""
    
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start
    
    def __iter__(self) -> "RangeIterator":
        self.current = self.start
        return self
    
    def __next__(self) -> int:
        # Check if we've reached the end
        if (self.step > 0 and self.current >= self.stop) or \
           (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        
        value = self.current
        self.current += self.step
        return value
```

### 6. Delegating Iteration

Classes can delegate iteration to internal collections:

```python
class Playlist:
    """A music playlist that delegates iteration."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._tracks: list[str] = []
    
    def add_track(self, track: str) -> None:
        self._tracks.append(track)
    
    def __iter__(self) -> Iterator[str]:
        """Delegate iteration to internal list."""
        return iter(self._tracks)
    
    def shuffle_iter(self) -> Iterator[str]:
        """Return shuffled iteration."""
        import random
        shuffled = self._tracks.copy()
        random.shuffle(shuffled)
        return iter(shuffled)
```

### 7. Infinite Generators

Generators can represent infinite sequences:

```python
def count(start: int = 0, step: int = 1):
    """Infinite counter like itertools.count."""
    n = start
    while True:
        yield n
        n += step

def cycle(iterable: list):
    """Infinitely cycle through an iterable."""
    while True:
        for item in iterable:
            yield item

# Usage with islice to limit output
from itertools import islice

first_10 = list(islice(count(10), 10))
# [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
```

---

## Common Mistakes

### 1. Forgetting to Reset Iterator State

```python
# Wrong - iterator can only be used once
class BadIterator:
    def __init__(self, data: list) -> None:
        self.data = data
        self.index = 0  # Never resets!
    
    def __iter__(self) -> "BadIterator":
        return self  # Should reset index here
    
    def __next__(self) -> any:
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value

# Right - reset in __iter__
class GoodIterator:
    def __init__(self, data: list) -> None:
        self.data = data
    
    def __iter__(self) -> "GoodIterator":
        self.index = 0  # Reset here
        return self
    
    def __next__(self) -> any:
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value
```

### 2. Using Lists When Generators Would Suffice

```python
# Memory intensive - loads all data
lines = [line.strip() for line in open("huge_file.txt")]

# Memory efficient - processes one line at a time
lines = (line.strip() for line in open("huge_file.txt"))
```

### 3. Consuming Generators Multiple Times

```python
def gen_numbers():
    yield from [1, 2, 3]

numbers = gen_numbers()
print(list(numbers))  # [1, 2, 3]
print(list(numbers))  # [] - already exhausted!

# Solution: recreate generator
def get_numbers():
    return gen_numbers()  # Return fresh generator
```

### 4. Not Handling StopIteration in Manual Iteration

```python
iterator = iter([1, 2, 3])

# Risky - assumes we know the length
try:
    while True:
        print(next(iterator))
except StopIteration:
    pass  # Proper handling
```

### 5. Confusing `__iter__` Return Values

```python
# Wrong - __iter__ must return an iterator (has __next__)
class BadIterable:
    def __iter__(self) -> list:  # Wrong return type!
        return [1, 2, 3]

# Right
class GoodIterable:
    def __init__(self) -> None:
        self.data = [1, 2, 3]
    
    def __iter__(self) -> Iterator[int]:
        return iter(self.data)
```

---

## Connection to Exercises

Today's exercises build custom iterators and generators:

| Problem | Skills Practiced |
|---------|------------------|
| 01. Custom Range Iterator | `__iter__`, `__next__`, step logic |
| 02. Countdown Iterator | Reverse iteration, StopIteration |
| 03. Paginated Collection | Real-world iterator, state management |
| 04. Tree Traversal Generator | Recursive generators, yield |
| 05. History Buffer | Ring buffer, circular iteration |
| 06. Playlist Iterator | Custom collection, shuffle/repeat modes |

---

## Weekly Project Connection

The Week 5 project involves a **Task Management System**. Day 5's concepts are essential because:

- **Iterators** enable lazy loading of large task lists
- **Generators** efficiently stream task history
- **Custom collections** provide filtered views of tasks
- **Pagination** handles large task collections in the UI

---

## Quick Reference

```python
from __future__ import annotations
from typing import Iterator

# Custom Iterator Class
class MyIterator:
    def __init__(self, data: list) -> None:
        self.data = data
    
    def __iter__(self) -> MyIterator:
        self.index = 0
        return self
    
    def __next__(self) -> any:
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value

# Generator Function
def my_generator(n: int) -> Iterator[int]:
    for i in range(n):
        yield i * 2

# Generator Expression
doubled = (x * 2 for x in range(100))

# Delegating Iteration
class Container:
    def __init__(self) -> None:
        self.items: list = []
    
    def __iter__(self) -> Iterator[any]:
        return iter(self.items)
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Experiment with combining generators (e.g., `yield from`)
3. Preview Day 6: **Reflection, Introspection, and Context Managers**
