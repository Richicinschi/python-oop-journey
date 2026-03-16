# Day 12: Lists Basics

## Learning Objectives

Today you'll master Python's most versatile sequence type - the list. Lists are ordered, mutable collections that can hold any type of data.

## Core Concepts

### Creating Lists

```python
# Empty list
empty = []
empty = list()

# Lists with initial values
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4], [5, 6]]

# List from other iterables
chars = list("abc")  # ['a', 'b', 'c']
range_list = list(range(5))  # [0, 1, 2, 3, 4]
```

### Indexing and Slicing

```python
fruits = ["apple", "banana", "cherry", "date"]

# Access by index (0-based)
first = fruits[0]      # "apple"
last = fruits[-1]      # "date" (negative indexing)

# Slicing [start:end:step]
subset = fruits[1:3]   # ["banana", "cherry"]
from_start = fruits[:2]   # ["apple", "banana"]
to_end = fruits[2:]       # ["cherry", "date"]
every_other = fruits[::2] # ["apple", "cherry"]
reversed_list = fruits[::-1]  # ["date", ...]
```

### Basic List Operations

```python
items = [1, 2, 3]

# Adding elements
items.append(4)           # [1, 2, 3, 4] - add to end
items.insert(0, 0)        # [0, 1, 2, 3, 4] - insert at index
items.extend([5, 6])      # [0, 1, 2, 3, 4, 5, 6] - add multiple

# Removing elements
items.remove(3)           # Removes first occurrence of 3
popped = items.pop()      # Removes and returns last item
popped = items.pop(0)     # Removes and returns item at index
items.clear()             # Removes all items

# Getting information
length = len(items)       # Number of items
index = items.index(2)    # Find position of value
count = items.count(2)    # Count occurrences
exists = 2 in items       # Membership test
```

### Modifying Lists

```python
nums = [1, 2, 3, 4, 5]

# Modifying elements
nums[0] = 10          # [10, 2, 3, 4, 5]
nums[1:3] = [20, 30]  # [10, 20, 30, 4, 5]

# Sorting (in-place vs new list)
nums.sort()           # Sorts in-place
nums.sort(reverse=True)  # Descending order
sorted_nums = sorted(nums)  # Returns new sorted list

# Reversing
nums.reverse()        # Reverses in-place
reversed_nums = list(reversed(nums))  # Returns iterator
```

## Common Patterns

### Iterating Over Lists

```python
items = ["a", "b", "c"]

# Basic iteration
for item in items:
    print(item)

# With index
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Accumulating values
total = 0
for num in numbers:
    total += num
```

### List Copying

```python
original = [1, 2, [3, 4]]

# Shallow copy (one level)
copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]

# Deep copy (nested structures)
import copy
deep = copy.deepcopy(original)
```

## Common Mistakes

```python
# Mistake 1: Modifying a list while iterating
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)  # Skips elements! Bug!

# Correct: Iterate over a copy
for n in numbers[:]:
    if n % 2 == 0:
        numbers.remove(n)

# Mistake 2: Using .sort() when you need the original list
original = [3, 1, 2]
original.sort()  # original is now [1, 2, 3] - modified!

# Correct: Use sorted() to keep original
sorted_list = sorted(original)  # original unchanged

# Mistake 3: Index out of range
items = [1, 2, 3]
print(items[3])  # IndexError! Valid indices are 0, 1, 2

# Correct: Check length first or use negative indexing
print(items[-1])  # Gets last element safely

# Mistake 4: Shallow copy with nested lists
original = [[1, 2], [3, 4]]
copy = original.copy()
copy[0].append(3)  # Modifies original[0] too!

# Correct: Use deepcopy for nested structures
import copy
deep = copy.deepcopy(original)
```

## Best Practices

1. **Use `append()` for single items, `extend()` for multiple items**
2. **Check membership with `in` before using `remove()` or `index()`**
3. **Use negative indices for accessing from the end**
4. **Remember that slicing creates new lists - consider memory for large datasets**
5. **Use `sorted()` when you need to keep the original list intact**

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01 | Creating and indexing lists |
| 02 | List methods (append, extend, insert) |
| 03 | List slicing |
| 04 | Finding and removing elements |
| 05 | Sorting and reversing |

## Connection to Weekly Project

Lists are essential for the Todo CLI project:
- Store all todos in a list
- Each todo is a dictionary stored in the list
- Append new todos, remove completed ones
- Iterate over the list to display todos

## Practice Problems

See the exercises in `exercises/day12/` directory. Each problem has a corresponding test in `tests/day12/` and solution in `solutions/day12/`.

## Key Takeaways

- Lists are **ordered** - items maintain their position
- Lists are **mutable** - you can modify them in-place
- Lists can contain **any type** of object, including other lists
- Indexing is **0-based** in Python
- Negative indices count from the **end** (-1 is last element)
