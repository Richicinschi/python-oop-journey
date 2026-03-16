# Day 14: Dictionaries Basics

## Learning Objectives

Today you'll master Python dictionaries - key-value mappings that provide fast lookups and are essential for organizing data.

## Core Concepts

### Creating Dictionaries

```python
# Empty dictionary
empty = {}
empty = dict()

# Dictionary with initial values
person = {"name": "Alice", "age": 30, "city": "New York"}

# Creating from sequences of pairs
pairs = [("a", 1), ("b", 2)]
d = dict(pairs)  # {'a': 1, 'b': 2}

# Using dict() with keyword arguments (only for string keys)
d = dict(name="Bob", age=25)  # {'name': 'Bob', 'age': 25}
```

### Accessing and Modifying

```python
scores = {"Alice": 95, "Bob": 87, "Carol": 92}

# Access by key
alice_score = scores["Alice"]  # 95

# Using get() - safer, returns None or default if key missing
bob_score = scores.get("Bob")        # 87
dave_score = scores.get("Dave")      # None
dave_score = scores.get("Dave", 0)   # 0 (default)

# Add or update
scores["Dave"] = 88       # Add new key
scores["Alice"] = 98      # Update existing key

# Remove items
removed = scores.pop("Bob")   # Removes and returns value
del scores["Carol"]           # Removes key-value pair
scores.clear()                # Removes all items
```

### Dictionary Methods

```python
info = {"x": 1, "y": 2, "z": 3}

# Keys, values, items
keys = info.keys()      # dict_keys(['x', 'y', 'z'])
values = info.values()  # dict_values([1, 2, 3])
items = info.items()    # dict_items([('x', 1), ('y', 2), ('z', 3)])

# Membership testing (checks keys only)
has_x = "x" in info     # True
has_w = "w" in info     # False

# Update one dictionary with another
extra = {"w": 4, "x": 10}
info.update(extra)  # {'x': 10, 'y': 2, 'z': 3, 'w': 4}
```

### Safe Dictionary Operations

```python
data = {"a": 1}

# setdefault - get value, or set and return default if missing
value = data.setdefault("a", 0)  # Returns 1, doesn't change
default = data.setdefault("b", 0)  # Sets b=0, returns 0

# Checking before access
if "key" in data:
    value = data["key"]
else:
    value = "default"
```

## Common Patterns

### Building a Dictionary

```python
# Counting occurrences
counts = {}
for item in ["a", "b", "a", "c", "a", "b"]:
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1
# {'a': 3, 'b': 2, 'c': 1}

# Or using get()
counts = {}
for item in ["a", "b", "a", "c", "a", "b"]:
    counts[item] = counts.get(item, 0) + 1
```

### Iterating Over Dictionaries

```python
data = {"a": 1, "b": 2, "c": 3}

# Iterate over keys (default)
for key in data:
    print(key)

# Iterate over keys and values
for key, value in data.items():
    print(f"{key}: {value}")

# Iterate over values only
for value in data.values():
    print(value)
```

### Dictionary Keys

Dictionary keys must be **hashable** (immutable):
- ✅ Strings: `"name"`
- ✅ Numbers: `42`, `3.14`
- ✅ Tuples: `(1, 2)`
- ❌ Lists: `[1, 2]` - not allowed!
- ❌ Dictionaries - not allowed!

## Common Mistakes

```python
# Mistake 1: Accessing a key that doesn't exist
data = {"a": 1}
value = data["b"]  # KeyError!

# Correct: Use get() with default
value = data.get("b", 0)

# Or check first
if "b" in data:
    value = data["b"]

# Mistake 2: Modifying a dict while iterating
for key in data:
    if key == "a":
        del data[key]  # RuntimeError!

# Correct: Create a list of keys first
for key in list(data.keys()):
    if key == "a":
        del data[key]

# Mistake 3: Using a mutable object as a key
bad_key = [1, 2]
data[bad_key] = "value"  # TypeError! Lists are unhashable

# Correct: Use a tuple instead
good_key = (1, 2)
data[good_key] = "value"

# Mistake 4: Thinking .keys() and .values() return lists
keys = data.keys()  # Returns a view, not a list
# Use list() if you need a list: list(data.keys())
```

## Best Practices

1. **Use `get()` instead of `[]` when key might not exist**
2. **Check membership with `in` before accessing uncertain keys**
3. **Use `items()` for iterating over both keys and values**
4. **Use `dict()` constructor for creating from key=value pairs with string keys**
5. **Remember: dictionary iteration order is insertion order (Python 3.7+)**

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01 | Creating dictionaries, accessing values |
| 02 | Using get() with defaults |
| 03 | Adding and updating key-value pairs |
| 04 | Iterating over dictionaries |
| 05 | Dictionary methods (keys, values, items) |

## Connection to Weekly Project

Dictionaries are the core data structure for the Todo CLI project:
- Each todo is a dictionary with keys: id, title, completed, created_at
- The todo list is a list of these dictionaries
- Dictionaries allow fast lookup of todos by ID

## Common Use Cases

```python
# Configuration settings
config = {"debug": True, "timeout": 30, "retries": 3}

# Lookup tables
month_names = {
    1: "January", 2: "February", 3: "March",
    # ... etc
}

# Caching results (memoization)
cache = {}

def expensive_function(n):
    if n not in cache:
        cache[n] = n * n * n  # Expensive computation
    return cache[n]
```

## Practice Problems

See the exercises in `exercises/day14/` directory. Each problem has a corresponding test in `tests/day14/` and solution in `solutions/day14/`.

## Key Takeaways

- Dictionaries store **key-value pairs** for O(1) average lookup time
- Keys must be **hashable** (immutable types)
- Use **`get()`** for safe access with potential missing keys
- **`items()`**, **`keys()`**, and **`values()`** provide dictionary views
- Dictionaries are **mutable** - you can add, remove, and change entries
