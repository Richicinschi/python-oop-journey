# Day 8: Boolean Logic

## Learning Objectives

By the end of this day, you will be able to:

1. Understand boolean values (`True` and `False`) in Python
2. Use comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
3. Combine conditions with logical operators (`and`, `or`, `not`)
4. Evaluate complex boolean expressions
5. Apply boolean logic to make decisions in code

---

## Key Concepts

### 1. Boolean Values

Python has two boolean values: `True` and `False`.

```python
is_active = True
is_admin = False

print(type(is_active))  # <class 'bool'>
```

### 2. Comparison Operators

Comparison operators compare values and return booleans:

```python
# Equal to (==)
5 == 5      # True
5 == 3      # False

# Not equal to (!=)
5 != 3      # True
5 != 5      # False

# Greater than (>)
10 > 5      # True
5 > 10      # False

# Less than (<)
3 < 7       # True
7 < 3       # False

# Greater than or equal to (>=)
5 >= 5      # True
5 >= 3      # True

# Less than or equal to (<=)
3 <= 5      # True
5 <= 5      # True
```

**Important:** Use `==` for comparison, `=` for assignment.

```python
x = 5       # Assignment
x == 5      # Comparison (True)
```

### 3. Logical Operators

Combine boolean expressions with `and`, `or`, `not`:

```python
# and - both must be True
True and True     # True
True and False    # False
False and True    # False
False and False   # False

# or - at least one must be True
True or True      # True
True or False     # True
False or True     # True
False or False    # False

# not - inverts the boolean
not True          # False
not False         # True
```

### 4. Truthiness and Falsiness

Values have "truthiness" in boolean contexts:

```python
# Falsy values
bool(0)           # False
bool("")          # False (empty string)
bool([])          # False (empty list)
bool({})          # False (empty dict)
bool(None)        # False

# Truthy values (everything else)
bool(1)           # True
bool(-5)          # True (non-zero numbers)
bool("hello")     # True (non-empty string)
bool([1, 2, 3])   # True (non-empty list)
```

### 5. Operator Precedence

Order of operations for boolean expressions:

```python
# 1. Comparison operators (==, !=, <, >, <=, >=)
# 2. not
# 3. and
# 4. or

# Use parentheses for clarity
result = (x > 0) and (y > 0) or (z > 0)
result = (x > 0) and ((y > 0) or (z > 0))  # Different meaning!
```

### 6. Short-Circuit Evaluation

Python stops evaluating as soon as the result is known:

```python
# and stops at first False
False and expensive_function()  # expensive_function never runs

# or stops at first True
True or expensive_function()    # expensive_function never runs

# Practical use: default values
name = user_input or "Anonymous"
```

### 7. Chained Comparisons

Python supports mathematical-style comparisons:

```python
# These are equivalent
1 < x < 10
1 < x and x < 10

# More examples
0 <= grade <= 100
'a' <= char <= 'z'
```

---

## Common Mistakes

### 1. Using `=` Instead of `==`

```python
# Wrong
if x = 5:      # Syntax error!
    pass

# Correct
if x == 5:
    pass
```

### 2. `is` vs `==`

```python
# == compares values
[1, 2] == [1, 2]      # True

# is compares identity (memory location)
[1, 2] is [1, 2]      # False (different objects)

a = [1, 2]
b = a
a is b                # True (same object)

# Use is only for None, True, False
x is None             # Correct
x is True             # Correct
```

### 3. Truthy/Falsy Confusion

```python
# Wrong - checks if list is not None (always True for list!)
if my_list != None:   # Bad style

# Correct - checks if list is not empty
if my_list:           # Pythonic

# Explicit length check (also fine)
if len(my_list) > 0:
```

### 4. Complex Expressions Without Parentheses

```python
# Confusing
result = x > 0 and y > 0 or z > 0 and w > 0

# Clear
result = (x > 0 and y > 0) or (z > 0 and w > 0)
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. check_equality | Basic comparison operators |
| 02. is_in_range | Chained comparisons, logical operators |
| 03. validate_password | Combining multiple conditions with `and` |
| 04. can_vote | Complex boolean logic with age rules |
| 05. logical_operations | Understanding `and`, `or`, `not` behavior |

---

## Quick Reference

```python
# Comparisons
==   # Equal to
!=   # Not equal to
<    # Less than
>    # Greater than
<=   # Less than or equal
>=   # Greater than or equal

# Logical operators
and  # True if both are True
or   # True if at least one is True
not  # Inverts the boolean

# Falsy values
0, "", [], {}, None

# Chained comparisons
1 < x < 10  # Same as: 1 < x and x < 10
```

---

## Next Steps

After completing today's exercises:
1. Practice writing boolean expressions
2. Test your understanding with edge cases
3. Preview Day 9: **If Statements** - where you'll use booleans to control program flow
