# Data Types Cheatsheet

Complete reference for Python's built-in data structures: lists, tuples, dictionaries, and sets.

---

## Quick Comparison

| Feature | List | Tuple | Dict | Set |
|---------|------|-------|------|-----|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` | `{"a": 1}` | `{1, 2, 3}` |
| Ordered | ✅ Yes | ✅ Yes | ✅ Yes (Py 3.7+) | ❌ No |
| Mutable | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Duplicates | ✅ Allowed | ✅ Allowed | ❌ Keys unique | ❌ Not allowed |
| Indexed by | Integer | Integer | Key | Not indexed |
| Use for | Sequences | Fixed data | Mappings | Unique items |

---

## Lists

Ordered, mutable collection of items.

### Creating Lists

```python
# Empty list
my_list = []
my_list = list()

# With values
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4]]

# From other types
chars = list("abc")           # ['a', 'b', 'c']
nums = list(range(5))         # [0, 1, 2, 3, 4]
```

### Accessing Elements

```python
fruits = ["apple", "banana", "cherry", "date"]

# Indexing (0-based)
fruits[0]     # "apple" (first)
fruits[-1]    # "date" (last)
fruits[1]     # "banana"

# Slicing [start:stop:step]
fruits[1:3]   # ["banana", "cherry"]
fruits[:2]    # ["apple", "banana"]
fruits[2:]    # ["cherry", "date"]
fruits[::2]   # ["apple", "cherry"] (every 2nd)
fruits[::-1]  # ["date", "cherry", "banana", "apple"] (reverse)
```

### Modifying Lists

```python
# Add items
my_list.append(item)          # Add to end
my_list.insert(index, item)   # Insert at position
my_list.extend(other_list)    # Add multiple items
my_list += other_list         # Same as extend

# Remove items
my_list.remove(item)          # Remove first occurrence
my_list.pop()                 # Remove and return last
my_list.pop(index)            # Remove and return at index
del my_list[index]            # Delete at index
my_list.clear()               # Remove all items

# Modify
my_list[index] = new_value
my_list[start:end] = [a, b, c]
```

### List Methods

| Method | Description | Example |
|--------|-------------|---------|
| `append(x)` | Add x to end | `lst.append(4)` |
| `extend(iter)` | Add all from iter | `lst.extend([5,6])` |
| `insert(i, x)` | Insert x at i | `lst.insert(0, "a")` |
| `remove(x)` | Remove first x | `lst.remove(3)` |
| `pop([i])` | Remove & return at i | `lst.pop()` |
| `clear()` | Remove all | `lst.clear()` |
| `index(x)` | Find position of x | `lst.index("a")` |
| `count(x)` | Count occurrences | `lst.count(2)` |
| `sort()` | Sort in place | `lst.sort()` |
| `reverse()` | Reverse in place | `lst.reverse()` |
| `copy()` | Shallow copy | `lst.copy()` |

```python
# Sorting
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()                # [1, 1, 3, 4, 5, 9]
numbers.sort(reverse=True)    # [9, 5, 4, 3, 1, 1]
numbers.sort(key=len)         # Sort by length (for strings)

sorted(numbers)               # Returns new sorted list
```

---

## Tuples

Immutable, ordered collection.

### Creating Tuples

```python
# Empty tuple
empty = ()
empty = tuple()

# With values (parentheses optional)
point = (3, 4)
coords = 1, 2, 3              # Parentheses optional
single = (5,)                 # Note the comma!
not_tuple = (5)               # This is just an int

# From other types
t = tuple([1, 2, 3])          # (1, 2, 3)
```

### Tuple Operations

```python
t = (1, 2, 3, 4, 5)

# Access (same as list)
t[0]          # 1
t[-1]         # 5
t[1:3]        # (2, 3)

# Can't modify!
t[0] = 10     # TypeError!

# But can create new tuples
new_t = t + (6, 7)            # (1, 2, 3, 4, 5, 6, 7)
repeated = t * 2              # (1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

# Unpacking
x, y, z = (1, 2, 3)
first, *rest = (1, 2, 3, 4)   # first=1, rest=[2, 3, 4]
a, b = b, a                   # Swap values
```

### Tuple Methods

| Method | Description | Example |
|--------|-------------|---------|
| `count(x)` | Count x | `t.count(2)` |
| `index(x)` | Find x | `t.index(3)` |

---

## Dictionaries

Key-value mappings (hash maps).

### Creating Dictionaries

```python
# Empty dict
empty = {}
empty = dict()

