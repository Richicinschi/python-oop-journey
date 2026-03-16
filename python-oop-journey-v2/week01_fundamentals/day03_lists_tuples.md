# Day 3: Lists and Tuples

## Learning Objectives

By the end of this day, you will be able to:

1. Create and manipulate Python lists effectively
2. Use list indexing and slicing to access and modify data
3. Apply common list methods for sorting, searching, and transformation
4. Write concise list comprehensions for data processing
5. Understand tuples as immutable sequences and when to use them
6. Solve algorithmic problems involving arrays and sequences
7. Analyze time and space complexity of list operations

---

## Key Concepts

### 1. List Basics

Lists are ordered, mutable sequences that can contain items of any type.

```python
# Creating lists
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4], [5, 6]]

# Basic operations
length = len(numbers)           # 5
combined = [1, 2] + [3, 4]      # [1, 2, 3, 4]
repeated = [1, 2] * 3           # [1, 2, 1, 2, 1, 2]

# Membership testing
exists = 3 in numbers           # True
missing = 10 not in numbers     # True
```

### 2. Indexing and Slicing

Access elements by position using zero-based indexing.

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Indexing
first = fruits[0]       # "apple"
last = fruits[-1]       # "elderberry"
second_last = fruits[-2]  # "date"

# Slicing [start:stop:step]
subset = fruits[1:4]    # ["banana", "cherry", "date"]
from_start = fruits[:3] # ["apple", "banana", "cherry"]
to_end = fruits[2:]     # ["cherry", "date", "elderberry"]
every_other = fruits[::2]  # ["apple", "cherry", "elderberry"]
reversed_list = fruits[::-1]  # reversed copy

# Modifying with slices
numbers = [1, 2, 3, 4, 5]
numbers[1:3] = [20, 30]  # [1, 20, 30, 4, 5]
numbers[1:1] = [15]      # Insert at position 1: [1, 15, 20, 30, 4, 5]
```

### 3. List Methods

Common methods for list manipulation:

```python
# Adding elements
items = [1, 2]
items.append(3)              # [1, 2, 3] - add to end
items.insert(0, 0)           # [0, 1, 2, 3] - insert at index
items.extend([4, 5])         # [0, 1, 2, 3, 4, 5] - add multiple

# Removing elements
items.pop()                  # Returns and removes last: 5, list is [0, 1, 2, 3, 4]
items.pop(0)                 # Returns and removes at index: 0, list is [1, 2, 3, 4]
items.remove(3)              # Removes first occurrence of value: [1, 2, 4]

# Searching and counting
nums = [1, 2, 3, 2, 4, 2]
index = nums.index(2)        # 1 - first occurrence
nums.index(2, 2)             # 3 - start search from index 2
count = nums.count(2)        # 3

# Sorting and reversing
nums = [3, 1, 4, 1, 5, 9, 2]
nums.sort()                  # Sorts in-place: [1, 1, 2, 3, 4, 5, 9]
nums.sort(reverse=True)      # Descending: [9, 5, 4, 3, 2, 1, 1]
sorted_nums = sorted(nums)   # Returns new sorted list, original unchanged
nums.reverse()               # Reverse in-place
reversed_nums = list(reversed(nums))  # Returns iterator, convert to list

# Copying
original = [1, 2, [3, 4]]
shallow = original.copy()    # or list(original) or original[:]
import copy
deep = copy.deepcopy(original)  # For nested structures
```

### 4. List Comprehensions

Concise syntax for creating lists:

```python
# Basic syntax: [expression for item in iterable]
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition: [expression for item in iterable if condition]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# Multiple loops
pairs = [(x, y) for x in [1, 2] for y in [3, 4]]
# [(1, 3), (1, 4), (2, 3), (2, 4)]

# Nested comprehensions
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Flattening
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for sublist in nested for x in sublist]
# [1, 2, 3, 4, 5, 6]
```

### 5. Tuples

Tuples are immutable ordered sequences - once created, they cannot be modified.

```python
# Creating tuples
empty = ()
single = (1,)           # Note the comma! (1) is just 1
multiple = (1, 2, 3)
no_parens = 1, 2, 3     # Parentheses are optional
from_list = tuple([1, 2, 3])

