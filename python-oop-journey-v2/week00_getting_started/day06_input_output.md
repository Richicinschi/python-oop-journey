# Day 06: Simple Input and Output

## Learning Objectives

By the end of this day, you will be able to:

1. Use `print()` to display output
2. Use `input()` to get user input
3. Create formatted strings using f-strings
4. Format numbers and text in output

---

## Key Concepts

### 1. The `print()` Function

Display output to the screen:

```python
print("Hello, World!")
print(42)
print(3.14)

# Print multiple items
print("Age:", 25)           # Output: Age: 25
print(1, 2, 3)              # Output: 1 2 3

# Print with custom separator
print(1, 2, 3, sep="-")     # Output: 1-2-3

# Print without newline
print("Hello", end=" ")
print("World")              # Output: Hello World
```

### 2. The `input()` Function

Get user input (always returns a string):

```python
name = input("Enter your name: ")
print("Hello,", name)

# Input always returns a string
age_str = input("Enter your age: ")
age = int(age_str)          # Convert to integer
print("Next year you will be", age + 1)
```

### 3. F-Strings (Formatted String Literals)

The modern way to format strings in Python:

```python
name = "Alice"
age = 25

# Basic f-string
greeting = f"Hello, {name}!"
print(greeting)             # Hello, Alice!

# F-string with expressions
message = f"Next year, {name} will be {age + 1}"
print(message)              # Next year, Alice will be 26
```

### 4. Formatting Numbers in F-Strings

```python
price = 19.99
quantity = 3

# Format to 2 decimal places
print(f"Price: ${price:.2f}")       # Price: $19.99

# Format integer with padding
print(f"Quantity: {quantity:03d}")  # Quantity: 003

# Format percentage
discount = 0.15
print(f"Discount: {discount:.1%}")  # Discount: 15.0%
```

### 5. Multi-line Output

```python
name = "Alice"
age = 25

# Using \n for newlines
info = f"Name: {name}\nAge: {age}"
print(info)
# Output:
# Name: Alice
# Age: 25

# Using triple quotes
report = f"""
Student Report
--------------
Name: {name}
Age: {age}
"""
print(report)
```

### 6. Combining Input and Output

```python
# Simple calculator
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
sum_result = num1 + num2

print(f"The sum of {num1} and {num2} is {sum_result}")
```

---

## Common Mistakes

```python
# Mistake 1: Forgetting input() returns a string
age = input("Enter age: ")
next_year = age + 1         # TypeError! Can't add string and int

# Correct:
age = int(input("Enter age: "))
next_year = age + 1

# Mistake 2: Forgetting the 'f' prefix
name = "Alice"
print("Hello, {name}")      # Prints: Hello, {name}
print(f"Hello, {name}")     # Prints: Hello, Alice

# Mistake 3: Wrong format specifier
num = 42
print(f"{num:.2f}")         # 42.00 (works, adds decimals)
text = "hello"
print(f"{text:.2f}")        # TypeError! Can't format string as float
```

---

## Practice Exercises

Complete the exercises in `exercises/day06/`:

1. **Problem 01**: Format Greeting
2. **Problem 02**: Format Sum Output
3. **Problem 03**: Format Person Info
4. **Problem 04**: Format Price Tag
5. **Problem 05**: Format Calculation Table

Run the tests with: `pytest week00_getting_started/tests/day06/`
