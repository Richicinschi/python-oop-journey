# Day 5: Functional Programming Basics

## Learning Objectives

By the end of this day, you will:

- Understand the principles of functional programming and pure functions
- Master `map()`, `filter()`, and `reduce()` for data transformation
- Use lambda expressions effectively for short, anonymous functions
- Create closures to capture and remember state
- Apply `functools.partial` to create specialized functions
- Compose functions to build complex operations from simple ones
- Recognize when functional approaches improve code clarity

---

## Core Concepts

### 1. Pure Functions

A pure function:
- Returns the same output for the same input (deterministic)
- Has no side effects (doesn't modify external state)
- Is easier to test, debug, and parallelize

```python
from __future__ import annotations

# Pure function - no side effects
def add(a: int, b: int) -> int:
    return a + b

# Impure function - has side effect (modifies external state)
total = 0
def add_to_total(value: int) -> int:
    global total
    total += value  # Side effect!
    return total
```

### 2. Lambda Expressions

Lambdas are anonymous functions for short, throwaway operations:

```python
from __future__ import annotations

# Regular function
def square(x: int) -> int:
    return x ** 2

# Equivalent lambda
square_lambda = lambda x: x ** 2

# Lambdas are great for short operations
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))  # [1, 4, 9, 16, 25]
```

**Best Practice:** Use lambdas for simple, one-expression functions. Use `def` for complex logic.

### 3. map(), filter(), reduce()

These functions process iterables functionally:

```python
from __future__ import annotations
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() - transform each element
doubled = list(map(lambda x: x * 2, numbers))  # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# filter() - keep elements that match condition
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4, 6, 8, 10]

# reduce() - aggregate to single value (from functools)
product = reduce(lambda acc, x: acc * x, numbers, 1)  # 3628800
```

### 4. Closures

A closure is a function that remembers values from its enclosing scope:

```python
from __future__ import annotations
from typing import Callable

def make_multiplier(factor: int) -> Callable[[int], int]:
    """Create a function that multiplies by factor."""
    def multiply(x: int) -> int:
        return x * factor  # Captures 'factor' from outer scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

Closures are powerful for:
- Factory functions
- Data hiding
- Callbacks with state
- Decorators

### 5. functools.partial

Create new functions with pre-filled arguments:

```python
from __future__ import annotations
from functools import partial
from typing import Callable

def calculate_price(base: float, tax_rate: float, discount: float) -> float:
    """Calculate final price with tax and discount."""
    after_discount = base * (1 - discount)
    return after_discount * (1 + tax_rate)

# Create specialized functions
no_tax = partial(calculate_price, tax_rate=0.0)
ten_percent_off = partial(calculate_price, discount=0.10)
standard = partial(calculate_price, tax_rate=0.08, discount=0.0)

print(standard(100.0))  # 108.0
```

### 6. Function Composition

Combine functions where output of one is input to another:

```python
from __future__ import annotations
from typing import Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(f: Callable[[U], V], g: Callable[[T], U]) -> Callable[[T], V]:
    """Compose two functions: compose(f, g)(x) == f(g(x))"""
    return lambda x: f(g(x))

# Usage
def add_one(x: int) -> int:
    return x + 1

def double(x: int) -> int:
    return x * 2

add_then_double = compose(double, add_one)
print(add_then_double(3))  # 8 (3 + 1 = 4, then 4 * 2 = 8)
```

### 7. Chaining Operations

Pipeline-style data processing:

```python
from __future__ import annotations
from typing import Callable, TypeVar

T = TypeVar('T')

def chain(initial: T, *operations: Callable[[T], T]) -> T:
    """Apply a sequence of operations to an initial value."""
    result = initial
    for op in operations:
        result = op(result)
    return result

# Usage
def strip(s: str) -> str:
    return s.strip()

def upper(s: str) -> str:
    return s.upper()

def add_exclaim(s: str) -> str:
    return s + "!"

result = chain("  hello  ", strip, upper, add_exclaim)
print(result)  # "HELLO!"
```

---

## Common Patterns

### Pipeline Pattern

```python
from __future__ import annotations
from typing import Callable, TypeVar

T = TypeVar('T')

def pipeline(data: list[T], *transforms: Callable[[list[T]], list[T]]) -> list[T]:
    """Apply a series of transformations to data."""
    result = data
    for transform in transforms:
        result = transform(result)
    return result

# Define transformations
def remove_negatives(nums: list[int]) -> list[int]:
    return [n for n in nums if n >= 0]

def double_all(nums: list[int]) -> list[int]:
    return [n * 2 for n in nums]

def take_first_n(n: int) -> Callable[[list[int]], list[int]]:
    def take(nums: list[int]) -> list[int]:
        return nums[:n]
    return take

# Execute pipeline
numbers = [-5, -2, 0, 3, 7, 10, -1, 15]
result = pipeline(numbers, remove_negatives, double_all, take_first_n(3))
print(result)  # [0, 6, 14]
```

### Sorting with Custom Keys

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    category: str

products = [
    Product("Laptop", 999.99, "Electronics"),
    Product("Book", 19.99, "Media"),
    Product("Phone", 699.99, "Electronics"),
]

# Sort by price (ascending)
by_price = sorted(products, key=lambda p: p.price)

# Sort by category then name
by_category_name = sorted(products, key=lambda p: (p.category, p.name))

# Sort by price descending
by_price_desc = sorted(products, key=lambda p: p.price, reverse=True)
```

---

## Common Mistakes

### 1. Mutable Default Arguments in Closures

```python
from __future__ import annotations
from typing import Callable

# WRONG - all closures share the same list
def wrong_adder() -> Callable[[int], list[int]]:
    items: list[int] = []  # Created once!
    def add(x: int) -> list[int]:
        items.append(x)
        return items
    return add

# CORRECT - each call gets its own list
def correct_adder() -> Callable[[int], list[int]]:
    items: list[int] = []
    def add(x: int) -> list[int]:
        items.append(x)
        return items
    return add
```

Actually, the above is a common confusion. The issue is different:

```python
from __future__ import annotations
from typing import Callable

# WRONG - late binding captures variable, not value
def create_multipliers_wrong() -> list[Callable[[int], int]]:
    return [lambda x: x * i for i in range(5)]

mults = create_multipliers_wrong()
print([m(2) for m in mults])  # [8, 8, 8, 8, 8] - all use last value of i!

# CORRECT - capture current value with default argument
def create_multipliers_correct() -> list[Callable[[int], int]]:
    return [lambda x, i=i: x * i for i in range(5)]

mults = create_multipliers_correct()
print([m(2) for m in mults])  # [0, 2, 4, 6, 8]
```

### 2. Modifying External State

```python
from __future__ import annotations

# AVOID - modifies external list
def impure_append(item: int, data: list[int]) -> list[int]:
    data.append(item)  # Side effect!
    return data

# PREFER - returns new list
from copy import deepcopy

def pure_append(item: int, data: list[int]) -> list[int]:
    new_data = deepcopy(data)
    new_data.append(item)
    return new_data
```

### 3. Overusing Lambdas

```python
from __future__ import annotations

# Hard to read
process = lambda x: (x * 2 + 10) / 5 if x > 0 else x * -1

# Better as a named function
def process(x: float) -> float:
    if x > 0:
        return (x * 2 + 10) / 5
    return x * -1
```

### 4. Forgetting to Consume Iterators

```python
from __future__ import annotations

numbers = [1, 2, 3, 4, 5]

# map() returns an iterator, not a list
doubled = map(lambda x: x * 2, numbers)
print(doubled)  # <map object at 0x...>

# Must convert to list to see results
doubled_list = list(map(lambda x: x * 2, numbers))
print(doubled_list)  # [2, 4, 6, 8, 10]
```

---

## Best Practices

1. **Prefer pure functions** when possible - easier to reason about
2. **Use type hints** for function parameters and return values
3. **Keep lambdas simple** - if it needs multiple lines, use `def`
4. **Document function contracts** - what inputs are valid, what output to expect
5. **Use functools.wraps** when writing decorators
6. **Consider operator module** for common operations:

```python
from __future__ import annotations
from operator import add, mul, itemgetter, attrgetter
from functools import reduce

# Instead of lambda x, y: x + y
sum_result = reduce(add, [1, 2, 3, 4])  # 10

# Instead of lambda x, y: x * y
product = reduce(mul, [1, 2, 3, 4])  # 24

# Get item by index/key
by_second = sorted([[1, 5], [1, 2], [1, 8]], key=itemgetter(1))
```

---

## Connection to Exercises

| Exercise | Concept Practice |
|----------|-----------------|
| 01. chain_operations | Chaining transformations, function application order |
| 02. compose_functions | Function composition, higher-order functions |
| 03. partial_discount | functools.partial, creating specialized functions |
| 04. map_filter_reduce_pipeline | Functional data processing pipelines |
| 05. custom_sort_key | Lambda expressions, sorting with key functions |
| 06. closure_counter | Closures, maintaining state across calls |
| 07. memoized_callable | Memoization, callable classes, caching |
| 08. predicate_combiner | Combining predicates, logical operations |

---

## Weekly Project Connection

The Week 2 project (Procedural Library System) applies functional programming principles:

- **Pure Functions**: `is_valid_isbn()`, `format_book_display()` have no side effects
- **Sorting**: `search_books()` uses `sorted()` with lambda key functions
- **Filtering**: `list_available_books()` uses `filter()` with predicates
- **Data Transformation**: Book data flows through transformation pipelines
- **Immutable Operations**: Consider returning new data rather than modifying in place

Example patterns from the project:
```python
# Pure function for ISBN validation
def is_valid_isbn(isbn: str) -> bool:
    return len(isbn) == 13 and isbn.isalnum()

# Sorting with key function
def search_books(library: dict, query: str) -> list[dict]:
    matches = [book for book in library.values() 
               if query.lower() in book["title"].lower()]
    return sorted(matches, key=lambda b: b["title"])

# Filtering with predicate
available_books = list(filter(
    lambda book: book["available"], 
    library.values()
))
```

---

## Further Reading

- Python `functools` module documentation
- `operator` module for functional programming
- `itertools` for efficient iteration patterns
- `toolz` library for advanced functional utilities
