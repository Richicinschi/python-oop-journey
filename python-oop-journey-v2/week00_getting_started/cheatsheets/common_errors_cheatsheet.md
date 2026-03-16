# Common Python Errors Cheatsheet

A guide to understanding, fixing, and preventing common Python errors for beginners.

---

## Syntax Errors

### IndentationError

**What it means:** Python expects consistent indentation (usually 4 spaces).

```python
# ❌ WRONG - Inconsistent indentation
def my_function():
print("Hello")      # IndentationError!

# ✅ CORRECT
def my_function():
    print("Hello")
```

**Common causes:**
- Mixing tabs and spaces
- Wrong number of spaces
- Forgetting to indent after `:`

**Prevention:**
- Configure editor to use spaces (not tabs)
- Set tab size to 4 spaces in VS Code
- Enable "render whitespace" to see hidden characters

---

### SyntaxError: invalid syntax

**What it means:** Python can't understand the code structure.

```python
# ❌ WRONG - Missing colon
if x == 5
    print("Five")

# ✅ CORRECT
if x == 5:
    print("Five")

# ❌ WRONG - Using = instead of ==
if x = 5:           # SyntaxError!
    print("Five")

# ✅ CORRECT
if x == 5:
    print("Five")
```

**Common causes:**
- Missing colons (`:`) after `if`, `for`, `while`, `def`, `class`
- Using `=` (assignment) instead of `==` (comparison)
- Mismatched parentheses, brackets, or quotes
- Invalid characters

---

## Name Errors

### NameError: name 'x' is not defined

**What it means:** You're using a variable that doesn't exist.

```python
# ❌ WRONG - Using before defining
print(message)
message = "Hello"

# ✅ CORRECT
message = "Hello"
print(message)

# ❌ WRONG - Typo in variable name
my_variable = 10
print(my_varible)   # NameError!

# ✅ CORRECT
my_variable = 10
print(my_variable)
```

**Common causes:**
- Using a variable before assigning it
- Typos in variable names
- Variable defined in a different scope
- Forgot to import a module

**Prevention:**
- Use descriptive variable names
- Check for typos carefully
- Initialize variables at the top of functions

---

## Type Errors

### TypeError: unsupported operand type(s)

**What it means:** You're trying to do an operation with incompatible types.

```python
# ❌ WRONG - Adding string and number
age = 25
message = "I am " + age + " years old"  # TypeError!

# ✅ CORRECT - Convert to string
age = 25
message = "I am " + str(age) + " years old"

# ✅ BETTER - Use f-string
message = f"I am {age} years old"

# ❌ WRONG - Wrong number of arguments
def greet(name):
    print(f"Hello, {name}!")

greet()             # TypeError!
greet("Alice", "Bob")  # TypeError!

# ✅ CORRECT
greet("Alice")
```

**Common causes:**
- Concatenating strings with numbers
- Passing wrong number of arguments
- Calling a non-callable object
- Using wrong type for an operation

---

### TypeError: 'NoneType' object is not callable/subscriptable

**What it means:** A function returned `None` but you're trying to use it.

```python
# ❌ WRONG - Forgetting to return
add(2, 3)

def add(a, b):
    result = a + b
    # Forgot return!

# ✅ CORRECT
def add(a, b):
    return a + b

total = add(2, 3)   # total is 5
```

---

## Index Errors

### IndexError: list index out of range

**What it means:** You're trying to access an element that doesn't exist.

```python
# ❌ WRONG - Index beyond list
fruits = ["apple", "banana"]
print(fruits[2])    # IndexError! Valid: 0, 1

# ✅ CORRECT
print(fruits[0])    # "apple"
print(fruits[1])    # "banana"
print(fruits[-1])   # "banana" (last item)

# ❌ WRONG - Empty list
items = []
print(items[0])     # IndexError!

# ✅ CORRECT - Check length first
if len(items) > 0:
    print(items[0])
# OR
if items:           # Empty list is falsy
    print(items[0])
```

**Prevention:**
- Check length before indexing: `if index < len(my_list)`
- Use `-1` for last item instead of calculating length
- Use `.get()` for dictionaries
- Use `try/except` for uncertain access

---

### KeyError

**What it means:** Dictionary doesn't have that key.

