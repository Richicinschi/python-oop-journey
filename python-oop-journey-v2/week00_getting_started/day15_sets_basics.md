# Day 15: Sets Basics

## Learning Objectives

Today you'll learn about sets - unordered collections of unique elements that are perfect for membership testing and eliminating duplicates.

## Core Concepts

### Creating Sets

```python
# Empty set (must use set(), not {} which creates a dict)
empty = set()

# Set with values
numbers = {1, 2, 3, 4, 5}

# From other iterables (removes duplicates!)
unique_chars = set("hello")  # {'h', 'e', 'l', 'o'}
unique_numbers = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}

# Set comprehension (advanced, but good to know)
evens = {x for x in range(10) if x % 2 == 0}  # {0, 2, 4, 6, 8}
```

### Set Operations - Modification

```python
fruits = {"apple", "banana"}

# Adding elements
fruits.add("cherry")        # Add single element
fruits.update(["date", "elderberry"])  # Add multiple elements

# Removing elements
fruits.remove("banana")     # Raises KeyError if not found
fruits.discard("banana")    # Safe removal, no error if not found
removed = fruits.pop()      # Removes and returns arbitrary element
fruits.clear()              # Removes all elements
```

### Set Operations - Mathematical

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union - all elements from both sets
union = a | b           # {1, 2, 3, 4, 5, 6}
union = a.union(b)

# Intersection - elements common to both
intersection = a & b    # {3, 4}
intersection = a.intersection(b)

# Difference - elements in a but not in b
diff = a - b            # {1, 2}
diff = a.difference(b)

# Symmetric difference - elements in either set, but not both
sym_diff = a ^ b        # {1, 2, 5, 6}
sym_diff = a.symmetric_difference(b)
```

### Set Comparisons

```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

# Subset
a.issubset(b)       # True - all elements of a are in b
a <= b              # Same thing

# Proper subset (strict)
a < b               # True - subset but not equal

# Superset
b.issuperset(a)     # True - b contains all elements of a
b >= a              # Same thing

# Disjoint (no common elements)
a.isdisjoint({4, 5})  # True
```

### Membership Testing

```python
numbers = {1, 2, 3, 4, 5}

# Fast O(1) membership testing
exists = 3 in numbers      # True
missing = 10 in numbers    # False
not_exists = 10 not in numbers  # True
```

## Common Patterns

### Removing Duplicates

```python
items = ["a", "b", "a", "c", "b", "a"]
unique_items = list(set(items))  # ['a', 'b', 'c'] (order not guaranteed)

# Preserving order (Python 3.7+)
unique_items = list(dict.fromkeys(items))  # ['a', 'b', 'c']
```

### Finding Common Elements

```python
def have_common_friends(friends_a, friends_b):
    """Check if two people have any friends in common."""
    return bool(set(friends_a) & set(friends_b))

# Or check if lists have any overlap
def lists_overlap(list1, list2):
    return not set(list1).isdisjoint(list2)
```

### Finding Unique Elements

```python
def unique_to_first(list1, list2):
    """Find elements only in list1, not in list2."""
    return list(set(list1) - set(list2))
```

## Sets vs Lists vs Tuples

| Feature | Set | List | Tuple |
|---------|-----|------|-------|
| Ordered | No | Yes | Yes |
| Mutable | Yes | Yes | No |
| Unique | Yes | No | No |
| Hashable | No | No | Yes |
| Lookup speed | O(1) | O(n) | O(n) |

## Common Mistakes

```python
# Mistake 1: Using {} for an empty set (creates a dict!)
empty = {}  # This is a dictionary, not a set!
empty_set = set()  # Correct way to create an empty set

# Mistake 2: Trying to add mutable objects to a set
my_set = {1, 2, 3}
my_set.add([4, 5])  # TypeError! Lists are unhashable

# Correct: Only immutable objects
my_set.add(4)
my_set.add((4, 5))  # Tuples are OK

# Mistake 3: Assuming sets preserve order
unique = set([3, 1, 4, 1, 5])  # Order not guaranteed!

# Correct: Use dict.fromkeys() for ordered uniqueness (Python 3.7+)
ordered = list(dict.fromkeys([3, 1, 4, 1, 5]))  # [3, 1, 4, 5]

# Mistake 4: Modifying a set while iterating
for item in my_set:
    if item > 2:
        my_set.remove(item)  # RuntimeError!

# Correct: Iterate over a copy or build a new set
to_remove = {item for item in my_set if item > 2}
my_set -= to_remove
```

## Best Practices

1. **Use sets for membership testing** - much faster than lists for large collections
2. **Use sets to eliminate duplicates** - but remember order is not preserved
3. **Use `discard()` instead of `remove()`** when you don't care if element exists
4. **Convert to set for fast lookup** when checking membership multiple times
5. **Remember: sets only contain hashable (immutable) elements** - no lists or dicts

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01 | Creating sets, removing duplicates |
| 02 | Set operations (union, intersection, difference) |
| 03 | Membership testing |
| 04 | Set methods (add, remove, discard) |
| 05 | Subset and superset checks |

## Connection to Weekly Project

Sets can be useful in the Todo CLI project:
- Track unique categories/tags for todos
- Quickly check if a todo ID exists
- Find common tags between todos

## Common Use Cases

```python
# Tag system
def has_common_tags(tags1, tags2):
    return bool(set(tags1) & set(tags2))

# Filtering seen items
def remove_seen(items, seen):
    """Return items that haven't been seen."""
    return [item for item in items if item not in seen]

# Validating unique usernames
def validate_usernames(usernames):
    if len(usernames) != len(set(usernames)):
        raise ValueError("Duplicate usernames found")
```

## Practice Problems

See the exercises in `exercises/day15/` directory. Each problem has a corresponding test in `tests/day15/` and solution in `solutions/day15/`.

## Key Takeaways

- Sets store **unique elements only** - duplicates are automatically removed
- Sets are **unordered** - no indexing or slicing
- Sets have **O(1)** membership testing - very fast lookups
- Sets support powerful **mathematical operations** (union, intersection, difference)
- Sets are **mutable** but can only contain **hashable** (immutable) elements
