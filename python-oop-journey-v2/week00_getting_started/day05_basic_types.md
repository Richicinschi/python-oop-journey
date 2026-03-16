# Day 05: Basic Data Types

## Learning Objectives

By the end of this day, you will be able to:

1. Identify and use Python's basic data types: `int`, `float`, `str`, `bool`
2. Use the `type()` function to check data types
3. Convert between different data types
4. Understand truthy and falsy values in Python

---

## Key Concepts

### 1. Integer (`int`)

Whole numbers, positive or negative, without decimals.

```python
age = 25
negative = -10
zero = 0
big_number = 1_000_000    # Underscores for readability
```

### 2. Float (`float`)

Numbers with decimal points.

```python
price = 19.99
pi = 3.14159
scientific = 6.022e23     # Scientific notation
temperature = -5.5
```

### 3. String (`str`)

Text data enclosed in quotes.

```python
name = "Alice"
greeting = 'Hello'
multiline = """This is
a multi-line
string"""
empty = ""
```

### 4. Boolean (`bool`)

Represents True or False.

```python
is_valid = True
has_error = False
```

### 5. Checking Types with `type()`

```python
x = 42
print(type(x))          # <class 'int'>
print(type(x).__name__) # 'int'

y = 3.14
print(type(y))          # <class 'float'>

z = "hello"
print(type(z))          # <class 'str'>
```

### 6. Type Conversion

Convert between types using constructor functions:

```python
# String to integer
num_str = "42"
num = int(num_str)      # 42

# Integer to string
text = str(42)          # "42"

# Float to integer (truncates)
int(3.7)                # 3
int(3.2)                # 3

# Integer to float
float(42)               # 42.0

# To boolean
bool(1)                 # True
bool(0)                 # False
bool("")                # False
bool("hello")           # True
```

### 7. Truthy and Falsy Values

**Falsy values** (convert to `False`):
- `0` (integer zero)
- `0.0` (float zero)
- `""` (empty string)
- `None` (represents no value)
- `[]` (empty list)
- `{}` (empty dictionary)

**Truthy values** (convert to `True`):
- All non-zero numbers
- All non-empty strings
- All non-empty collections

```python
# Examples
bool(0)                 # False
bool(5)                 # True
bool(-1)                # True
bool("")                # False
bool("hello")           # True
bool(None)              # False
```

---

## Common Mistakes

```python
# Mistake 1: Converting invalid string to int
int("hello")            # ValueError!

# Mistake 2: Float to int truncates, doesn't round
int(3.9)                # 3, not 4!

# Mistake 3: Forgetting quotes make numbers
x = 42      # This is an integer
y = "42"    # This is a string

# Mistake 4: Concatenating string with number
age = 25
msg = "I am " + age     # TypeError!
msg = "I am " + str(age)  # Correct: "I am 25"
```

---

## Practice Exercises

Complete the exercises in `exercises/day05/`:

1. **Problem 01**: Get Type Information
2. **Problem 02**: Convert to Integer
3. **Problem 03**: Convert to String
4. **Problem 04**: Check Boolean Truthiness
5. **Problem 05**: Convert to Float

Run the tests with: `pytest week00_getting_started/tests/day05/`
