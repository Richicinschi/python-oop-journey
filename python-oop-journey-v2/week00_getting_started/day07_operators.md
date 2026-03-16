# Day 07: Basic Operators

## Learning Objectives

By the end of this day, you will be able to:

1. Use arithmetic operators for calculations
2. Use comparison operators to compare values
3. Use logical operators to combine conditions
4. Understand operator precedence

---

## Key Concepts

### 1. Arithmetic Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division (always float) | `7 / 2` | `3.5` |
| `//` | Floor Division | `7 // 2` | `3` |
| `%` | Modulo (remainder) | `7 % 2` | `1` |
| `**` | Exponentiation | `2 ** 3` | `8` |

```python
# Examples
print(10 + 5)       # 15
print(10 - 5)       # 5
print(10 * 5)       # 50
print(10 / 3)       # 3.333... (always float)
print(10 // 3)      # 3 (integer division)
print(10 % 3)       # 1 (remainder)
print(2 ** 4)       # 16 (2 to the power of 4)
```

### 2. Comparison Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `5 <= 3` | `False` |

```python
# Examples
x = 10
y = 5

print(x == y)       # False
print(x != y)       # True
print(x > y)        # True
print(x < y)        # False
print(x >= 10)      # True
print(x <= 10)      # True

# Chained comparison
print(1 < x < 20)   # True (x is between 1 and 20)
```

### 3. Logical Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `and` | Both must be True | `True and False` | `False` |
| `or` | At least one True | `True or False` | `True` |
| `not` | Inverts the value | `not True` | `False` |

```python
# and - both must be True
print(True and True)    # True
print(True and False)   # False
print(False and False)  # False

# or - at least one must be True
print(True or False)    # True
print(False or True)    # True
print(False or False)   # False

# not - inverts the boolean
print(not True)         # False
print(not False)        # True

# Practical example
age = 25
has_id = True
can_enter = age >= 18 and has_id
print(can_enter)        # True
```

### 4. Operator Precedence

Order of operations (highest to lowest):

1. Parentheses `()`
2. Exponentiation `**`
3. Unary plus/minus `+x`, `-x`
4. Multiplication, division, floor division, modulo `*`, `/`, `//`, `%`
5. Addition, subtraction `+`, `-`
6. Comparison operators `==`, `!=`, `>`, `<`, `>=`, `<=`
7. Logical `not`
8. Logical `and`
9. Logical `or`

```python
# Examples
result = 2 + 3 * 4          # 14 (not 20)
result = (2 + 3) * 4        # 20

result = 2 ** 3 + 1         # 9 (not 16)
result = 2 ** (3 + 1)       # 16

result = 10 > 5 and 5 > 2   # True
result = not 5 > 10         # True
```

### 5. Compound Assignment Operators

```python
x = 10

x += 5      # Same as: x = x + 5
x -= 3      # Same as: x = x - 3
x *= 2      # Same as: x = x * 2
x /= 4      # Same as: x = x / 4
x //= 2     # Same as: x = x // 2
x %= 3      # Same as: x = x % 3
x **= 2     # Same as: x = x ** 2
```

---

## Common Mistakes

```python
# Mistake 1: Using = instead of ==
if x = 5:           # SyntaxError! This is assignment
if x == 5:          # Correct! This is comparison

# Mistake 2: Integer division vs float division
print(5 / 2)        # 2.5 (float division)
print(5 // 2)       # 2 (floor division)

# Mistake 3: Modulo with negative numbers
print(-5 % 3)       # 1 (result has same sign as divisor)

# Mistake 4: Operator precedence confusion
result = 2 + 3 * 4      # 14, not 20
result = 2 ** 3 ** 2    # 512, not 64 (right to left!)
```

---

## Practice Exercises

Complete the exercises in `exercises/day07/`:

1. **Problem 01**: Arithmetic Operations
2. **Problem 02**: Compare Numbers
3. **Problem 03**: Check In Range
4. **Problem 04**: Logical AND and OR
5. **Problem 05**: Calculate Remainder and Quotient

Run the tests with: `pytest week00_getting_started/tests/day07/`
