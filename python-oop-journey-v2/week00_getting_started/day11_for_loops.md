# Day 11: For Loops

## Learning Objectives

By the end of this day, you will be able to:

1. Write `for` loops to iterate over sequences
2. Use `range()` for numerical iteration
3. Iterate over lists, strings, and other iterables
4. Use `break` and `continue` in for loops
5. Apply `enumerate()` for index-value pairs
6. Use `zip()` for parallel iteration

---

## Key Concepts

### 1. Basic For Loop

Iterate over each item in a sequence:

```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over a string
for char in "Python":
    print(char)

# Iterate over a tuple
colors = ("red", "green", "blue")
for color in colors:
    print(color)
```

### 2. The range() Function

Generate numerical sequences efficiently:

```python
# range(stop) - starts from 0
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) - includes start, excludes stop
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Reverse range
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

**Key points:**
- `range()` is lazy (memory efficient)
- It generates numbers on-the-fly
- Stop value is always excluded

### 3. Iterating Lists

```python
numbers = [10, 20, 30, 40, 50]

# Direct iteration
for num in numbers:
    print(num)

# With range and index
for i in range(len(numbers)):
    print(f"Index {i}: {numbers[i]}")

# Using enumerate (preferred)
for i, num in enumerate(numbers):
    print(f"Index {i}: {num}")

# Start enumerate from 1
for i, num in enumerate(numbers, start=1):
    print(f"{i}. {num}")
```

### 4. enumerate() Function

Get both index and value:

```python
names = ["Alice", "Bob", "Charlie"]

# Without enumerate (not Pythonic)
for i in range(len(names)):
    print(f"{i}: {names[i]}")

# With enumerate (Pythonic)
for index, name in enumerate(names):
    print(f"{index}: {name}")

# Custom start index
for rank, name in enumerate(names, start=1):
    print(f"{rank}. {name}")
```

### 5. zip() Function

Iterate over multiple lists in parallel:

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["NYC", "LA", "Chicago"]

# Parallel iteration
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Three lists
for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age}, from {city}")

# zip stops at shortest list
short = [1, 2]
long = ["a", "b", "c", "d"]
for s, l in zip(short, long):
    print(s, l)  # Only (1, 'a') and (2, 'b')

# Create dict from two lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))  # {'a': 1, 'b': 2, 'c': 3}
```

### 6. Break and Continue

Control loop flow:

```python
# break - exit loop
for num in range(100):
    if num > 10:
        break
    print(num)

# continue - skip iteration
for num in range(10):
    if num % 2 == 0:
        continue
    print(num)  # Only odd numbers

# else clause (runs if no break)
for i in range(5):
    if i == 10:  # Never true
        break
else:
    print("Loop completed without break")
```

### 7. Nested For Loops

Loops inside loops:

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")
    print("---")

# Pattern printing
for i in range(1, 5):
    for j in range(i):
        print("*", end="")
    print()
# Output:
# *
# **
# ***
# ****
```

### 8. Common Iteration Patterns

```python
# Sum all elements
total = 0
for num in numbers:
    total += num

# Find maximum
maximum = numbers[0]
for num in numbers:
    if num > maximum:
        maximum = num

# Build new list
squares = []
for num in range(1, 6):
    squares.append(num ** 2)

# Filter list
evens = []
for num in numbers:
    if num % 2 == 0:
        evens.append(num)
```

---

## Common Mistakes

### 1. Modifying List While Iterating

```python
# Dangerous - skips elements!
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)  # Bug!

# Correct - iterate over a copy
for n in numbers[:]:  # Slice creates copy
    if n % 2 == 0:
        numbers.remove(n)

# Better - list comprehension
evens_removed = [n for n in numbers if n % 2 != 0]
```

### 2. Off-by-One with range()

```python
# Wrong - misses last index
for i in range(len(items) - 1):
    print(items[i])

# Correct
for i in range(len(items)):
    print(items[i])

# Best - iterate directly
for item in items:
    print(item)
```

### 3. Forgetting range() is Exclusive

```python
# Wrong - expects 1 through 5
for i in range(5):  # Actually 0, 1, 2, 3, 4
    print(i)

# Correct
for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(i)
```

### 4. Unpacking Errors with zip()

```python
# Wrong - mismatched variables
for a, b, c in zip([1, 2], ["a", "b"]):
    pass  # ValueError: not enough values to unpack

# Correct
for a, b in zip([1, 2], ["a", "b"]):
    pass
```

### 5. Using range(len()) Unnecessarily

```python
# Un-Pythonic
for i in range(len(my_list)):
    do_something(my_list[i])

# Pythonic - iterate directly
for item in my_list:
    do_something(item)

# When you need index, use enumerate
for i, item in enumerate(my_list):
    print(f"{i}: {item}")
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. sum_range | Using range() for summation |
| 02. print_pattern | Nested for loops |
| 03. find_in_list | Iterating with for, early exit with break |
| 04. filter_even | Building new lists with for loops |
| 05. enumerate_names | Using enumerate() effectively |

---

## Quick Reference

```python
# Basic for loop
for item in iterable:
    pass

# With range
for i in range(10):        # 0 to 9
for i in range(1, 11):     # 1 to 10
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
for i in range(10, 0, -1): # 10 to 1

# enumerate for index
for i, item in enumerate(items):
for i, item in enumerate(items, start=1):

# zip for parallel iteration
for a, b in zip(list_a, list_b):
for a, b, c in zip(a_list, b_list, c_list):

# Control flow
break      # Exit loop
continue   # Skip iteration
else       # Runs if no break

# Avoid
range(len(items))  # Use enumerate or iterate directly
```

---

## Next Steps

After completing today's exercises:
1. Practice converting while loops to for loops
2. Experiment with different range() parameters
3. Try combining zip() with enumerate()
4. Review all Week 0 material before moving to Week 1
