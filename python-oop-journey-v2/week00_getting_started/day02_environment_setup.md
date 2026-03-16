# Day 02: Setting Up Your Environment

## Learning Objectives

By the end of this day, you will be able to:

1. Explain what an IDE is and why it helps
2. Install and configure Visual Studio Code
3. Install Python extensions for VS Code
4. Use basic terminal commands (cd, ls/dir, pwd)
5. Create, save, and run a Python file
6. Connect VS Code to your Python installation

---

## What You Will Learn
- What an IDE is and why you need one
- How to install and configure Visual Studio Code
- How to install Python extensions for VS Code
- Basic terminal/command line usage
- How to create and run your first Python file

---

## What is an IDE?

An **IDE** (Integrated Development Environment) is a program that helps you write code. Think of it like Microsoft Word, but for programming:

| Feature | What It Does | Why It Helps |
|---------|--------------|--------------|
| **Syntax Highlighting** | Colors code based on meaning | Easier to read and spot errors |
| **Auto-completion** | Suggests code as you type | Faster coding, fewer typos |
| **Error Detection** | Underlines mistakes | Catch errors before running |
| **Integrated Terminal** | Run commands inside the editor | No need to switch windows |
| **Debugger** | Step through code line by line | Find and fix bugs easier |

While you can write Python in any text editor (like Notepad), an IDE makes learning much easier.

---

## Installing Visual Studio Code

### What is VS Code?

**Visual Studio Code** (VS Code) is a free, lightweight code editor made by Microsoft. It's:
- Free and open source
- Works on Windows, Mac, and Linux
- Has thousands of extensions
- Used by millions of programmers

### Installation Steps

#### Step 1: Download VS Code
1. Go to [https://code.visualstudio.com](https://code.visualstudio.com)
2. Click the download button for your operating system
3. Save the installer file

#### Step 2: Run the Installer

**Windows:**
1. Double-click the downloaded `.exe` file
2. Accept the license agreement
3. Click "Next" through the installation
4. **IMPORTANT**: Check these boxes:
   - ☑ "Add to PATH"
   - ☑ "Add 'Open with Code' action to Windows Explorer"
5. Click "Install"

**Mac:**
1. Open the downloaded `.zip` file
2. Drag "Visual Studio Code" to your Applications folder
3. Open from Applications (you may need to right-click and select "Open" the first time)

**Linux:**
- Ubuntu/Debian: Download `.deb` and run `sudo dpkg -i filename.deb`
- Fedora: Download `.rpm` and run `sudo rpm -i filename.rpm`
- Or use your software center

---

## Installing Python Extensions

VS Code becomes powerful for Python when you install extensions.

### Step 1: Open Extensions View
- Click the Extensions icon on the left sidebar (looks like four squares)
- Or press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)

### Step 2: Install Python Extension
1. Type "Python" in the search box
2. Find the extension by **Microsoft** (it has millions of downloads)
3. Click **"Install"**

This extension provides:
- Python syntax highlighting
- Code suggestions (IntelliSense)
- Error detection
- Debugging support
- Test runner integration

### Step 3: Install Additional Helpful Extensions

While not required, these extensions are helpful:

| Extension | Purpose |
|-----------|---------|
| **Pylance** | Better Python code analysis (usually auto-installed) |
| **Python Indent** | Auto-fixes indentation |
| **Error Lens** | Shows errors inline |

---

## Configuring VS Code

### Setting Your Python Interpreter

VS Code needs to know which Python to use.

1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Python: Select Interpreter"
3. Choose the Python version you installed (should be 3.8+)

### Recommended Settings

Open settings (`Ctrl+,` or `Cmd+,`) and search for these:

```
Editor: Font Size → 14 (or your preference)
Editor: Tab Size → 4 (standard for Python)
Editor: Insert Spaces → true (Python uses spaces, not tabs)
```

---

## Basic Terminal Usage

The **terminal** (or command line) is where you run commands to interact with your computer.

### Opening the Terminal in VS Code

