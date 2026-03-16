# Day 5: Control Flow

## Learning Objectives

By the end of this day, you will be able to:

1. Use conditional statements (`if`, `elif`, `else`) to control program flow
2. Write `for` loops to iterate over sequences and ranges
3. Write `while` loops for conditional iteration
4. Use `break`, `continue`, and `pass` statements effectively
5. Apply `range()`, `enumerate()`, and `zip()` for common iteration patterns
6. Combine control flow constructs to solve algorithmic problems
7. Understand loop complexity and efficiency considerations

---

## Key Concepts

### 1. Conditional Statements: `if`, `elif`, `else`

Conditional statements allow your program to make decisions based on conditions.

```python
# Basic if statement
age = 18
if age >= 18:
    print("You are an adult")

# if-else statement
temperature = 25
if temperature > 30:
    print("It's hot")
else:
    print("It's not hot")

# if-elif-else chain
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

# Ternary conditional expression (inline if)
status = "adult" if age >= 18 else "minor"
```

**Important:** Python uses indentation (typically 4 spaces) to define code blocks.

### 2. `for` Loops

`for` loops iterate over sequences (lists, strings, tuples, etc.) or other iterable objects.

```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over a string
for char in "Python":
    print(char)

# Iterate with range()
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 6):       # 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8 (step by 2)
    print(i)

# Iterate in reverse
for i in range(5, 0, -1):   # 5, 4, 3, 2, 1
    print(i)
```

### 3. `while` Loops

`while` loops continue executing as long as a condition is true.

```python
# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1

# While with else (executes when loop completes normally)
n = 3
while n > 0:
    print(n)
    n -= 1
else:
    print("Loop completed!")

# Infinite loop with break condition
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        break
```

### 4. Loop Control Statements: `break`, `continue`, `pass`

```python
# break - exit the loop immediately
for i in range(10):
    if i == 5:
        break  # Stop at 5
    print(i)    # Prints 0, 1, 2, 3, 4

# continue - skip to next iteration
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)       # Prints 1, 3, 5, 7, 9

# pass - do nothing (placeholder)
for i in range(5):
    if i == 3:
        pass  # TODO: handle this case later
    print(i)

# pass in function/class definitions
def function_to_be_implemented():
    pass  # Prevents syntax error

class FutureFeature:
    pass
```

### 5. `range()` Function

`range()` generates a sequence of numbers efficiently without storing them all in memory.

```python
# range(stop) - starts from 0
list(range(5))        # [0, 1, 2, 3, 4]

# range(start, stop) - includes start, excludes stop
list(range(2, 6))     # [2, 3, 4, 5]

# range(start, stop, step)
list(range(0, 10, 2)) # [0, 2, 4, 6, 8]
list(range(10, 0, -1))# [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# range is lazy (memory efficient)
r = range(1_000_000)  # Doesn't create a list in memory
```

### 6. `enumerate()` Function

`enumerate()` adds a counter to an iterable, useful when you need both index and value.

```python
fruits = ["apple", "banana", "cherry"]

# Without enumerate
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# With enumerate (more Pythonic)
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Start counting from 1
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")  # 1: apple, 2: banana, 3: cherry
```

### 7. `zip()` Function

`zip()` combines multiple iterables element-wise.

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

# Iterate over two lists in parallel
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# zip stops at the shortest iterable
short = [1, 2]
long = ["a", "b", "c", "d"]
list(zip(short, long))  # [(1, 'a'), (2, 'b')]

# zip with three or more iterables
a = [1, 2, 3]
b = ['a', 'b', 'c']
c = [True, False, True]
for x, y, z in zip(a, b, c):
    print(x, y, z)

# Create a dict from two lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))  # {'a': 1, 'b': 2, 'c': 3}
```

### 8. Nested Loops

Loops can be nested inside other loops.

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

### 9. Loop Comprehensions (Preview)

While comprehensions are more of a functional topic, here's a preview:

```python
# List comprehension (shorthand for loops)
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

---

## Common Mistakes

### 1. Off-by-One Errors

