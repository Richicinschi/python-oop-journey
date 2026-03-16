# Control Flow Cheatsheet

Quick reference for if statements, loops, and control structures in Python.

---

## If Statements

### Basic If

```python
if condition:
    # Execute if condition is True
    do_something()
```

### If-Else

```python
if condition:
    # Execute if True
    do_something()
else:
    # Execute if False
    do_other_thing()
```

### If-Elif-Else

```python
if condition1:
    # First condition True
    do_a()
elif condition2:
    # Second condition True
    do_b()
elif condition3:
    # Third condition True
    do_c()
else:
    # None were True
    do_default()
```

### One-Line If (Ternary Operator)

```python
# Syntax: value_if_true if condition else value_if_false
status = "adult" if age >= 18 else "minor"

# Equivalent to:
if age >= 18:
    status = "adult"
else:
    status = "minor"
```

---

## Comparison Patterns

```python
# Basic comparisons
if x == 5:          # Equal to
if x != 5:          # Not equal to
if x > 5:           # Greater than
if x < 5:           # Less than
if x >= 5:          # Greater or equal
if x <= 5:          # Less or equal

# Multiple conditions
if a > 0 and b > 0:     # Both must be true
if a > 0 or b > 0:      # At least one true
if not x:               # x is falsy

# Membership tests
if x in [1, 2, 3]:      # x is in the list
if x not in [1, 2, 3]:  # x is not in the list
if 'a' in "apple":      # substring check

# Chained comparisons
if 0 < x < 10:          # Same as: 0 < x and x < 10
if 1 <= grade <= 100:   # Inclusive range check
```

---

## For Loops

### Basic For Loop

```python
# Iterate over a sequence
for item in sequence:
    # Do something with item
    print(item)
```

### Common For Loop Patterns

```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over a string
for char in "Hello":
    print(char)

# Iterate over a range
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8 (step by 2)
    print(i)

# Iterate with index
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Iterate over dictionary
person = {"name": "Alice", "age": 25}
for key in person:
    print(key)

for key, value in person.items():
    print(f"{key} = {value}")

# Iterate over multiple sequences
names = ["Alice", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

---

## While Loops

### Basic While Loop

```python
while condition:
    # Execute while condition is True
    do_something()
```

### Common While Loop Patterns

```python
# Count-controlled loop
count = 0
while count < 5:
    print(count)
    count += 1

# User input validation
password = ""
while password != "secret":
    password = input("Enter password: ")

# Infinite loop with break
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        break
    process_input(user_input)
```

---

## Loop Control Statements

| Statement | Description | Use Case |
|-----------|-------------|----------|
| `break` | Exit loop immediately | Stop when condition met |
| `continue` | Skip to next iteration | Skip certain items |
| `pass` | Do nothing (placeholder) | Empty loop body |
| `else` | Execute if loop didn't break | Check if loop completed |

```python
# break - exit loop early
for i in range(10):
    if i == 5:
        break       # Stops at 5, doesn't print it
    print(i)        # Prints 0, 1, 2, 3, 4

# continue - skip iteration
for i in range(10):
    if i % 2 == 0:
        continue    # Skip even numbers
    print(i)        # Prints 1, 3, 5, 7, 9

# pass - placeholder
for i in range(10):
    pass            # TODO: implement later

# else with loop - executes only if no break
for i in range(5):
    if i == 10:     # Condition never met
        break
else:
    print("Loop completed without break")  # This prints

# Searching example with else
items = [1, 2, 3, 4, 5]
for item in items:
    if item == 10:
        print("Found!")
        break
else:
    print("Not found")  # This prints (10 not in list)
```

---

## Nested Loops

```python
# Nested for loops
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")

# Common pattern: 2D grid
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:
    for item in row:
        print(item, end=" ")
    print()  # New line after each row

# Nested while loops
i = 0
while i < 3:
    j = 0
    while j < 3:
        print(f"({i}, {j})")
        j += 1
    i += 1
```

---

## List Comprehensions (Advanced)

```python
# Basic list comprehension
squares = [x**2 for x in range(5)]
# [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Nested comprehension
matrix = [[i*j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

---

## Common Loop Patterns

```python
# Pattern 1: Sum all items
total = 0
for num in numbers:
    total += num

# Pattern 2: Find maximum
maximum = numbers[0]
for num in numbers:
    if num > maximum:
        maximum = num

# Pattern 3: Count matches
count = 0
for num in numbers:
    if num > 0:
        count += 1

# Pattern 4: Collect matches
evens = []
for num in numbers:
    if num % 2 == 0:
        evens.append(num)

# Pattern 5: Build string
result = ""
for char in reversed(text):
    result += char

# Pattern 6: Flag search
found = False
for item in items:
    if item == target:
        found = True
        break
```

---

## Quick Reference Table

| Task | Syntax |
|------|--------|
| Simple condition | `if x > 0:` |
| Two-way decision | `if x > 0: ... else: ...` |
| Multiple conditions | `if ... elif ... else:` |
| Ternary | `result = a if condition else b` |
| Fixed iterations | `for i in range(n):` |
| Iterate list | `for item in list:` |
| Iterate with index | `for i, item in enumerate(list):` |
| Condition-based loop | `while condition:` |
| Exit loop | `break` |
| Skip iteration | `continue` |
| Placeholder | `pass` |
