# Day 6: Performance and Optimization

## Learning Objectives

By the end of this day, you will:

- Understand how `__slots__` reduces memory usage and when to use it
- Implement caching strategies using `functools.lru_cache` and custom caches
- Apply lazy loading patterns to defer expensive operations
- Use batching to reduce overhead in database/repository operations
- Profile Python code and identify optimization opportunities

---

## 1. Memory Optimization with `__slots__`

By default, Python objects store attributes in a dynamic dictionary (`__dict__`). This provides flexibility but has memory overhead.

### Using `__slots__`

`__slots__` pre-declares the attributes an instance will have, avoiding `__dict__` creation:

```python
class PointDict:
    """Standard class with __dict__."""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class PointSlots:
    """Memory-optimized class with __slots__."""
    __slots__ = ('x', 'y')
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
```

### Trade-offs

| Aspect | `__dict__` | `__slots__` |
|--------|-----------|-------------|
| Memory | Higher per-instance | Lower per-instance |
| Flexibility | Can add attributes dynamically | Fixed attributes |
| Performance | Slower attribute access | Faster attribute access |
| Weakrefs | Supported by default | Must add `'__weakref__'` to slots |
| Inheritance | Simple | Requires careful handling |

### When to Use `__slots__`

- You will create many instances (thousands+)
- The attribute set is fixed and known
- Memory is constrained (embedded, data processing)
- You need faster attribute access

---

## 2. Caching Strategies

Caching stores expensive computation results to avoid redundant work.

### `functools.lru_cache`

Built-in decorator for memoization:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Custom Cache Implementation

For more control, implement your own cache:

```python
from typing import TypeVar, Callable

K = TypeVar('K')
V = TypeVar('V')

class SimpleCache:
    """Basic LRU cache implementation."""
    
    def __init__(self, maxsize: int = 128) -> None:
        self.maxsize = maxsize
        self._cache: dict[K, V] = {}
        self._access_order: list[K] = []
    
    def get(self, key: K) -> V | None:
        if key in self._cache:
            # Move to end (most recently used)
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None
    
    def set(self, key: K, value: V) -> None:
        if key in self._cache:
            self._access_order.remove(key)
        elif len(self._cache) >= self.maxsize:
            # Evict least recently used
            lru_key = self._access_order.pop(0)
            del self._cache[lru_key]
        
        self._cache[key] = value
        self._access_order.append(key)
```

### Cache Invalidation Strategies

1. **TTL (Time To Live)**: Expire entries after a time period
2. **LRU (Least Recently Used)**: Evict least accessed entries
3. **Size-based**: Limit by entry count or total size
4. **Manual**: Explicit invalidation on data changes

---

## 3. Lazy Loading

Lazy loading defers expensive operations until they're actually needed.

### Property-based Lazy Loading

```python
class ExpensiveResource:
    """Resource that loads data on first access."""
    
    def __init__(self) -> None:
        self._data: list[str] | None = None
    
    @property
    def data(self) -> list[str]:
        if self._data is None:
            self._data = self._load_data()
        return self._data
    
    def _load_data(self) -> list[str]:
        # Expensive operation
        return [f"item_{i}" for i in range(10000)]
```

### Lazy Collection Loading

For large collections, load in chunks or on demand:

```python
from typing import Iterator

class LazyCollection:
    """Collection that yields items on demand."""
    
    def __init__(self, source: list[int]) -> None:
        self._source = source
    
    def __iter__(self) -> Iterator[int]:
        for item in self._source:
            yield self._transform(item)
    
    def _transform(self, item: int) -> int:
        # Expensive transformation
        return item ** 2
```

---

## 4. Batching Operations

Batching reduces overhead by processing multiple items together.

### Repository Pattern with Batching

