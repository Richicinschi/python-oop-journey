# Day 2: Strings

## Overview

Today we dive deep into Python strings - one of the most commonly used data types. Understanding string manipulation is essential for text processing, data cleaning, parsing, and algorithmic problem solving.

## Learning Objectives

By the end of today, you will be able to:

- Create and manipulate strings using Python's rich string API
- Use indexing and slicing to extract substrings
- Apply string methods for searching, transforming, and validating text
- Understand string immutability and its implications
- Format strings using modern Python techniques (f-strings, `.format()`)
- Solve common string algorithm problems

## Key Concepts

### 1. String Basics

Strings in Python are sequences of Unicode characters. They can be created with single quotes, double quotes, or triple quotes for multiline strings.

```python
# Creating strings
single = 'Hello'
double = "World"
multiline = """This is a
multiline string"""

# String concatenation
greeting = single + " " + double  # "Hello World"

# String repetition
line = "-" * 10  # "----------"

# String length
length = len(greeting)  # 11
```

### 2. Indexing and Slicing

Strings are zero-indexed sequences. You can access individual characters and slices using bracket notation.

```python
text = "Python"

# Indexing (0-based)
text[0]   # 'P' (first character)
text[-1]  # 'n' (last character)
text[-2]  # 'o' (second to last)

# Slicing [start:stop:step]
text[0:2]    # 'Py' (characters at 0 and 1)
text[:2]     # 'Py' (from start to index 1)
text[2:]     # 'thon' (from index 2 to end)
text[::2]    # 'Pto' (every second character)
text[::-1]   # 'nohtyP' (reversed string)
```

**Key slicing rules:**
- `start` is inclusive, `stop` is exclusive
- Omitting `start` means "from the beginning"
- Omitting `stop` means "to the end"
- Negative indices count from the end (-1 is last)
- Negative step reverses the direction

### 3. Common String Methods

Python strings have numerous built-in methods for manipulation:

```python
text = "  Hello, World!  "

# Case operations
"hello".upper()      # "HELLO"
"HELLO".lower()      # "hello"
"hello world".title()  # "Hello World"

# Stripping whitespace
text.strip()         # "Hello, World!"
text.lstrip()        # "Hello, World!  "
text.rstrip()        # "  Hello, World!"

# Searching
"Hello".find("l")      # 2 (index of first 'l')
"Hello".rfind("l")     # 3 (index of last 'l')
"Hello".count("l")     # 2 (count of 'l')
"Hello" in "Hello World"  # True (membership test)

# Checking content
"123".isdigit()        # True
"abc".isalpha()        # True
"abc123".isalnum()     # True
" ".isspace()          # True
"hello".startswith("he")  # True
"hello".endswith("lo")    # True

# Replacement and splitting
"hello world".replace("world", "Python")  # "hello Python"
"a,b,c".split(",")     # ["a", "b", "c"]
"-".join(["a", "b", "c"])  # "a-b-c"
```

### 4. String Immutability

**Strings are immutable** in Python - they cannot be changed after creation. Any operation that modifies a string returns a new string.

```python
s = "hello"
# s[0] = "H"  # TypeError! Strings are immutable

# Instead, create a new string
s = "H" + s[1:]  # "Hello"

# Or use methods that return new strings
s = s.capitalize()  # "Hello"
```

**Why immutability matters:**
- Safe to use as dictionary keys
- Hashable (can be stored in sets)
- Thread-safe by design
- Allows string interning for memory efficiency

### 5. String Formatting

Modern Python offers several ways to format strings:

```python
name = "Alice"
age = 30

# f-strings (Python 3.6+) - RECOMMENDED
f"My name is {name} and I am {age} years old"

# Expressions inside f-strings
f"Next year I'll be {age + 1}"

# Format specifiers
f"Pi is approximately {3.14159:.2f}"  # "Pi is approximately 3.14"
f"Number: {42:05d}"  # "Number: 00042"

# .format() method (older but still useful)
"My name is {} and I am {} years old".format(name, age)
"My name is {0} and I am {1} years old".format(name, age)
"My name is {n} and I am {a} years old".format(n=name, a=age)

# % formatting (legacy, avoid in new code)
"My name is %s and I am %d years old" % (name, age)
```

