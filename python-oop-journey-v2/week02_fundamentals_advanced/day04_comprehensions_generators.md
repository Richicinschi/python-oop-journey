# Day 4: Comprehensions and Generators

## Learning Objectives

By the end of this day, you will be able to:

- Write concise and efficient list, dictionary, and set comprehensions
- Understand when to use comprehensions vs traditional loops
- Create generator functions using the `yield` keyword
- Leverage lazy evaluation for memory-efficient data processing
- Use `itertools` module for common iteration patterns
- Build memory-efficient pipelines with generator expressions
- Choose between eager and lazy evaluation strategies

---

## Key Concepts

### List Comprehensions

List comprehensions provide a concise way to create lists based on existing iterables.

```python
# Basic syntax: [expression for item in iterable]
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition: [expression for item in iterable if condition]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Nested comprehensions for flattening
matrix = [[1, 2, 3], [4, 5, 6]]
flattened = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6]
```

### Dictionary Comprehensions

Dictionary comprehensions create dictionaries using a similar syntax.

```python
# Basic syntax: {key: value for item in iterable}
words = ["apple", "banana", "cherry"]
lengths = {word: len(word) for word in words}
# {'apple': 5, 'banana': 6, 'cherry': 6}

# With condition
scores = {"Alice": 95, "Bob": 82, "Charlie": 78}
passing = {name: score for name, score in scores.items() if score >= 80}
# {'Alice': 95, 'Bob': 82}

# Inverting a dictionary
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}
```

### Set Comprehensions

Set comprehensions create sets (unique values only).

```python
# Basic syntax: {expression for item in iterable}
unique_lengths = {len(word) for word in ["apple", "banana", "cherry", "date"]}
# {4, 5, 6}

# With condition
multiples_of_three = {x for x in range(20) if x % 3 == 0}
# {0, 3, 6, 9, 12, 15, 18}
```

### Generator Functions

Generators are functions that use `yield` to produce a sequence of values lazily.

```python
def count_up_to(n: int):
    """Generate numbers from 1 to n."""
    count = 1
    while count <= n:
        yield count
        count += 1

# Usage
for num in count_up_to(5):
    print(num)  # 1, 2, 3, 4, 5

# Convert to list (consumes the generator)
numbers = list(count_up_to(3))  # [1, 2, 3]
```

Key differences from regular functions:
- Generators pause execution at `yield` and resume on next iteration
- They maintain state between calls
- They produce values one at a time (memory efficient)
- They can be infinite

### Generator Expressions

Generator expressions are like list comprehensions but return a generator object.

```python
# List comprehension (eager, stores all values)
squares_list = [x**2 for x in range(1000000)]  # Uses lots of memory

# Generator expression (lazy, yields one at a time)
squares_gen = (x**2 for x in range(1000000))  # Almost no memory

# Usage with next()
gen = (x**2 for x in range(5))
print(next(gen))  # 0
print(next(gen))  # 1
```

### The `itertools` Module

The `itertools` module provides efficient iterators for common patterns.

```python
import itertools

# islice - slice an iterator without consuming everything
first_ten = itertools.islice(itertools.count(), 10)

# chain - concatenate iterables
combined = itertools.chain([1, 2], [3, 4], [5, 6])  # 1, 2, 3, 4, 5, 6

# groupby - group consecutive equal elements
data = ["apple", "apricot", "banana", "blueberry", "cherry"]
for letter, words in itertools.groupby(data, key=lambda x: x[0]):
    print(letter, list(words))
# a ['apple', 'apricot']
# b ['banana', 'blueberry']
# c ['cherry']

# combinations and permutations
list(itertools.combinations([1, 2, 3], 2))  # [(1, 2), (1, 3), (2, 3)]
list(itertools.permutations([1, 2], 2))     # [(1, 2), (2, 1)]
```

### Lazy Evaluation Patterns

Generators enable lazy evaluation - computing values only when needed.

```python
# Processing large files line by line
def process_large_file(filename: str):
    with open(filename) as f:
        for line in f:
            yield line.strip().upper()

# Chaining operations without intermediate storage
def pipeline(data):
    # Each step yields one item at a time
    step1 = (x * 2 for x in data)           # Double each
    step2 = (x for x in step1 if x > 10)    # Filter
    step3 = (x ** 2 for x in step2)         # Square
    return step3

# Nothing computed until we iterate
result = pipeline(range(100))
for value in result:
    print(value)  # Process one at a time
```