# Tuple unpacking
coordinates = (3, 4)
x, y = coordinates      # x=3, y=4

# Extended unpacking
first, *rest = (1, 2, 3, 4, 5)  # first=1, rest=[2, 3, 4, 5]
*beginning, last = (1, 2, 3, 4) # beginning=[1, 2, 3], last=4

# Tuple methods (limited - immutable!)
t = (1, 2, 3, 2, 4, 2)
count = t.count(2)      # 3
index = t.index(3)      # 2

# When to use tuples
# - Fixed data that shouldn't change (coordinates, RGB values)
# - Dictionary keys (lists can't be keys)
# - Function return values (multiple values)
# - Performance: tuples are slightly faster and use less memory
```

### 6. Immutability

Understanding mutability is crucial for writing bug-free code:

```python
# Lists are mutable
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4] - a changed too!

# Tuples are immutable
t1 = (1, 2, 3)
t2 = t1
t2 = t2 + (4,)  # Creates new tuple
print(t1)  # (1, 2, 3) - t1 unchanged

# But mutable objects inside tuples can still change
nested = ([1, 2], [3, 4])
nested[0].append(3)
print(nested)  # ([1, 2, 3], [3, 4])
```

---

## Common Mistakes

1. **Modifying a list while iterating over it:**
   ```python
   # WRONG: Skips elements
   for item in items:
       if condition(item):
           items.remove(item)
   
   # RIGHT: Iterate over a copy
   for item in items[:]:
       if condition(item):
           items.remove(item)
   # Or use list comprehension
   items = [item for item in items if not condition(item)]
   ```

2. **Confusing `sort()` with `sorted()`:**
   ```python
   # sort() modifies in-place, returns None
   result = nums.sort()  # result is None!
   
   # sorted() returns a new list
   result = sorted(nums)  # result is the sorted list
   ```

3. **Creating multiple references to the same list:**
   ```python
   # WRONG: All rows are the same list
   matrix = [[0] * 3] * 3
   matrix[0][0] = 1  # All rows now start with 1
   
   # RIGHT: Each row is a separate list
   matrix = [[0] * 3 for _ in range(3)]
   ```

4. **Using lists as default arguments:**
   ```python
   # WRONG: Shared list across calls
   def add_item(item, items=[]):
       items.append(item)
       return items
   
   # RIGHT: Create new list each time
   def add_item(item, items=None):
       if items is None:
           items = []
       items.append(item)
       return items
   ```

5. **Tuple with single element:**
   ```python
   # WRONG: This is just the integer 1
   t = (1)
   
   # RIGHT: Trailing comma makes it a tuple
   t = (1,)
   ```

---

## Connection to Exercises

The exercises for Day 3 focus on algorithmic problem-solving using lists and tuples:

| Problem | Key Concepts |
|---------|-------------|
| 01. Two Sum | List traversal, dictionary for O(n) lookup |
| 02. Remove Duplicates | In-place modification, two-pointer technique |
| 03. Rotate Array | List slicing, reversal algorithm |
| 04. Contains Duplicate | Set for O(1) lookup, early termination |
| 05. Maximum Subarray | Kadane's algorithm, dynamic programming |
| 06. Merge Sorted Arrays | Two-pointer technique, sorted merging |
| 07. Product Except Self | Prefix/suffix products, O(n) without division |
| 08. Find Minimum in Rotated Array | Binary search on rotated sorted array |
| 09. Three Sum | Sorting, two-pointer, avoiding duplicates |
| 10. Container With Most Water | Two-pointer from both ends |
| 11. Best Time to Buy/Sell Stock | Tracking min and max profit |

---

## Time Complexity Reference

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Access by index | O(1) | `list[i]` |
| Append | O(1) amortized | May need to resize |
| Pop from end | O(1) | `list.pop()` |
| Pop from index | O(n) | Must shift elements |
| Insert | O(n) | Must shift elements |
| Search (in) | O(n) | Linear scan |
| Sort | O(n log n) | Timsort algorithm |
| List comprehension | O(n) | For single loop |

---

## Further Reading

- [Python Lists Documentation](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