```python
# Wrong - misses the last element
for i in range(len(items) - 1):  # Should be len(items)
    print(items[i])

# Correct
for i in range(len(items)):
    print(items[i])

# Even better - iterate directly
for item in items:
    print(item)
```

### 2. Modifying a List While Iterating

```python
# Dangerous - modifying while iterating
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)  # Skips elements! Bug!

# Correct - iterate over a copy
for n in numbers[:]:  # Create a slice copy
    if n % 2 == 0:
        numbers.remove(n)

# Better - use list comprehension
evens_removed = [n for n in numbers if n % 2 != 0]
```

### 3. Infinite Loops

```python
# Forgot to increment - infinite loop!
count = 0
while count < 5:
    print(count)
    # Missing: count += 1

# Condition never becomes False
x = 10
while x > 0:
    print(x)
    x += 1  # Wrong direction - x keeps growing!
```

### 4. Indentation Errors

```python
# This looks right but isn't
if condition:
    print("Condition met")
    print("This is part of the if block")
print("This is NOT part of the if block - always executes")

# Mixing tabs and spaces (Python 3 forbids this)
# Always use 4 spaces for indentation
```

### 5. Misunderstanding `else` with Loops

```python
# The else executes when the loop completes normally (no break)
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed without break")  # This prints!

# Common confusion: else does NOT mean "if the condition is False"
while False:
    print("never runs")
else:
    print("this DOES run!")  # Because no break occurred
```

### 6. Using `range(len())` Unnecessarily

```python
# Un-Pythonic
for i in range(len(my_list)):
    print(my_list[i])

# Pythonic
for item in my_list:
    print(item)

# When you need the index, use enumerate
for i, item in enumerate(my_list):
    print(f"{i}: {item}")
```

---

## Connection to Exercises

Today's exercises reinforce control flow through classic algorithmic problems:

| Problem | Skills Practiced |
|---------|------------------|
| 01. fizz_buzz | Conditionals, modulo operator, loops |
| 02. is_prime | Loops, conditionals, early termination |
| 03. count_primes | Nested loops, sieve algorithm, efficiency |
| 04. generate_parentheses | Recursion simulation, backtracking pattern |
| 05. is_power_of_two | Bitwise thinking, mathematical loops |
| 06. is_happy_number | While loops, cycle detection, digit manipulation |
| 07. spiral_matrix | Nested loops, boundary tracking, 2D traversal |
| 08. rotate_image | Nested loops, matrix manipulation, in-place operations |
| 09. pascals_triangle | Pattern recognition, dynamic building, nested loops |
| 10. letter_combinations | Cartesian product, multiple iterations, recursion |

---

## Weekly Project Connection

The Week 1 project is a **Command-Line Quiz Game**. Day 5's concepts are essential because:

- **Loops** iterate through questions and handle replay functionality
- **Conditionals** check if answers are correct and handle menu choices
- **`enumerate()`** displays question numbers ("Question 1 of 10")
- **`zip()`** pairs questions with their correct answers
- **Control flow** manages the game state (playing, paused, finished)
- **Break/continue** handles early exit and skip question features

---

## Quick Reference

```python
# Conditionals
if condition:
    pass
elif other_condition:
    pass
else:
    pass

# For loop
for item in iterable:
    pass

# While loop
while condition:
    pass

# Loop control
break      # Exit loop immediately
continue   # Skip to next iteration
pass       # Do nothing (placeholder)

# Useful functions
range(stop)              # 0 to stop-1
range(start, stop)       # start to stop-1
range(start, stop, step) # With step size

enumerate(iterable)           # (0, item0), (1, item1), ...
enumerate(iterable, start=1)  # (1, item0), (2, item1), ...

zip(a, b, c)             # (a0, b0, c0), (a1, b1, c1), ...

# Nested loops
for i in range(n):
    for j in range(m):
        pass
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Review any problems you found challenging
3. Compare your solutions with the reference implementations
4. Preview Day 6: **Functions Deep Dive** - where you'll master function definition and scope
