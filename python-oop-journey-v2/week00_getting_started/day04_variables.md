# Day 04: Variables and Assignment

## Learning Objectives

By the end of this day, you will be able to:

1. Create and use variables in Python
2. Follow Python naming conventions for variables
3. Use assignment statements to store values
4. Perform multiple assignment in Python
5. Unpack values from tuples into variables

---

## Key Concepts

### 1. What is a Variable?

A variable is a name that refers to a value stored in memory. Think of it as a labeled box where you can store data.

```python
# Creating variables
name = "Alice"      # A string value
age = 25            # An integer value
height = 5.6        # A float value
```

### 2. Variable Naming Rules

**Must follow these rules:**
- Must start with a letter (a-z, A-Z) or underscore (_)
- Can contain letters, digits (0-9), and underscores
- Cannot use reserved keywords (like `if`, `for`, `class`, `def`)
- Case-sensitive (`name` and `Name` are different)

```python
# Valid names
my_variable = 1
_my_var = 2
myVar2 = 3
MY_VAR = 4

# Invalid names
2myvar = 1      # Starts with a number
my-var = 2      # Contains hyphen
my var = 3      # Contains space
class = 4       # Reserved keyword
```

### 3. Naming Conventions (Best Practices)

Use `snake_case` for variable names:

```python
# Good (snake_case)
student_name = "Alice"
total_score = 95
is_valid = True

# Avoid (camelCase is for Java, not Python)
studentName = "Alice"   # Works, but not Pythonic

# Avoid (single letters, unclear names)
x = "Alice"     # What does x represent?
n = 95          # What is n?
```

### 4. Assignment Statement

The `=` sign is the assignment operator. It stores the value on the right into the variable on the left.

```python
# Basic assignment
x = 10          # x now refers to the value 10
y = x + 5       # y now refers to 15

# Reassignment
x = 10
x = 20          # x now refers to 20 (old value is forgotten)
```

### 5. Multiple Assignment

Python allows assigning multiple variables at once:

```python
# Assign same value to multiple variables
x = y = z = 0
print(x, y, z)  # Output: 0 0 0

# Assign different values at once
a, b, c = 1, 2, 3
print(a, b, c)  # Output: 1 2 3
```

### 6. Swapping Variables

Using a temporary variable:

```python
a = 5
b = 10

# Swap using temp variable
temp = a
a = b
b = temp

print(a, b)     # Output: 10 5
```

### 7. Tuple Unpacking

Extract values from a tuple into separate variables:

```python
coordinates = (3, 4)
x, y = coordinates
print(x)        # Output: 3
print(y)        # Output: 4

# Works with any iterable
data = [1, 2, 3]
a, b, c = data
print(a, b, c)  # Output: 1 2 3
```

---

## Common Mistakes

```python
# Mistake 1: Using a variable before defining it
print(undefined_var)    # NameError!

# Mistake 2: Confusing = with ==
x = 5       # Assignment (store 5 in x)
x == 5      # Comparison (is x equal to 5?)

# Mistake 3: Variable names starting with numbers
1st_place = "Gold"      # SyntaxError!

# Mistake 4: Using reserved keywords
class = "Math"          # SyntaxError!
```

---

## Practice Exercises

Complete the exercises in `exercises/day04/`:

1. **Problem 01**: Assign and Print Variable
2. **Problem 02**: Swap Two Variables
3. **Problem 03**: Multiple Assignment
4. **Problem 04**: Variable Naming Conventions
5. **Problem 05**: Unpack and Sum

Run the tests with: `pytest week00_getting_started/tests/day04/`
