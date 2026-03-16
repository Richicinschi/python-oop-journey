# Day 10: While Loops

## Learning Objectives

By the end of this day, you will be able to:

1. Write `while` loops for conditional repetition
2. Use `break` to exit loops early
3. Use `continue` to skip iterations
4. Avoid infinite loops
5. Apply while loops to solve iteration problems
6. Use `else` clauses with loops

---

## Key Concepts

### 1. Basic While Loop

Repeat code while a condition is true:

```python
count = 0
while count < 5:
    print(count)
    count += 1

# Output: 0, 1, 2, 3, 4
```

**Important:** The loop body must eventually make the condition false, or you'll have an infinite loop.

### 2. While with Else

The `else` block runs when the loop completes normally (no `break`):

```python
n = 3
while n > 0:
    print(n)
    n -= 1
else:
    print("Loop completed!")

# Output: 3, 2, 1, Loop completed!
```

### 3. Break Statement

Exit the loop immediately:

```python
# Find first number divisible by 7
num = 1
while num <= 100:
    if num % 7 == 0:
        print(f"Found: {num}")
        break
    num += 1

# User input loop
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        break
    print(f"You entered: {user_input}")
```

### 4. Continue Statement

Skip to the next iteration:

```python
# Print only odd numbers
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue  # Skip even numbers
    print(num)

# Output: 1, 3, 5, 7, 9
```

### 5. Infinite Loops

Loops that run forever (use with caution):

```python
# Server or game loop pattern
while True:
    # Process events
    # Update state
    # Render
    if should_exit:
        break

# Common mistake - infinite loop!
count = 0
while count < 5:
    print(count)
    # Forgot: count += 1  <-- INFINITE LOOP!
```

### 6. Input Validation

Classic use case for while loops:

```python
# Get valid age
age = -1
while age < 0 or age > 150:
    age_input = input("Enter your age (0-150): ")
    if age_input.isdigit():
        age = int(age_input)
    else:
        print("Please enter a number")

print(f"Your age is: {age}")
```

### 7. Loop Patterns

```python
# Count up
i = 0
while i < 10:
    print(i)
    i += 1

# Count down
i = 10
while i > 0:
    print(i)
    i -= 1

# Process digits of a number
num = 12345
while num > 0:
    digit = num % 10  # Get last digit
    print(digit)
    num //= 10        # Remove last digit
```

### 8. Flag Variables

Control loops with boolean flags:

```python
found = False
i = 0
while i < 100 and not found:
    if is_prime(i):
        print(f"First prime: {i}")
        found = True
    i += 1
```

---

## Common Mistakes

### 1. Infinite Loops

```python
# Wrong - condition never becomes false
x = 5
while x > 0:
    print(x)
    x += 1  # x keeps growing!

# Correct
x = 5
while x > 0:
    print(x)
    x -= 1
```

### 2. Wrong Comparison

```python
# Wrong - uses = instead of ==
while x = 5:   # Syntax error!
    pass

# Correct
while x == 5:
    pass
```

### 3. Off-by-One Errors

```python
# Wrong - misses 10
i = 1
while i < 10:  # Stops at 9
    print(i)
    i += 1

# Correct
i = 1
while i <= 10:  # Includes 10
    print(i)
    i += 1
```

### 4. Modifying Loop Variable Incorrectly

```python
# Wrong - skips numbers
i = 0
while i < 10:
    print(i)
    i += 1
    if i == 5:
        i += 1  # Now 6, loop continues from 6 - skips 5!

# Better - handle special case before increment
i = 0
while i < 10:
    if i == 5:
        print("Skipping 5")
        i += 1
        continue
    print(i)
    i += 1
```

### 5. Forgetting to Initialize Variable

```python
# Wrong - i is undefined
while i < 10:  # NameError!
    pass

# Correct
i = 0
while i < 10:
    pass
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. count_down | Basic while loop, counting down |
| 02. sum_until_limit | Accumulating values in a loop |
| 03. find_first_divisible | Using break effectively |
| 04. skip_multiples | Using continue statement |
| 05. guess_number_pattern | Input validation, infinite loop with break |

---

## Quick Reference

```python
# Basic while
while condition:
    pass

# With else (runs if no break)
while condition:
    pass
else:
    pass

# Control statements
break      # Exit loop immediately
continue   # Skip to next iteration

# Common patterns
while True:           # Infinite loop (use break)
while x < n:          # Count up
while x > 0:          # Count down
while not found:      # Search pattern
```

---

## Next Steps

After completing today's exercises:
1. Practice tracing through while loops by hand
2. Convert between while loops and for loops
3. Preview Day 11: **For Loops** - a more Pythonic way to iterate