# With values
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# From sequences
d = dict([("a", 1), ("b", 2)])    # {"a": 1, "b": 2}
d = dict(name="Bob", age=30)       # {"name": "Bob", "age": 30}

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Accessing and Modifying

```python
person = {"name": "Alice", "age": 25}

# Access
person["name"]                # "Alice"
person.get("name")            # "Alice"
person.get("phone", "N/A")    # "N/A" (default if missing)

# Add/Update
person["phone"] = "555-1234"  # Add new key
person["age"] = 26            # Update existing

# Remove
del person["age"]             # Delete key
phone = person.pop("phone")   # Remove and return
item = person.popitem()       # Remove and return (key, value) pair
person.clear()                # Remove all

# Check existence
"name" in person              # True
"phone" in person             # False
```

### Dictionary Methods

| Method | Description | Example |
|--------|-------------|---------|
| `keys()` | All keys | `person.keys()` |
| `values()` | All values | `person.values()` |
| `items()` | All (key, value) pairs | `person.items()` |
| `get(k, d)` | Get with default | `person.get("x", 0)` |
| `pop(k)` | Remove & return | `person.pop("name")` |
| `popitem()` | Remove arbitrary item | `person.popitem()` |
| `update(d)` | Merge dictionaries | `d1.update(d2)` |
| `setdefault(k,v)` | Set if missing | `d.setdefault("x", 0)` |

```python
# Iterating
for key in person:
    print(key)

for key in person.keys():
    print(key)

for value in person.values():
    print(value)

for key, value in person.items():
    print(f"{key}: {value}")
```

---

## Sets

Unordered collection of unique items.

### Creating Sets

```python
# Empty set (note: {} creates dict!)
empty = set()

# With values
numbers = {1, 2, 3, 4, 5}
mixed = {1, "hello", 3.14}    # Mixed types allowed

# From other types
s = set([1, 2, 2, 3])         # {1, 2, 3} (duplicates removed)
s = set("hello")              # {'h', 'e', 'l', 'o'}
```

### Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Mathematical operations
a | b         # {1, 2, 3, 4, 5, 6} (union)
a & b         # {3, 4} (intersection)
a - b         # {1, 2} (difference)
a ^ b         # {1, 2, 5, 6} (symmetric difference)

# Methods
a.union(b)
a.intersection(b)
a.difference(b)
a.symmetric_difference(b)
```

### Modifying Sets

```python
s = {1, 2, 3}

# Add items
s.add(4)              # Add single item
s.update([5, 6])      # Add multiple
s |= {7, 8}           # Union update

# Remove items
s.remove(3)           # Remove (error if missing)
s.discard(3)          # Remove (no error)
s.pop()               # Remove & return arbitrary
s.clear()             # Remove all
```

### Set Methods

| Method | Description | Example |
|--------|-------------|---------|
| `add(x)` | Add element | `s.add(5)` |
| `remove(x)` | Remove (error if absent) | `s.remove(3)` |
| `discard(x)` | Remove (no error) | `s.discard(3)` |
| `pop()` | Remove arbitrary | `s.pop()` |
| `clear()` | Remove all | `s.clear()` |
| `union(s)` | a \| b | `a.union(b)` |
| `intersection(s)` | a & b | `a.intersection(b)` |
| `difference(s)` | a - b | `a.difference(b)` |

### Set Relationships

```python
a = {1, 2, 3}
b = {1, 2}

b.issubset(a)         # True (b ⊆ a)
a.issuperset(b)       # True (a ⊇ b)
a.isdisjoint({4, 5})  # True (no common elements)
```

---

## When to Use Each

| Use Case | Best Type | Why |
|----------|-----------|-----|
| Shopping list | List | Order matters, may have duplicates |
| Coordinates | Tuple | Fixed, unchangeable values |
| Phone book | Dict | Fast lookup by name |
| Unique tags | Set | Automatically removes duplicates |
| Matrix/grid | List of lists | 2D structure |
| Configuration | Dict | Named settings |
| Record/row | Tuple or Dict | Fixed fields with values |

---

## Type Conversions

```python
# To list
list("abc")           # ['a', 'b', 'c']
list((1, 2, 3))       # [1, 2, 3]
list({1, 2})          # [1, 2]
list({"a": 1})        # ['a']

# To tuple
tuple([1, 2, 3])      # (1, 2, 3)

# To set
set([1, 2, 2, 3])     # {1, 2, 3}

# To dict (from sequence of pairs)
dict([("a", 1)])      # {"a": 1}
```