### 6. Unicode and Encoding

Python 3 strings are Unicode by default, making international text handling straightforward.

```python
# Unicode characters are fully supported
emoji = "🐍"
japanese = "こんにちは"
chinese = "你好世界"

# Encoding/decoding for file I/O
text = "Hello"
bytes_data = text.encode("utf-8")  # b'Hello'
decoded = bytes_data.decode("utf-8")  # "Hello"
```

### 7. Raw Strings

Use raw strings (prefix with `r`) when you want backslashes treated literally - useful for regex patterns and Windows paths.

```python
# Regular string - backslash escapes
path = "C:\\Users\\name"  # Need to escape backslashes

# Raw string - backslashes are literal
path = r"C:\Users\name"  # Much cleaner!

# Common use case: regex patterns
import re
pattern = r"\d+"  # Matches one or more digits
```

## Common Mistakes

### 1. Modifying Strings In-Place

```python
# WRONG
s = "hello"
s[0] = "H"  # TypeError: 'str' object does not support item assignment

# CORRECT
s = "H" + s[1:]
# Or
s = s.capitalize()
```

### 2. Confusing `find()` vs `index()`

```python
text = "hello"

text.find("z")    # Returns -1 (not found)
text.index("z")   # Raises ValueError (not found)

# Use find() when "not found" is expected
# Use index() when "not found" should be an error
```

### 3. Mutable Default Arguments with Strings

```python
# This is a function default argument issue, not strings specifically
def add_prefix(s, prefix=""):  # OK - strings are immutable
    return prefix + s
```

### 4. Concatenating in Loops

```python
# INEFFICIENT (creates many intermediate strings)
result = ""
for char in "hello":
    result += char

# EFFICIENT (use join for multiple concatenations)
result = "".join(["h", "e", "l", "l", "o"])
```

### 5. Slice Out of Range Errors

```python
text = "hi"

# Python handles out-of-range slices gracefully
text[0:100]  # "hi" (no error, just returns what's available)

# But indexing raises IndexError
text[100]  # IndexError: string index out of range
```

### 6. Case-Sensitive Comparisons

```python
# WRONG for user input
if user_input == "yes":  # Won't match "YES" or "Yes"

# CORRECT
if user_input.lower() == "yes":
```

## Connection to Exercises

Today's exercises build string manipulation skills progressively:

| Exercise | Concepts Practiced |
|----------|-------------------|
| 01. Reverse String | Slicing `[::-1]`, string traversal |
| 02. Valid Palindrome | Two-pointer technique, `isalnum()`, case handling |
| 03. Anagram Check | Sorting strings, character counting |
| 04. First Unique Character | Hash map (dict), character frequency |
| 05. Longest Common Prefix | Horizontal/vertical scanning, `startswith()` |
| 06. Count and Say | String building, run-length encoding |
| 07. Longest Substring Without Repeating | Sliding window, set operations |
| 08. String Compression | String building, character counting |
| 09. Group Anagrams | Hash map, sorting as key |
| 10. Zigzag Conversion | String traversal patterns, list joining |
| 11. Longest Palindromic Substring | Expand around center, dynamic programming |

## Key Takeaways

1. **Master slicing** - It's Pythonic and efficient for substring operations
2. **Remember immutability** - Every "modification" creates a new string
3. **Use f-strings** - They're readable, fast, and expressive
4. **Leverage built-in methods** - Python's string methods are optimized in C
5. **Think about algorithms** - String problems often use sliding window, two-pointers, or hashing

## Further Reading

- [Python String Methods Documentation](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- f-string formatting: [PEP 498](https://peps.python.org/pep-0498/)

## Time Estimate

- Reading: 20-30 minutes
- Exercises: 2-3 hours
- Review: 20 minutes