---

## Common Mistakes

### 1. Consuming a Generator Multiple Times

```python
# WRONG: Generators can only be iterated once
def get_numbers():
    yield from [1, 2, 3]

nums = get_numbers()
print(list(nums))  # [1, 2, 3]
print(list(nums))  # [] - already exhausted!

# CORRECT: Create a new generator each time
print(list(get_numbers()))  # [1, 2, 3]
print(list(get_numbers()))  # [1, 2, 3]
```

### 2. Using List Comprehension When Generator Expression Suffices

```python
# WRONG: Creates entire list in memory
result = sum([x**2 for x in range(1000000)])

# CORRECT: Generator expression computes one at a time
result = sum(x**2 for x in range(1000000))
```

### 3. Modifying Collection During Comprehension

```python
# WRONG: Unpredictable behavior
items = [1, 2, 3, 4, 5]
result = [items.pop() for _ in items]  # Don't do this!

# CORRECT: Create new collection
def process(items):
    return [x * 2 for x in items]
```

### 4. Forgetting That `zip()` Returns an Iterator in Python 3

```python
# In Python 3, zip() returns an iterator (like a generator)
z = zip([1, 2], ['a', 'b'])
print(list(z))  # [(1, 'a'), (2, 'b')]
print(list(z))  # [] - exhausted!

# CORRECT: Convert to list if you need multiple passes
pairs = list(zip([1, 2], ['a', 'b']))
```

### 5. Creating Nested List Comprehensions That Are Hard to Read

```python
# WRONG: Too complex, hard to understand
result = [[x * y for y in range(10) if y % 2 == 0] for x in range(10) if x > 5]

# CORRECT: Break into steps or use helper functions
def get_even_multiples(x: int) -> list[int]:
    return [x * y for y in range(10) if y % 2 == 0]

result = [get_even_multiples(x) for x in range(10) if x > 5]
```

### 6. Using Mutable Default Arguments in Generators

```python
# WRONG: Mutable default is shared across calls
def accumulate(values, running=[]):
    for v in values:
        running.append(v)
        yield sum(running)

# CORRECT: Use None as default
def accumulate(values, running=None):
    if running is None:
        running = []
    for v in values:
        running.append(v)
        yield sum(running)
```

---

## Connection to Exercises

| Exercise | Concept Practice |
|----------|-----------------|
| 01. Flatten Nested List | Nested comprehensions, flattening 2D data |
| 02. Invert Dictionary | Dictionary comprehension, key-value swapping |
| 03. Matrix Transpose | Nested comprehensions, 2D data transformation |
| 04. Even Square Map | List comprehension with filtering |
| 05. Word Length Histogram | Dictionary comprehension, aggregation |
| 06. Unique Pairs | Set comprehension, itertools.combinations |
| 07. Running Total Generator | yield, maintaining state in generators |
| 08. Fibonacci Generator | Infinite sequences with yield |
| 09. Chunked Iterator | yield, itertools.islice, batch processing |
| 10. Lazy Filter Map | Chaining generators, lazy evaluation |

---

## Weekly Project Connection

The Week 2 project (Procedural Library System) uses comprehensions and generators:

- **Book filtering**: List comprehensions to filter by genre or author
- **Report generation**: Generators for processing large catalogs efficiently
- **Search results**: Lazy generators for paginated result sets
- **Statistics**: Dictionary comprehensions for aggregating book data
- **Export functions**: Generator-based writers for CSV/JSON

Mastering comprehensions and generators will make your library system efficient and memory-friendly when handling large collections.

---

## Summary

- **Comprehensions** (list, dict, set) provide concise syntax for transforming iterables
- **Generators** enable lazy evaluation, computing values on-demand
- **Generator expressions** are memory-efficient alternatives to list comprehensions
- **`yield`** transforms a function into a generator, pausing and resuming execution
- **`itertools`** provides battle-tested utilities for iteration patterns
- Use **lazy evaluation** for large datasets or infinite sequences
- Choose **eager evaluation** (lists) when you need random access or multiple passes