```python
from typing import TypeVar

T = TypeVar('T')

class BatchedRepository:
    """Repository that batches database operations."""
    
    def __init__(self, batch_size: int = 100) -> None:
        self.batch_size = batch_size
        self._buffer: list[T] = []
    
    def add(self, item: T) -> None:
        self._buffer.append(item)
        if len(self._buffer) >= self.batch_size:
            self._flush()
    
    def _flush(self) -> None:
        if self._buffer:
            self._save_batch(self._buffer)
            self._buffer = []
    
    def _save_batch(self, items: list[T]) -> None:
        # Single database call for multiple items
        pass
    
    def close(self) -> None:
        self._flush()  # Don't forget remaining items!
```

### Benefits of Batching

- Reduced network round-trips
- Better database utilization
- Transaction efficiency
- Memory management through controlled buffer sizes

---

## 5. Profiling Python Code

Before optimizing, measure! Use profiling tools to find actual bottlenecks.

### `cProfile` - Standard Library Profiler

```python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(10000):
        total += sum(range(i))
    return total

# Profile the function
profiler = cProfile.Profile()
profiler.enable()
result = slow_function()
profiler.disable()

# Print statistics
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

### `timeit` for Micro-benchmarks

```python
import timeit

# Compare two approaches
dict_time = timeit.timeit(
    'p = PointDict(1, 2)',
    setup='from __main__ import PointDict',
    number=100000
)

slots_time = timeit.timeit(
    'p = PointSlots(1, 2)',
    setup='from __main__ import PointSlots',
    number=100000
)

print(f"Dict: {dict_time:.4f}s, Slots: {slots_time:.4f}s")
```

### Line Profiler (External)

For line-by-line analysis:

```bash
pip install line_profiler
```

```python
from line_profiler import profile

@profile
def function_to_analyze():
    x = [i**2 for i in range(10000)]  # Line 1
    y = sum(x)                         # Line 2
    return y
```

### Profiling Best Practices

1. **Measure first**: Don't guess where bottlenecks are
2. **Profile realistic workloads**: Use real data, not tiny test cases
3. **Focus on hotspots**: 80% of time is usually in 20% of code
4. **Compare before/after**: Verify optimizations actually help
5. **Watch for overhead**: Some optimizations add complexity

---

## Common Mistakes

### 1. Premature Optimization

```python
# Don't: Optimize without profiling
# Do: Write clear code first, optimize what matters
```

### 2. Overusing `__slots__`

```python
# Don't: Use slots for every class
class TemporaryHelper:
    __slots__ = ('x',)  # Overkill for a few instances

# Do: Use slots when you have many instances
class DataPoint:
    __slots__ = ('x', 'y', 'z')  # Millions of these
```

### 3. Cache Without Invalidation

```python
# Don't: Cache without considering stale data
_cache = {}

def get_user(user_id):
    if user_id not in _cache:
        _cache[user_id] = fetch_from_db(user_id)
    return _cache[user_id]  # Never updates!

# Do: Implement TTL or manual invalidation
```

### 4. Unbounded Caches

```python
# Don't: Let cache grow forever
@lru_cache(maxsize=None)  # Dangerous for unbounded inputs
def process(item):
    return expensive(item)

# Do: Set appropriate limits
@lru_cache(maxsize=1024)
def process(item):
    return expensive(item)
```

---

## Connection to Weekly Project

In the Personal Finance Tracker project, you'll apply these concepts:

- **Slots**: Use for transaction objects when processing large datasets
- **Caching**: Cache account balances or category summaries
- **Lazy Loading**: Defer loading of historical transactions
- **Batching**: Batch database writes for imported transactions
- **Profiling**: Ensure report generation performs well with years of data

---

## Summary

| Technique | Use Case | Key Benefit |
|-----------|----------|-------------|
| `__slots__` | Many similar objects | Reduced memory |
| `lru_cache` | Expensive pure functions | Avoid recomputation |
| Lazy Loading | Large/expensive data | Defer work until needed |
| Batching | Multiple DB operations | Reduced overhead |
| Profiling | Finding bottlenecks | Data-driven optimization |

Remember: "Premature optimization is the root of all evil." Measure first, then optimize what matters.
