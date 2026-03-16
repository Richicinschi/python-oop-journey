# Day 27: Debugging Basics

## Learning Objectives

By the end of this day, you will be able to:

1. Use print debugging effectively to understand program flow
2. Read and interpret error messages and tracebacks
3. Apply systematic debugging strategies
4. Understand the basics of IDE debuggers (breakpoints, step-through)

---

## Key Concepts

### 1. What is Debugging?

**Debugging** is the process of finding and fixing errors (bugs) in your code. The term originated from a literal moth found in a computer in 1947!

Good debugging skills separate beginners from experienced programmers. It's not about being smart—it's about being systematic.

---

### 2. Print Debugging (The Beginner's Best Friend)

Print debugging is simple but powerful. Add `print()` statements to see what your code is doing.

```python
def calculate_discount(price, discount_percent):
    print(f"Input: price={price}, discount={discount_percent}")  # Debug
    
    discount = price * discount_percent / 100
    print(f"Calculated discount: {discount}")  # Debug
    
    final_price = price - discount
    print(f"Final price: {final_price}")  # Debug
    
    return final_price
```

**When to use print debugging:**
- Quick checks of variable values
- Understanding program flow
- Checking if a function is being called
- Verifying loop iterations

**Tips for effective print debugging:**
```python
# Label your debug prints clearly
print(f"DEBUG: After loop, total={total}")

# Print data types when confused
print(f"DEBUG: value={value}, type={type(value)}")

# Show iteration info
for i, item in enumerate(items):
    print(f"DEBUG: i={i}, item={item}")
    # ... rest of code
```

---

### 3. Reading Error Messages (The Traceback)

When Python crashes, it shows a **traceback**. Learning to read it is essential.

```
Traceback (most recent call last):
  File "program.py", line 10, in <module>
    result = calculate_average(numbers)
  File "program.py", line 5, in calculate_average
    return sum(numbers) / len(numbers)
ZeroDivisionError: division by zero
```

**How to read it:**
1. **Start at the bottom** - This shows the actual error
2. **Read the message** - "division by zero" tells you what happened
3. **Look up for the location** - Line 5 in `calculate_average`
4. **Trace the call stack** - See what led to the error

---

### 4. The Debugging Process

Follow a systematic approach:

```
1. REPRODUCE the bug
   ↓ Can you make it happen consistently?
   
2. LOCATE the problem
   ↓ Where in the code does it occur?
   
3. UNDERSTAND the cause
   ↓ Why is it happening?
   
4. FIX the code
   ↓ Make the minimal change needed
   
5. VERIFY the fix
   ↓ Test that it works
```

---

### 5. Common Debugging Strategies

**Strategy 1: Binary Search**
If you have 100 lines and don't know where the bug is:
- Put a print in the middle (line 50)
- Check if the bug has occurred by that point
- Repeat in the half that contains the bug

**Strategy 2: Work Backwards**
- Look at the error message
- Find the line that failed
- Check what values led to that failure
- Trace backwards to the source

**Strategy 3: Rubber Duck Debugging**
- Explain your code out loud (or to a rubber duck)
- Often you'll spot the problem while explaining
- Forces you to think through each step

---

### 6. Common Beginner Bugs

| Bug | Example | Fix |
|-----|---------|-----|
| Off-by-one | `range(5)` gives 0-4 | Remember: start inclusive, end exclusive |
| String vs Number | `"5" + 5` | Convert: `int("5") + 5` |
| Mutable default | `def f(x=[])` | Use `def f(x=None)` |
| Assignment vs Compare | `if x = 5:` | Use `==` for comparison |
| Indentation | Mixing tabs and spaces | Use spaces consistently |
| Case sensitivity | `my_var` vs `My_Var` | Be consistent with naming |
| Modifying while iterating | `for x in list: list.remove(x)` | Iterate over a copy |

---

### 7. IDE Debugger Basics

Modern IDEs (VS Code, PyCharm) have built-in debuggers:

**Key Concepts:**
- **Breakpoint**: A line where execution pauses
- **Step Over**: Execute current line, move to next
- **Step Into**: Enter a function call
- **Step Out**: Finish current function, return to caller
- **Continue**: Run until next breakpoint

**How to use a debugger:**
1. Set a breakpoint where you want to start investigating
2. Run in debug mode
3. When execution pauses, inspect variables
4. Step through code line by line
5. Watch how values change

**Simple example in VS Code:**
```python
def calculate_sum(numbers):  # ← Set breakpoint here
    total = 0
    for n in numbers:
        total += n  # ← Step through this loop
    return total
```

---

### 8. Debugging Checklist

When your code doesn't work:

- [ ] Read the error message carefully
- [ ] Check the line number in the traceback
- [ ] Look at the lines immediately before the error
- [ ] Add print statements to see variable values
- [ ] Check data types with `type()`
- [ ] Verify function inputs and outputs
- [ ] Test with simple, known inputs
- [ ] Comment out code to isolate the problem
- [ ] Check for typos in variable names
- [ ] Verify indentation is correct

---

## Best Practices

1. **Remove or disable debug prints** before committing code
2. **Use descriptive labels** in debug output
3. **Test one change at a time**
4. **Write tests** to prevent regression
5. **Document tricky fixes** with comments

---

## Summary

Debugging is a skill that improves with practice. Remember:

- Errors are helpful messages, not failures
- Be systematic in your approach
- Use print debugging to understand what's happening
- Read tracebacks from the bottom up
- Don't guess—verify with evidence

---

## Connection to Project

Debugging skills are essential for the final project. When your Todo List app isn't working:

1. Use `print()` to trace data flow between functions
2. Check the error traceback - it points directly to the problem
3. Verify file I/O operations are working with debug output
4. Test each module independently before integrating

Remember: every bug you fix makes you a better programmer!

---

## Next Steps

Congratulations! You've completed Week 0: Getting Started. You're now ready to move on to Week 1 where you'll dive into Object-Oriented Programming fundamentals.

**Next**: Week 1 - Object-Oriented Fundamentals
