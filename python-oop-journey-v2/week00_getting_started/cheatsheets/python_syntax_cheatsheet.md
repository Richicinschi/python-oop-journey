# Python Syntax Cheatsheet

Quick reference for Python basics: variables, types, and operators.

---

## Variable Assignment

```python
# Basic assignment
name = "Alice"
age = 25
pi = 3.14159
is_valid = True

# Multiple assignment
x, y, z = 1, 2, 3

# Same value to multiple variables
a = b = c = 0

# Swapping values
a, b = b, a
```

---

## Data Types Quick Reference

| Type | Description | Example |
|------|-------------|---------|
| `int` | Integer (whole numbers) | `42`, `-7`, `0` |
| `float` | Floating point (decimals) | `3.14`, `-0.5`, `2.0` |
| `str` | String (text) | `"Hello"`, `'Python'` |
| `bool` | Boolean (True/False) | `True`, `False` |
| `None` | Null/empty value | `None` |
| `list` | Ordered, mutable collection | `[1, 2, 3]` |
| `tuple` | Ordered, immutable collection | `(1, 2, 3)` |
| `dict` | Key-value pairs | `{"key": "value"}` |
| `set` | Unordered, unique items | `{1, 2, 3}` |

---

## Type Checking & Conversion

```python
# Check type
type(x)           # Returns the type of x
isinstance(x, int)  # True if x is an int

# Type conversion (casting)
int("42")         # 42 (string to int)
float("3.14")     # 3.14 (string to float)
str(42)           # "42" (int to string)
bool(1)           # True (truthy values)
list("abc")       # ['a', 'b', 'c']
```

---

## Arithmetic Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division (always float) | `5 / 2` | `2.5` |
| `//` | Floor division | `5 // 2` | `2` |
| `%` | Modulo (remainder) | `5 % 2` | `1` |
| `**` | Exponentiation | `2 ** 3` | `8` |

```python
# Operator precedence (PEMDAS)
# Parentheses > Exponents > Multiplication/Division > Addition/Subtraction

result = 2 + 3 * 4      # 14 (not 20)
result = (2 + 3) * 4    # 20

# Augmented assignment
x = 5
x += 3      # x = x + 3, x is now 8
x -= 2      # x = x - 2, x is now 6
x *= 4      # x = x * 4, x is now 24
x /= 6      # x = x / 6, x is now 4.0
```

---

## Comparison Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<=` | Less than or equal | `5 <= 5` | `True` |
| `>=` | Greater than or equal | `5 >= 3` | `True` |

```python
# Chained comparisons
1 < x < 10      # Same as: 1 < x and x < 10
```

---

## Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Both must be True | `True and False` → `False` |
| `or` | At least one True | `True or False` → `True` |
| `not` | Inverts the value | `not True` → `False` |

```python
# Truthy values: non-zero numbers, non-empty collections, True
# Falsy values: 0, 0.0, "", [], {}, None, False

x = 5
y = 0

bool(x)     # True (truthy)
bool(y)     # False (falsy)

# Short-circuit evaluation
result = x and y    # Returns y (first falsy) or last truthy
result = x or y     # Returns x (first truthy) or last falsy
```

---

## String Basics

```python
# String creation
single = 'Hello'
double = "World"
multi = """Multi
line string"""

# String concatenation
full = "Hello" + " " + "World"   # "Hello World"

# String repetition
dashes = "-" * 10                 # "----------"

# String formatting (f-strings)
name = "Alice"
age = 25
message = f"Hello, {name}! You are {age} years old."

# Alternative formatting
"Hello, {}!".format(name)
"Hello, %s!" % name
```

---

## Input and Output

```python
# Print function
print("Hello, World!")
print("Value:", 42)           # Multiple arguments
print("a", "b", "c", sep="-")  # a-b-c
print("Hello", end=" ")        # No newline at end
print("World")                # Hello World

# Input (always returns string)
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # Convert to int
```

---

## Common Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `print()` | Output to console | `print("Hello")` |
| `input()` | Get user input | `name = input("Name: ")` |
| `len()` | Length of object | `len("abc")` → `3` |
| `range()` | Generate sequence | `range(5)` → `0,1,2,3,4` |
| `type()` | Get object type | `type(42)` → `<class 'int'>` |
| `int()` | Convert to integer | `int("42")` → `42` |
| `str()` | Convert to string | `str(42)` → `"42"` |
| `float()` | Convert to float | `float("3.14")` → `3.14` |
| `round()` | Round number | `round(3.14159, 2)` → `3.14` |
| `abs()` | Absolute value | `abs(-5)` → `5` |
| `max()` | Maximum value | `max(1, 5, 3)` → `5` |
| `min()` | Minimum value | `min(1, 5, 3)` → `1` |
| `sum()` | Sum of iterable | `sum([1, 2, 3])` → `6` |

---

## Quick Tips

1. **Python is case-sensitive**: `Name` and `name` are different variables
2. **Indentation matters**: Use 4 spaces (not tabs)
3. **Comments**: Use `#` for single-line, `'''` or `"""` for multi-line
4. **Variable naming**: Use `snake_case` for variables, avoid starting with numbers
5. **No semicolons**: End of line means end of statement
