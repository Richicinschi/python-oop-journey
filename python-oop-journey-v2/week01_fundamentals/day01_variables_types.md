# Day 1: Variables, Data Types, Arithmetic, Basic Operations

## Learning Objectives

By the end of this day, you will be able to:

1. Declare and use variables in Python
2. Understand and work with Python's basic data types (`int`, `float`, `str`, `bool`, `None`)
3. Perform arithmetic operations and understand operator precedence
4. Convert between different data types safely
5. Apply these fundamentals to solve mathematical and logical problems

---

## Key Concepts

### 1. Variables

Variables are names that refer to values stored in memory. Python uses dynamic typing—you don't declare the type explicitly.

```python
# Variable assignment
age = 25           # integer
temperature = 98.6  # float
name = "Alice"     # string
is_valid = True    # boolean
result = None      # NoneType (represents absence of value)
```

**Naming rules:**
- Must start with a letter or underscore
- Can contain letters, digits, and underscores
- Case-sensitive (`age` ≠ `Age`)
- Cannot use reserved keywords (like `if`, `for`, `class`)

**Naming conventions:**
- Use `snake_case` for variables and functions
- Use descriptive names: `student_count` instead of `sc`

### 2. Numeric Types: `int` and `float`

**Integers (`int`)**: Whole numbers, unlimited precision in Python 3.

```python
positive = 42
negative = -17
zero = 0
big_number = 1_000_000_000  # Underscores for readability
```

**Floating-point numbers (`float`)**: Numbers with decimal points.

```python
pi = 3.14159
scientific = 6.022e23  # 6.022 × 10²³
ratio = 1 / 3
```

**Arithmetic Operators:**

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division (always float) | `5 / 2` | `2.5` |
| `//` | Floor division | `5 // 2` | `2` |
| `%` | Modulo (remainder) | `5 % 2` | `1` |
| `**` | Exponentiation | `2 ** 3` | `8` |

**Operator Precedence** (highest to lowest):
1. Parentheses `()`
2. Exponentiation `**`
3. Unary plus/minus `+x`, `-x`
4. Multiplication, division, floor division, modulo `*`, `/`, `//`, `%`
5. Addition, subtraction `+`, `-`

```python
result = 2 + 3 * 4      # 14 (not 20)
result = (2 + 3) * 4    # 20
result = 2 ** 3 ** 2    # 512 (right-to-left: 2^(3^2))
```

### 3. Strings (`str`)

Strings represent text and are immutable sequences of characters.

```python
single = 'Hello'
double = "World"
multiline = """This is a
multi-line string"""

# String operations
full = single + " " + double  # Concatenation: "Hello World"
repeated = "Hi" * 3           # Repetition: "HiHiHi"
length = len("Python")        # Length: 6
```

### 4. Booleans (`bool`)

Booleans represent truth values: `True` or `False`.

```python
is_active = True
has_error = False

# Comparison operators return booleans
result = 5 > 3    # True
result = 5 == 3   # False
result = 5 != 3   # True
```

**Truthy and Falsy values:**
- Falsy: `None`, `0`, `0.0`, `''` (empty string), `[]` (empty list), etc.
- Truthy: Everything else

### 5. `None` Type

`None` represents the absence of a value. It's a singleton object of type `NoneType`.

```python
result = None  # No value yet

def find_item():
    return None  # Indicates "not found"
```

### 6. Type Conversion

Convert between types using constructor functions:

```python
# String to number
num = int("42")        # 42 (int)
price = float("19.99") # 19.99 (float)

# Number to string
text = str(42)         # "42"

# To boolean
flag = bool(1)         # True
flag = bool(0)         # False
flag = bool("")        # False
flag = bool("hello")   # True
```

**Safe conversion with error handling:**

```python
def safe_int(value: str) -> int | None:
    """Try to convert string to int, return None if invalid."""
    try:
        return int(value)
    except ValueError:
        return None
```

### 7. Tuple Unpacking

Python allows assigning multiple values at once:

```python
# Basic unpacking
x, y = 10, 20

# Swapping values
a, b = 5, 10
a, b = b, a  # Now a=10, b=5

# Multiple assignment
first, second, third = 1, 2, 3
```

---

## Common Mistakes

### 1. Integer Division vs Float Division

```python
# Wrong assumption
result = 5 / 2      # Result is 2.5 (float), not 2!

# For integer result, use floor division
result = 5 // 2     # Result is 2 (int)
```

### 2. Modulo with Negative Numbers

```python
result = -5 % 3     # Result is 1 (not -2)
# Python's modulo always returns non-negative result for positive divisor
```

### 3. Mutable Default Arguments (Preview)

While not directly in today's scope, this is a famous gotcha:

```python
# This will be covered in Week 2-3
def bad_function(items=[]):  # Don't do this!
    items.append(1)
    return items
```

### 4. String vs Number Concatenation

```python
age = 25
# message = "I am " + age      # TypeError!
message = "I am " + str(age)   # Correct: "I am 25"
# Or use f-strings (covered later): f"I am {age}"
```

### 5. Comparing Floats for Equality

```python
# Dangerous
if 0.1 + 0.2 == 0.3:  # False! (floating point precision)

# Better approach
abs(0.1 + 0.2 - 0.3) < 1e-9  # True
```

### 6. Type Checking with `is` vs `==`

```python
x = None
if x is None:       # Correct - check identity
    pass

if x == None:       # Works but not recommended
    pass
```

---

## Connection to Exercises

Today's exercises reinforce these concepts through practical problems:

| Problem | Skills Practiced |
|---------|------------------|
| 01. calculate_sum | Basic arithmetic, function definition |
| 02. celsius_to_fahrenheit | Arithmetic formulas, float operations |
| 03. divide_with_remainder | Division operators, tuple return |
| 04. is_perfect_square | Math operations, boolean logic |
| 05. reverse_integer | Integer manipulation, loops (preview) |
| 06. count_even_digits | Digit extraction, conditionals |
| 07. power | Loops, efficient computation |
| 08. swap_values | Tuple unpacking, multiple assignment |
| 09. validate_and_convert | Type conversion, error handling |
| 10. gcd | Algorithms, Euclidean algorithm |
| 11. is_palindrome_number | Digit manipulation, comparison |

---

## Weekly Project Connection

The Week 1 project is a **Command-Line Quiz Game**. Day 1's concepts are essential because:

- **Variables** store the quiz questions, answers, and player score
- **Booleans** track whether answers are correct
- **Type conversion** handles user input (strings) and score calculation (integers)
- **Arithmetic** calculates the final percentage score

---

## Quick Reference

```python
# Variable declaration
name = value

# Common types
int_val = 42
float_val = 3.14
str_val = "hello"
bool_val = True
none_val = None

# Arithmetic
a + b   # Addition
a - b   # Subtraction
a * b   # Multiplication
a / b   # Division (float)
a // b  # Floor division
a % b   # Modulo (remainder)
a ** b  # Exponentiation

# Type checking
type(x)           # Get type
isinstance(x, int)  # Check if int

# Type conversion
int(x)      # Convert to integer
float(x)    # Convert to float
str(x)      # Convert to string
bool(x)     # Convert to boolean
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Review any problems you found challenging
3. Preview Day 2: **Strings** - where you'll work with text manipulation
