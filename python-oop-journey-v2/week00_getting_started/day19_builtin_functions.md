# Day 19: Built-in Functions

## Learning Objectives

By the end of this day, you will:

- Use `len()` to get the size of collections
- Generate sequences with `range()`
- Iterate with indices using `enumerate()`
- Combine iterables with `zip()`
- Sort data with `sorted()`
- Chain built-in functions together effectively

---

## Key Concepts

### 1. The `len()` Function

Returns the number of items in a collection:

```python
# With strings
len("Hello")           # 5

# With lists
len([1, 2, 3, 4])      # 4

# With dictionaries
len({"a": 1, "b": 2})  # 2

# Empty collections
len([])                # 0
len("")                # 0
```

### 2. The `range()` Function

Generates a sequence of numbers:

```python
# range(stop) - starts at 0
list(range(5))         # [0, 1, 2, 3, 4]

# range(start, stop)
list(range(2, 6))      # [2, 3, 4, 5]

# range(start, stop, step)
list(range(0, 10, 2))  # [0, 2, 4, 6, 8]
list(range(5, 0, -1))  # [5, 4, 3, 2, 1]
```

Common use case - iterating N times:

```python
for i in range(3):
    print(f"Iteration {i}")
# Iteration 0
# Iteration 1
# Iteration 2
```

### 3. The `enumerate()` Function

Adds a counter to an iterable:

```python
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start from a different number
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")
# 1: apple
# 2: banana
# 3: cherry
```

### 4. The `zip()` Function

Combines multiple iterables element-wise:

```python
names = ["Alice", "Bob", "Carol"]
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(f"{name} is {age} years old")
# Alice is 25 years old
# Bob is 30 years old
# Carol is 35 years old

# zip stops at the shortest iterable
short = ["a", "b"]
long = [1, 2, 3, 4]
list(zip(short, long))  # [("a", 1), ("b", 2)]
```

Creating dictionaries from zip:

```python
keys = ["a", "b", "c"]
values = [1, 2, 3]
dict(zip(keys, values))  # {"a": 1, "b": 2, "c": 3}
```

### 5. The `sorted()` Function

Returns a new sorted list from an iterable:

```python
# Basic sorting
sorted([3, 1, 4, 1, 5])  # [1, 1, 3, 4, 5]

# Reverse sorting
sorted([3, 1, 4], reverse=True)  # [4, 3, 1]

# Sorting strings (alphabetically)
sorted(["banana", "apple", "Cherry"])  # ['Cherry', 'apple', 'banana']

# Sorting with key function
words = ["aaa", "bb", "c"]
sorted(words, key=len)  # ['c', 'bb', 'aaa'] - by length
```

### 6. Chaining Built-ins

These functions work great together:

```python
# Get sorted list with original indices
data = [30, 10, 20]
for original_index, value in enumerate(data):
    print(f"Index {original_index}: {value}")

# Sort two related lists together
names = ["Charlie", "Alice", "Bob"]
scores = [85, 95, 75]

# Sort by name
sorted_pairs = sorted(zip(names, scores))
# [("Alice", 95), ("Bob", 75), ("Charlie", 85)]

# Create a numbered list
items = ["apple", "banana", "cherry"]
numbered = list(enumerate(items, 1))
# [(1, "apple"), (2, "banana"), (3, "cherry")]
```

---

## Common Mistakes

### 1. Forgetting `list()` with `range()`

```python
# range returns a range object, not a list
r = range(5)
print(r)  # range(0, 5)

# Convert to list if needed
list(r)   # [0, 1, 2, 3, 4]
```

### 2. Modifying While Iterating

```python
# Bad - modifying list while iterating
for i in range(len(my_list)):
    if condition(my_list[i]):
        my_list.pop(i)  # Dangerous!

# Better - create a new list
my_list = [x for x in my_list if not condition(x)]
```

### 3. Assuming `zip()` Result is a List

```python
z = zip([1, 2], ["a", "b"])
print(z)  # <zip object at 0x...>

# Convert to list if you need to reuse
pairs = list(zip([1, 2], ["a", "b"]))
```

### 4. Forgetting `sorted()` Returns New List

```python
# sorted() doesn't modify original
data = [3, 1, 2]
sorted_data = sorted(data)
print(data)         # [3, 1, 2] - unchanged!
print(sorted_data)  # [1, 2, 3]

# Use list.sort() for in-place sorting
data.sort()
print(data)         # [1, 2, 3] - modified
```

---

## Connection to Exercises

### Problem 01: Count Items
Use `len()` to count various collection types.

### Problem 02: Generate Range
Practice `range()` with different parameters.

### Problem 03: Enumerate Items
Add indices to iterables using `enumerate()`.

### Problem 04: Zip Data
Combine multiple lists using `zip()`.

### Problem 05: Sort Data
Sort data using `sorted()` with various options.

---

## Connection to Project

Built-in functions make the Todo List project cleaner:

```python
def display_tasks(tasks: list[dict]) -> None:
    """Display all tasks with their index."""
    # enumerate() for numbered list
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else " "
        print(f"{i}. [{status}] {task['description']}")

def sort_by_priority(tasks: list[dict]) -> list[dict]:
    """Sort tasks by priority (high → medium → low)."""
    priority_order = {"high": 0, "medium": 1, "low": 2}
    # sorted() with custom key
    return sorted(tasks, key=lambda t: priority_order[t["priority"]])

def count_pending(tasks: list[dict]) -> int:
    """Count how many tasks are pending."""
    # sum() with generator expression
    return sum(1 for task in tasks if not task["completed"])
```

---

## Tips for Success

1. **`range()` is memory efficient** - It generates numbers on demand
2. **`enumerate()` beats manual counting** - Cleaner than `range(len())`
3. **`zip()` stops at shortest** - Ensure lists are same length or handle mismatch
4. **`sorted()` always returns a list** - Original data is unchanged
5. **Chain them together** - These functions compose beautifully
