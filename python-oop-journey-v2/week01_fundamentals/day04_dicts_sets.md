# Day 4: Dictionaries and Sets

## Learning Objectives

By the end of this day, you will be able to:

- Create and manipulate dictionaries for key-value data storage
- Use dictionary methods effectively (`get()`, `keys()`, `values()`, `items()`, `update()`, etc.)
- Leverage sets for unique element storage and mathematical operations
- Apply hash-based data structures to solve algorithmic problems efficiently
- Choose between dictionaries and sets based on use case requirements
- Recognize O(1) average time complexity for hash-based operations

---

## Key Concepts

### Dictionary Basics

A dictionary is a mutable, unordered collection of key-value pairs with O(1) average lookup time.

```python
# Creating dictionaries
empty_dict = {}
empty_dict = dict()

person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])      # "Alice"
print(person.get("age"))   # 30
print(person.get("salary", 0))  # 0 (default value)

# Adding and updating
person["email"] = "alice@example.com"
person.update({"age": 31, "country": "USA"})
```

### Dictionary Methods

```python
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}

# Getting views
scores.keys()      # dict_keys(['Alice', 'Bob', 'Charlie'])
scores.values()    # dict_values([95, 87, 92])
scores.items()     # dict_items([('Alice', 95), ...])

# Safe operations
scores.get("David", 0)  # Returns 0 instead of KeyError

# Removal
removed = scores.pop("Bob")        # Returns 87
last_item = scores.popitem()       # Removes and returns arbitrary item

# Membership testing
"Alice" in scores      # True (checks keys)
95 in scores.values()  # True

# Building from iterables
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}
```

### Using Dictionaries as Hash Maps

Dictionaries excel at counting, grouping, and lookup operations:

```python
# Frequency counting
from collections import Counter

def count_elements(items: list[str]) -> dict[str, int]:
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq

# Or simply:
def count_elements_simple(items: list[str]) -> dict[str, int]:
    return dict(Counter(items))

# Two-sum pattern using hash map
def has_pair_sum(nums: list[int], target: int) -> bool:
    seen = {}
    for num in nums:
        complement = target - num
        if complement in seen:
            return True
        seen[num] = True
    return False
```

### Set Basics

A set is an unordered collection of unique elements with O(1) membership testing.

```python
# Creating sets
empty_set = set()  # Not {} (that's an empty dict)
fruits = {"apple", "banana", "cherry"}
numbers = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}

# Set properties (elements must be hashable)
unique_chars = set("hello")  # {'h', 'e', 'l', 'o'}
```

### Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Mathematical operations
a | b           # Union: {1, 2, 3, 4, 5, 6}
a & b           # Intersection: {3, 4}
a - b           # Difference: {1, 2}
a ^ b           # Symmetric difference: {1, 2, 5, 6}

# Method equivalents
a.union(b)
a.intersection(b)
a.difference(b)
a.symmetric_difference(b)

# In-place operations
a.update(b)           # a |= b
a.intersection_update(b)  # a &= b

# Membership testing
2 in a         # True (O(1) average)
5 not in a     # True
```

### Set Comprehensions

```python
# Similar to list comprehensions
squares = {x**2 for x in range(10)}
# {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}

even_squares = {x**2 for x in range(10) if x % 2 == 0}
# {0, 4, 16, 36, 64}
```

### Dictionary Comprehensions

```python
# Transforming data
words = ["apple", "banana", "cherry"]
lengths = {word: len(word) for word in words}
# {'apple': 5, 'banana': 6, 'cherry': 6}

# Filtering
scores = {"Alice": 95, "Bob": 82, "Charlie": 78}
passing = {name: score for name, score in scores.items() if score >= 80}
```

---

## Common Mistakes

### 1. Using Mutable Keys

```python
# WRONG: Lists are unhashable
bad_dict = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'

# CORRECT: Use tuples instead
good_dict = {(1, 2): "value"}  # Works fine
```

### 2. Assuming Dictionary Order (Python < 3.7)

```python
# In Python 3.7+, dictionaries maintain insertion order
# But don't rely on order for algorithm logic
# Use collections.OrderedDict if order is critical for older Python
```

### 3. Modifying Dictionary During Iteration

```python
# WRONG: RuntimeError or unexpected behavior
for key in my_dict:
    if condition(key):
        del my_dict[key]

# CORRECT: Create list of keys to remove
keys_to_remove = [k for k in my_dict if condition(k)]
for k in keys_to_remove:
    del my_dict[k]

# Or use dictionary comprehension
my_dict = {k: v for k, v in my_dict if not condition(k)}
```

### 4. Forgetting `get()` Default

```python
counts = {}

# WRONG: KeyError on first occurrence
for item in items:
    counts[item] += 1

# CORRECT: Provide default value
for item in items:
    counts[item] = counts.get(item, 0) + 1

# Or use collections.defaultdict
from collections import defaultdict
counts = defaultdict(int)
for item in items:
    counts[item] += 1
```

### 5. Using `[]` Instead of `set()`

```python
# WRONG: Creates empty dictionary, not set
empty = {}  # This is a dict!

# CORRECT: Use set() constructor
empty = set()
```

### 6. Expecting Set Indexing

```python
my_set = {1, 2, 3}

# WRONG: Sets are unordered
first = my_set[0]  # TypeError: 'set' object is not subscriptable

# CORRECT: Convert to list or iterate
first = next(iter(my_set))  # Gets arbitrary element
```

---

## Connection to Exercises

| Exercise | Concept Practice |
|----------|-----------------|
| 01. Find All Pairs | Hash map for complement lookup |
| 02. Group Anagrams Optimal | Dictionary for grouping by key |
| 03. Top K Frequent | Frequency counting + sorting |
| 04. Longest Consecutive Sequence | Set for O(1) existence checks |
| 05. Intersection of Two Arrays | Set intersection operations |
| 06. Subarray Sum Equals K | Prefix sum with hash map |
| 07. First Missing Positive | Hash set for existence tracking |
| 08. Isomorphic Strings | Bidirectional character mapping |
| 09. Word Pattern | Pattern-to-word dictionary mapping |
| 10. Valid Sudoku | Sets for row/column/box validation |

---

## Weekly Project Connection

The Week 1 project (Command-line Quiz Game) uses dictionaries extensively:

- **Question storage**: Dictionary mapping question IDs to question data
- **Score tracking**: Dictionary mapping player names to scores
- **Category organization**: Nested dictionaries for question categories
- **Answer validation**: Set for valid option letters (A, B, C, D)

Mastering dictionaries today will make implementing the quiz game's data layer straightforward.

---

## Summary

- **Dictionaries** provide O(1) key-based lookup and are ideal for mappings, counts, and grouping
- **Sets** provide O(1) membership testing and are ideal for uniqueness and set operations
- Both use hashing internally, requiring hashable (immutable) elements
- Choose dictionaries when you need key-value associations; choose sets when you only need existence