- **Menu**: Terminal → New Terminal
- **Shortcut**: `` Ctrl+` `` (backtick key, usually under Esc)

### Essential Commands

| Command | Windows | Mac/Linux | What It Does |
|---------|---------|-----------|--------------|
| Current directory | `cd` | `pwd` | Show where you are |
| List files | `dir` | `ls` | Show files in current folder |
| Change directory | `cd foldername` | `cd foldername` | Move into a folder |
| Go up one folder | `cd ..` | `cd ..` | Move to parent folder |
| Clear screen | `cls` | `clear` | Clean the terminal |

### Practice: Navigate to Your Project

1. Open VS Code terminal
2. Create a folder for your learning:
   ```bash
   # Windows
   mkdir C:\Users\%USERNAME%\python-learning
   cd C:\Users\%USERNAME%\python-learning
   
   # Mac/Linux
   mkdir ~/python-learning
   cd ~/python-learning
   ```

---

## Creating Your First Python File

Let's create and run a simple Python file!

### Step 1: Create a New File
1. In VS Code, click **File → New File**
2. Save it as `first_program.py`:
   - Press `Ctrl+S` (or `Cmd+S` on Mac)
   - Navigate to your `python-learning` folder
   - Name it `first_program.py`
   - Make sure it ends with `.py`!

### Step 2: Write Some Code

Type this into the file:

```python
# This is my first Python program!

name = "Learner"
age = 1  # This represents day 1 of learning

print(f"Hello, {name}!")
print(f"You are {age} day(s) into your Python journey.")
print("Welcome to the world of programming!")
```

### Step 3: Run the Program

**Option 1: Using the Play Button**
- Look for the ▶️ play button in the top right corner
- Click it to run your program

**Option 2: Using the Terminal**
```bash
# Make sure you're in the right folder
python first_program.py
```

**Expected Output:**
```
Hello, Learner!
You are 1 day(s) into your Python journey.
Welcome to the world of programming!
```

🎉 **Congratulations!** You just ran your first Python program!

---

## Exercises for Today

Complete these exercises to practice:

1. **Create `greeting.py`**
   - Create a file that prints a personalized greeting
   - Use your own name in the variable

2. **Create `calculator.py`**
   - Create variables for two numbers
   - Print their sum, difference, product, and quotient

3. **Experiment**
   - Try changing the code
   - See what happens when you make mistakes
   - Don't worry about breaking anything!

## Connection to Exercises

| Exercise | Skills Practiced |
|----------|------------------|
| greeting.py | Creating Python files, variables, print() |
| calculator.py | Variables, basic arithmetic, multiple print statements |

Exercise files are provided in [day02_exercises/](./day02_exercises/)

## Connection to Weekly Project

Setting up your environment correctly is essential for the Todo CLI project. You'll use VS Code to:
- Edit Python files with syntax highlighting
- Run and test your code
- Debug issues when they arise

---

## Troubleshooting

### "Python is not recognized"

**Windows**: Close VS Code and reopen it after installing Python

**Mac**: Use `python3` instead of `python` in the terminal

### "No Python interpreter selected"

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your Python installation

### Extensions won't install

- Check your internet connection
- Make sure VS Code is up to date
- Try restarting VS Code

---

## Summary Checklist

- [ ] Downloaded and installed VS Code
- [ ] Installed the Python extension by Microsoft
- [ ] Selected Python interpreter in VS Code
- [ ] Opened the integrated terminal
- [ ] Created a folder for learning
- [ ] Created and ran `first_program.py`
- [ ] Saw the expected output

---

## What's Next?

Tomorrow, we'll dive deeper into writing Python programs. You'll learn about:
- The `print()` function in detail
- Comments (notes in your code)
- Basic program structure

**Next**: [Day 03: Your First Python Program](./day03_first_program.md)

---

## Quick Reference

### VS Code Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Save file | `Ctrl+S` | `Cmd+S` |
| Open terminal | `` Ctrl+` `` | `` Cmd+` `` |
| Command palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Run Python file | Right-click → "Run" | Right-click → "Run" |

### File Extensions

| Extension | File Type |
|-----------|-----------|
| `.py` | Python file |
| `.txt` | Text file |
| `.md` | Markdown file (like this document) |
