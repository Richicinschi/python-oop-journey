# Day 9: If Statements

## Learning Objectives

By the end of this day, you will be able to:

1. Write `if` statements to make decisions in code
2. Use `if-else` for binary choices
3. Chain conditions with `if-elif-else`
4. Understand Python's indentation rules
5. Apply nested conditionals for complex logic
6. Use ternary expressions for simple conditionals

---

## Key Concepts

### 1. Basic If Statement

Execute code only when a condition is true:

```python
age = 18

if age >= 18:
    print("You are an adult")

print("This always runs")
```

**Important:** Python uses indentation (4 spaces) to define code blocks.

### 2. If-Else Statement

Choose between two alternatives:

```python
 temperature = 25

if temperature > 30:
    print("It's hot")
else:
    print("It's not hot")
```

### 3. If-Elif-Else Chain

Handle multiple conditions:

```python
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

print(f"Your grade is: {grade}")
```

**Key points:**
- Conditions are checked in order
- Only the first matching block runs
- `else` is optional but recommended for completeness

### 4. Indentation Rules

Python uses indentation to define code blocks:

```python
if condition:
    # 4 spaces - part of the if block
    print("Inside if")
    x = 5
# No indentation - outside the if block
print("Outside if")

# Nested if
if outer_condition:
    print("Outer block")
    if inner_condition:
        print("Inner block")  # 8 spaces total
    print("Back to outer")
print("Outside all")
```

**Rules:**
- Use exactly 4 spaces per indentation level
- Never mix tabs and spaces
- Be consistent throughout your file

### 5. Nested If Statements

Place if statements inside other if statements:

```python
has_id = True
age = 20

if has_id:
    if age >= 18:
        print("Entry granted")
    else:
        print("Too young")
else:
    print("ID required")

# Can be flattened with 'and'
if has_id and age >= 18:
    print("Entry granted")
elif not has_id:
    print("ID required")
else:
    print("Too young")
```

### 6. Ternary Expression

Compact form for simple if-else:

```python
# Long form
if age >= 18:
    status = "adult"
else:
    status = "minor"

# Ternary form
status = "adult" if age >= 18 else "minor"

# Can be used directly
print("Welcome" if is_logged_in else "Please log in")
```

### 7. Truthiness in Conditionals

Use truthy/falsy values directly:

```python
name = ""

# Check if string is not empty
if name:  # True if name is not empty
    print(f"Hello, {name}")
else:
    print("Name is empty")

# Check if list has items
items = [1, 2, 3]
if items:  # True if list is not empty
    print(f"You have {len(items)} items")
```

### 8. Multiple Conditions

Combine conditions with logical operators:

```python
age = 25
income = 50000

if age >= 18 and income >= 30000:
    print("Loan approved")

# Check membership
role = "admin"
if role in ["admin", "moderator"]:
    print("Access granted")
```

---

## Common Mistakes

### 1. Missing Colon

```python
# Wrong
if x > 0
    print("Positive")

# Correct
if x > 0:
    print("Positive")
```

### 2. Inconsistent Indentation

```python
# Wrong - mixing spaces
if x > 0:
    print("Positive")    # 4 spaces
     print("Yes")        # 5 spaces - ERROR!

# Correct
if x > 0:
    print("Positive")    # 4 spaces
    print("Yes")         # 4 spaces
```

### 3. Using `elif` Without `if`

```python
# Wrong
elif x > 0:    # Syntax error - elif without if!
    pass

# Correct
if x > 0:
    pass
elif x < 0:
    pass
```

### 4. Accidental Assignment in Condition

```python
# Wrong - assigns 5 to x, then checks if x is truthy
if x = 5:
    pass

# Correct
if x == 5:
    pass
```

### 5. Unnecessary Nested Ifs

```python
# Overly complex
if x > 0:
    if y > 0:
        print("Both positive")

# Simpler
if x > 0 and y > 0:
    print("Both positive")
```

### 6. Forgetting `else` for Edge Cases

```python
# Missing edge case handling
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
# What if score is 50? grade is undefined!

# Better
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"  # Handle all other cases
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. get_number_sign | Basic if-elif-else chain |
| 02. calculate_grade | Multiple elif conditions |
| 03. find_maximum | Nested if statements |
| 04. is_leap_year | Complex conditional logic |
| 05. categorize_age | Multiple condition checks |

---

## Quick Reference

```python
# Basic if
if condition:
    pass

# If-else
if condition:
    pass
else:
    pass

# If-elif-else
if condition1:
    pass
elif condition2:
    pass
else:
    pass

# Ternary
result = value_if_true if condition else value_if_false

# Check truthiness
if my_list:      # True if not empty
if my_string:    # True if not empty
if my_number:    # True if not zero
```

---

## Next Steps

After completing today's exercises:
1. Practice converting nested ifs to flat if-elif chains
2. Experiment with ternary expressions
3. Preview Day 10: **While Loops** - where you'll repeat code based on conditions
