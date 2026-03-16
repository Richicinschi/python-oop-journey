# 📚 Week 0: Interactive Jupyter Notebooks

Welcome to the **Week 0 Getting Started** interactive notebooks! These notebooks are designed to help you learn Python fundamentals in a hands-on, interactive way.

---

## 🚀 Quick Start

### Prerequisites

Make sure you have Jupyter installed:

```bash
# If you don't have Jupyter installed
pip install jupyter

# Or if you have the project requirements
pip install -r ../../requirements.txt
```

### Launching Jupyter

From this directory (`week00_getting_started/notebooks/`), run:

```bash
jupyter notebook
```

Or use JupyterLab for a more modern interface:

```bash
jupyter lab
```

---

## 📓 Notebook Guide

### Beginner Track (Recommended Order)

| Order | Notebook | Topics | Duration |
|-------|----------|--------|----------|
| 1 | `00_getting_started.ipynb` | Introduction, first code, variables | 20 min |
| 2 | `01_python_basics_walkthrough.ipynb` | Types, operators, strings | 30 min |
| 3 | `02_control_flow_walkthrough.ipynb` | If/else, loops | 35 min |
| 4 | `03_collections_walkthrough.ipynb` | Lists, dicts, tuples, sets | 40 min |
| 5 | `04_functions_walkthrough.ipynb` | Functions, scope, lambdas | 35 min |

**Total estimated time:** ~2.5 hours

---

## 🎯 How to Use These Notebooks

### Running Code Cells

1. **Click** on a code cell (gray box with code)
2. **Press** `Shift + Enter` to run it
3. **Or click** the ▶️ play button on the left

### Cell Types

- **Code cells** (gray): Contain Python code you can run
- **Markdown cells** (white): Contain explanations and instructions

### Interactive Features

Each notebook includes:

- ✅ **Live code examples** - Run them and see results instantly
- ✅ **Exercises** - Practice what you learned (marked with `TODO`)
- ✅ **Solutions** - Hidden solutions (in HTML comments) if you get stuck
- ✅ **Visual diagrams** - ASCII art to help visualize concepts
- ✅ **Experiment zones** - Free space to try your own code

### Tips for Success

1. **Don't just read** - Run every code cell!
2. **Experiment** - Change values and see what happens
3. **Make mistakes** - Errors are learning opportunities
4. **Take breaks** - Learning is a marathon, not a sprint
5. **Have fun** - Programming is creative and rewarding!

---

## 🔍 Notebook Contents

### 00_getting_started.ipynb
**Welcome to Python!**

- What is a Jupyter Notebook?
- Your first Python program
- Using Python as a calculator
- Understanding comments
- Variables and data storage
- Dealing with errors (don't worry, they're normal!)

**By the end:** You'll write and run your first Python code!

---

### 01_python_basics_walkthrough.ipynb
**Variables, Types, and Operators**

- Data types (str, int, float, bool)
- String manipulation and f-strings
- Arithmetic operators (+, -, *, /, //, %, **)
- Comparison operators (==, !=, <, >, <=, >=)
- Assignment operators (+=, -=, etc.)
- Type conversion

**By the end:** You'll work confidently with Python's basic data types!

---

### 02_control_flow_walkthrough.ipynb
**Making Decisions and Repeating Actions**

- If, elif, else statements
- For loops and the `range()` function
- While loops
- Loop control (break, continue)
- Nested structures
- Tracing execution flow

**By the end:** You'll control how your programs make decisions and repeat tasks!

---

### 03_collections_walkthrough.ipynb
**Lists, Dictionaries, Sets, and Tuples**

- Lists: ordered, mutable collections
- Dictionaries: key-value pairs
- Tuples: immutable sequences
- Sets: unique collections
- Iterating over collections
- List and dictionary comprehensions

**By the end:** You'll organize and manipulate data efficiently!

---

### 04_functions_walkthrough.ipynb
**Writing Reusable Code**

- Defining functions with `def`
- Parameters and return values
- Default parameters
- Variable scope (local vs global)
- *args and **kwargs
- Lambda functions
- Docstrings and documentation

**By the end:** You'll write modular, reusable, well-documented code!

---

## 💡 Learning Tips

### For Absolute Beginners

1. Start with `00_getting_started.ipynb`
2. Go slowly - don't rush
3. Run every code cell
4. Try the exercises before looking at solutions
5. It's okay to not understand everything immediately

### For Those with Some Experience

1. You might move through `00` and `01` quickly
2. Focus on Python-specific features (f-strings, comprehensions)
3. Pay attention to the exercises - they may challenge you!
4. Use the notebooks as a reference

### For Everyone

- **Practice daily** - Even 15 minutes is better than nothing
- **Type the code** - Don't just copy-paste
- **Break things** - See what errors you get
- **Ask questions** - If something doesn't make sense, investigate!

---

## 🎓 Exercises and Solutions

### Exercise Format

Exercises look like this:

```python
# TODO: Write code to do X
# Hint: Try using Y

# Your code here:

```

### Viewing Solutions

Solutions are hidden in HTML comments. To view them:

1. **In edit mode**: Double-click a markdown cell to see the raw text
2. **Look for**:
   ```html
   <!-- SOLUTION START -->
   <!-- 
   solution code here
   -->
   <!-- SOLUTION END -->
   ```
3. **Try first!** Only look after attempting the exercise yourself

---

## 🛠️ Troubleshooting

### Jupyter Won't Start

```bash
# Check if jupyter is installed
jupyter --version

# If not, install it
pip install jupyter

# Or upgrade
pip install --upgrade jupyter
```

### Code Won't Run

1. Make sure the cell is selected (has a blue/green bar on left)
2. Press `Shift + Enter` (not just Enter)
3. Check for syntax errors

### Kernel Dies

```python
# In the menu: Kernel → Restart
# Then run cells again from the top
```

### Import Errors

```bash
# Make sure you're in the right directory
# Or install missing packages
pip install package_name
```

---

## 📖 Additional Resources

### Within This Course

- `../day00_welcome.md` - Welcome message and course overview
- `../exercises/` - Additional practice problems
- `../solutions/` - Solution files for exercises

### External Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)
- [Python Tutor (Visualize Code)](https://pythontutor.com/)

---

## ✅ Progress Checklist

Track your progress through the notebooks:

- [ ] `00_getting_started.ipynb` - Introduction
- [ ] `01_python_basics_walkthrough.ipynb` - Variables & Types
- [ ] `02_control_flow_walkthrough.ipynb` - Loops & Conditionals
- [ ] `03_collections_walkthrough.ipynb` - Lists & Dictionaries
- [ ] `04_functions_walkthrough.ipynb` - Functions

Once you've completed all notebooks, you're ready for **Week 1: Object-Oriented Fundamentals**!

---

## 🤝 Getting Help

### If You're Stuck

1. **Re-read the explanation** - Sometimes a second read helps
2. **Look at the examples** - They show the pattern
3. **Try a simpler version** - Break the problem down
4. **Check the hint** - Often points you in the right direction
5. **Look at the solution** - It's okay to peek!

### Remember

> "The expert in anything was once a beginner."\n> — Helen Hayes

Everyone struggles at first. Keep going!

---

## 🎉 Have Fun!

Learning to program is like learning a new language or a musical instrument. It takes practice, but it's incredibly rewarding. Enjoy the journey!

**Happy Coding! 🐍✨**
