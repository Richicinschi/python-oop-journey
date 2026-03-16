# Day 24: Understanding Errors

## Learning Objectives

By the end of this day, you will be able to:

1. Distinguish between syntax errors and runtime errors
2. Read and interpret Python tracebacks
3. Understand common error types and their causes
4. Recognize error messages as helpful debugging tools

---

## Key Concepts

### 1. What Are Errors?

Errors (also called **exceptions**) are Python's way of telling you that something went wrong. Don't fear errors—they're actually helpful messages designed to guide you to the problem!

Think of errors like a helpful friend who points out when you've made a mistake:
- They tell you **what** went wrong
- They tell you **where** it happened
- They often suggest **why** it happened

---

### 2. Syntax Errors

**Syntax errors** occur when Python cannot understand your code because it breaks the language rules. These are caught before the program runs.

```python
# Syntax Error: Missing closing parenthesis
print("Hello World"

# Syntax Error: Invalid indentation
def greet():
print("Hi")  # Should be indented

# Syntax Error: Missing colon
if x > 5
    print("Big")
```

**Key characteristics:**
- Python cannot run the program at all
- The error message points to the approximate location
- Usually the easiest errors to fix

---

### 3. Runtime Errors

**Runtime errors** (exceptions) occur while the program is running. The syntax is correct, but something unexpected happens during execution.

```python
# ZeroDivisionError
result = 10 / 0

# TypeError
length = len(42)  # len() works on sequences, not numbers

# NameError
print(undefined_variable)

# IndexError
my_list = [1, 2, 3]
print(my_list[10])  # Index 10 doesn't exist
```

**Key characteristics:**
- Program starts running but crashes mid-execution
- Happen due to invalid operations or unexpected data
- Can occur in code that usually works (e.g., user input)

---

### 4. Reading Tracebacks

When Python encounters an error, it prints a **traceback** (stack trace). This is like a detective's report showing exactly what happened.

```
Traceback (most recent call last):
  File "example.py", line 7, in <module>
    result = divide(10, 0)
  File "example.py", line 4, in divide
    return a / b
ZeroDivisionError: division by zero
```

**How to read a traceback (bottom to top):**

1. **Bottom line**: The error type and message
   ```
   ZeroDivisionError: division by zero
   ```
   This tells you exactly what went wrong.

2. **The lines above**: The chain of function calls
   ```
   File "example.py", line 4, in divide
       return a / b
   ```
   This shows where in your code the error occurred.

3. **The top**: Where execution started
   ```
   File "example.py", line 7, in <module>
       result = divide(10, 0)
   ```
   This shows the original call that led to the error.

**Pro tip**: Always read tracebacks from the **bottom up**!

---

### 5. Common Error Types

| Error Type | Meaning | Example |
|------------|---------|---------|
| `SyntaxError` | Code doesn't follow Python rules | `print("hi"` |
| `IndentationError` | Wrong indentation | Missing spaces after `def` |
| `NameError` | Variable doesn't exist | `print(x)` when x not defined |
| `TypeError` | Wrong type used | `len(5)` or `"2" + 2` |
| `ValueError` | Right type, wrong value | `int("hello")` |
| `IndexError` | List index out of range | `[1,2][5]` |
| `KeyError` | Dictionary key not found | `{"a":1}["b"]` |
| `ZeroDivisionError` | Division by zero | `10 / 0` |
| `AttributeError` | Object lacks the attribute | `"hello".nonexistent()` |
| `ImportError` | Can't import module | `import nonexistent` |

---

### 6. Errors as Learning Tools

Beginners often see errors as failures. Experienced programmers see them as helpful guides!

**Before you fix an error:**
1. Read the error message carefully
2. Look at the line number it points to
3. Check the lines immediately before (the real error might be there)
4. Understand what the error type means
5. Fix one error at a time

---

## Practice Approach

When you encounter an error:

1. **Don't panic**—errors are normal!
2. **Read the message** slowly
3. **Find the line** mentioned in the traceback
4. **Understand the error type** using this day's material
5. **Fix and test** your solution

---

## Common Beginner Mistakes

1. **Reading tracebacks top-to-bottom** → Read from the bottom!
2. **Ignoring the error message** → The message often tells you exactly how to fix it
3. **Changing multiple things at once** → Fix one error, then test
4. **Not looking at the line before** → Sometimes the error is on the previous line

## Connection to Project

Understanding errors helps you debug your Todo List app. Common errors you might see:

| Error | When It Happens | Fix |
|-------|-----------------|-----|
| `FileNotFoundError` | tasks.json doesn't exist yet | Check if file exists before reading |
| `KeyError` | Accessing non-existent task field | Use `.get()` or validate data |
| `ValueError` | Invalid user input | Validate input before processing |
| `IndexError` | Invalid task number selected | Check bounds before accessing list |

---

## Next Steps

Tomorrow we'll learn how to **handle** errors gracefully using `try` and `except`—a powerful tool that lets your program recover from errors instead of crashing.

**Next**: [Day 25: Try and Except](./day25_try_except.md)