```python
# ❌ WRONG - Accessing missing key
person = {"name": "Alice"}
print(person["age"])    # KeyError!

# ✅ CORRECT - Use .get()
age = person.get("age")     # Returns None
age = person.get("age", 0)  # Returns 0 if missing

# ✅ CORRECT - Check first
if "age" in person:
    print(person["age"])
```

---

## Attribute Errors

### AttributeError: 'type' object has no attribute 'x'

**What it means:** You're trying to use a method/attribute that doesn't exist.

```python
# ❌ WRONG - Wrong method name
my_list = [1, 2, 3]
my_list.add(4)      # AttributeError! Lists use append()

# ✅ CORRECT
my_list.append(4)

# ❌ WRONG - Calling method on wrong type
text = "hello"
text.append("!")     # AttributeError! Strings are immutable

# ✅ CORRECT
text = text + "!"
```

**Prevention:**
- Check available methods with `dir(object)`
- Use `help(list)` to see documentation
- Remember: strings and tuples are immutable

---

## Value Errors

### ValueError: invalid literal for int()

**What it means:** Can't convert a string to a number.

```python
# ❌ WRONG - Not a number
number = int("hello")   # ValueError!
number = int("3.14")    # ValueError! (use float first)

# ✅ CORRECT
number = int("42")      # 42
number = int(float("3.14"))  # 3

# ✅ SAFE - With validation
user_input = input("Enter a number: ")
if user_input.isdigit():
    number = int(user_input)
else:
    print("That's not a valid number!")
```

---

### ValueError: too many values to unpack

**What it means:** Number of variables doesn't match number of values.

```python
# ❌ WRONG - Mismatch
a, b = [1, 2, 3]    # ValueError!

# ✅ CORRECT
a, b, c = [1, 2, 3]

# ✅ CORRECT - Use * for remaining
a, *rest = [1, 2, 3]  # a=1, rest=[2,3]
```

---

## Common Logic Errors

### Infinite Loops

```python
# ❌ WRONG - Never updates condition
x = 0
while x < 10:
    print(x)    # Infinite loop! x never changes

# ✅ CORRECT
x = 0
while x < 10:
    print(x)
    x += 1      # Don't forget to update!
```

---

### Modifying List While Iterating

```python
# ❌ WRONG - Modifying while iterating
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)   # Unexpected behavior!

# ✅ CORRECT - Create new list
evens = [n for n in numbers if n % 2 == 0]

# ✅ CORRECT - Iterate over copy
for n in numbers[:]:
    if n % 2 == 0:
        numbers.remove(n)
```

---

### Integer Division Gotcha

```python
# In Python 2, 5 / 2 = 2
# In Python 3:

result = 5 / 2      # 2.5 (always float)
result = 5 // 2     # 2 (floor division)
```

---

## Error Handling Pattern

```python
# Basic try/except
try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")
else:
    print(f"Result: {result}")  # Runs if no exception
finally:
    print("Done!")              # Always runs
```

---

## Quick Reference: Error Types

| Error | When It Happens | Quick Fix |
|-------|-----------------|-----------|
| `SyntaxError` | Invalid Python code | Check colons, quotes, indentation |
| `IndentationError` | Wrong indentation | Use 4 spaces consistently |
| `NameError` | Variable not defined | Define before use, check spelling |
| `TypeError` | Wrong types for operation | Check types with `type()` |
| `IndexError` | List index too big | Check `len()` first |
| `KeyError` | Missing dictionary key | Use `.get()` or check with `in` |
| `AttributeError` | Method doesn't exist | Check with `dir()` |
| `ValueError` | Invalid value conversion | Validate before converting |
| `ZeroDivisionError` | Dividing by zero | Check if divisor is 0 |

---

## Debugging Tips

1. **Read the error message carefully** - it tells you line number and type
2. **Use `print()`** to check variable values
3. **Use `type()`** to verify variable types
4. **Use `dir()`** to see available methods
5. **Use `help()`** to read documentation
6. **Test in small pieces** - isolate the problem
7. **Use a debugger** - set breakpoints in VS Code

---

## Prevention Checklist

- [ ] Initialize all variables before use
- [ ] Check lengths before indexing
- [ ] Validate user input
- [ ] Use `.get()` for dictionary access
- [ ] Test edge cases (empty lists, zero, etc.)
- [ ] Use f-strings instead of string concatenation
- [ ] Keep functions small and focused
- [ ] Write test cases for your code
