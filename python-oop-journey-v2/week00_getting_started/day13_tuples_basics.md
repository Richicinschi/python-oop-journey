# Day 13: Tuples Basics

## Learning Objectives

Today you'll learn about tuples - immutable sequences that are perfect for fixed collections of items and data that shouldn't change.

## Core Concepts

### Creating Tuples

```python
# Empty tuple
empty = ()
empty = tuple()

# Tuples with values (parentheses optional)
point = (3, 4)
point = 3, 4  # Same thing

# Single element tuple (note the comma!)
single = (5,)  # This is a tuple
not_tuple = (5)  # This is just an integer!

# Tuple from other iterables
chars = tuple("abc")  # ('a', 'b', 'c')
list_to_tuple = tuple([1, 2, 3])  # (1, 2, 3)
```

### Accessing Tuple Elements

```python
coordinates = (10, 20, 30)

# Indexing (same as lists)
x = coordinates[0]    # 10
y = coordinates[1]    # 20
z = coordinates[-1]   # 30 (last element)

# Slicing (returns a new tuple)
first_two = coordinates[:2]  # (10, 20)
```

### Tuple Immutability

```python
point = (1, 2)
point[0] = 5  # TypeError! Tuples cannot be modified

# But mutable objects inside tuples CAN be modified
nested = ([1, 2], [3, 4])
nested[0].append(3)  # Works! Now ([1, 2, 3], [3, 4])
```

### Tuple Unpacking

```python
# Basic unpacking
point = (3, 4)
x, y = point  # x=3, y=4

# Unpacking with *
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2, 3, 4]
first, *middle, last = (1, 2, 3, 4)  # first=1, middle=[2, 3], last=4

# Ignoring values with _
x, _, z = (1, 2, 3)  # x=1, z=3

# Swapping variables
a, b = 1, 2
a, b = b, a  # Now a=2, b=1
```

### Tuple Methods

```python
nums = (1, 2, 3, 2, 2, 4)

# Count occurrences
count = nums.count(2)  # 3

# Find index (first occurrence)
idx = nums.index(3)    # 2
idx = nums.index(2)    # 1 (first occurrence)
```

## Common Patterns

### Multiple Return Values

```python
def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([3, 1, 4, 1, 5])
```

### Enumerate with Tuples

```python
items = ["a", "b", "c"]
for index, value in enumerate(items):
    # index and value are unpacked from tuples
    print(f"{index}: {value}")
```

### Dictionary Items as Tuples

```python
data = {"x": 1, "y": 2}
for key, value in data.items():
    # Each item is a (key, value) tuple
    print(f"{key} = {value}")
```

## Tuples vs Lists

| Feature | Tuple | List |
|---------|-------|------|
| Mutable | No | Yes |
| Syntax | `()` or `1, 2` | `[]` |
| Performance | Faster | Slower |
| Use case | Fixed data | Changing data |
| Hashable | Yes (can be dict key) | No |

## Common Mistakes

```python
# Mistake 1: Forgetting the comma for single-element tuples
single = (5)      # This is an integer, not a tuple!
tuple_val = (5,)  # This is a tuple

# Mistake 2: Trying to modify a tuple
point = (3, 4)
point[0] = 5  # TypeError! Tuples are immutable

# Correct: Create a new tuple
point = (5, point[1])

# Mistake 3: Tuple unpacking with wrong number of elements
coords = (1, 2, 3)
x, y = coords  # ValueError: too many values to unpack

# Correct: Match the number of variables
x, y, z = coords
# Or use * to capture remaining
x, *rest = coords

# Mistake 4: Using tuples for mutable data that needs to change
# Tuples are for fixed data. If it changes, use a list.
```

## Best Practices

1. **Use tuples for heterogeneous data** (coordinates, records, RGB values)
2. **Use lists for homogeneous collections** that will grow/shrink
3. **Use tuples as dictionary keys** when you need compound keys
4. **Prefer tuple unpacking** over indexing for clarity
5. **Use `namedtuple` or dataclasses** for more descriptive tuple fields

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01 | Creating tuples, single-element syntax |
| 02 | Tuple indexing and slicing |
| 03 | Tuple unpacking |
| 04 | Returning multiple values from functions |
| 05 | Tuples as dictionary keys |

## Connection to Weekly Project

Tuples in the Todo CLI project:
- Use tuples for menu options that shouldn't change
- Return multiple values from helper functions
- Use tuple unpacking when iterating over dictionary items

## Practice Problems

See the exercises in `exercises/day13/` directory. Each problem has a corresponding test in `tests/day13/` and solution in `solutions/day13/`.

## Key Takeaways

- Tuples are **immutable** - once created, they cannot be changed
- Tuples are **faster** than lists and use less memory
- Tuples can be used as **dictionary keys** (lists cannot)
- Tuple **unpacking** is a powerful Python feature
- The **trailing comma** is essential for single-element tuples
