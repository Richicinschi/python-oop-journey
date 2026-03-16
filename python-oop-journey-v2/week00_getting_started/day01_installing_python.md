# Day 01: Installing Python

## Learning Objectives

By the end of this day, you will be able to:

1. Explain how Python works (interpreter model)
2. Install Python 3.8+ on your operating system
3. Verify your Python installation works
4. Use basic Python terminology: interpreter, version, pip
5. Run Python code in interactive mode

---

## What You Will Learn
- What Python is and how it works
- How to install Python on Windows, Mac, or Linux
- How to verify your installation
- Basic terminology: interpreter, version, environment

---

## What is Python?

Python is a **programming language**—a way for humans to write instructions that computers can understand.

### How Python Works

```
You Write Python Code → Python Interpreter → Computer Executes
     (human readable)      (translator)        (machine code)
```

The **Python interpreter** is a program that reads your Python code and translates it into instructions for your computer.

### Why Python 3?

Python has versions, like software updates:
- **Python 2** (old, no longer supported)
- **Python 3** (current, what we use)

Always use **Python 3.8 or newer**. We'll be using Python 3.10+ features in this course.

---

## Installation by Operating System

### Windows Installation

#### Step 1: Download Python
1. Go to [https://python.org/downloads](https://python.org/downloads)
2. Click the yellow **"Download Python 3.x.x"** button
3. Save the installer file (it will be named something like `python-3.12.0-amd64.exe`)

#### Step 2: Run the Installer
1. Double-click the downloaded file
2. **IMPORTANT**: Check the box that says **"Add Python to PATH"**
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"**

#### Step 3: Verify Installation
1. Press `Win + R` to open the Run dialog
2. Type `cmd` and press Enter
3. In the black window (Command Prompt), type:
   ```
   python --version
   ```
4. You should see something like:
   ```
   Python 3.12.0
   ```

If you see an error like "'python' is not recognized," try:
```
py --version
```

---

### macOS Installation

#### Option 1: Official Installer (Recommended for Beginners)
1. Go to [https://python.org/downloads](https://python.org/downloads)
2. Click the **"Download Python 3.x.x"** button
3. Open the downloaded `.pkg` file
4. Follow the installation wizard
5. Enter your password when prompted

#### Option 2: Using Homebrew (For advanced users)
If you have Homebrew installed:
```bash
brew install python
```

#### Verify Installation
1. Open Terminal (Press `Cmd + Space`, type "Terminal", press Enter)
2. Type:
   ```bash
   python3 --version
   ```
3. You should see:
   ```
   Python 3.12.0
   ```

**Note**: On Mac, you must use `python3` not `python` (without the 3).

---

### Linux Installation

Most Linux distributions come with Python pre-installed.

#### Check if Python is Already Installed
```bash
python3 --version
```

If you see a version number (3.8 or higher), you're done!

#### Ubuntu/Debian Installation
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Fedora Installation
```bash
sudo dnf install python3
```

#### Arch Linux Installation
```bash
sudo pacman -S python
```

---

## Understanding Python Components

After installation, you have several tools:

| Tool | What It Does | How to Access It |
|------|--------------|------------------|
| `python` (or `python3`) | Runs Python programs | Command line |
| **IDLE** | Basic Python editor | Comes with Python |
| **pip** | Installs extra Python packages | Command line |

### What is IDLE?

IDLE (Integrated Development and Learning Environment) is a simple editor that comes with Python. While we'll use VS Code later, you can try IDLE now:

**Windows**: Search for "IDLE" in the Start menu  
**Mac**: Open Terminal, type `idle3`  
**Linux**: Open Terminal, type `idle3`

You'll see a window with `>>>` prompts. This is the **Python shell**—you can type Python code here and see immediate results.

Try typing:
```python
>>> 2 + 2
4
>>> print("Hello!")
Hello!
```

---

## Common Installation Issues

### Windows: "'python' is not recognized"

**Cause**: Python wasn't added to PATH during installation

**Solution 1**: Reinstall Python and check "Add Python to PATH"

**Solution 2**: Use `py` instead of `python`:
```
py --version
```

### Mac: "command not found: python3"

**Cause**: Python isn't installed or not in PATH

**Solution**: Install using the official installer from python.org

### Linux: Permission Denied

**Cause**: Need administrator privileges

**Solution**: Use `sudo` before the install command

### "Python version is too old"

**Cause**: You have Python 2 or an old Python 3

**Solution**: Install the latest Python 3 from python.org

---

## Testing Your Installation

Let's run a quick test to make sure everything works.

### Test 1: Check Python Version

Open your terminal/command prompt and run:

```bash
# Windows
python --version

# Mac/Linux
python3 --version
```

Expected output: `Python 3.8.x` or higher (3.10+ recommended)

### Test 2: Run a Simple Command

In your terminal, start Python interactively:

```bash
# Windows
python

# Mac/Linux
python3
```

You should see:
```
Python 3.12.0 (main, Oct  2 2023, 12:00:00)
[GCC ...] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Now type:
```python
>>> print("Python is working!")
Python is working!
```

Press `Ctrl + Z` then Enter (Windows) or `Ctrl + D` (Mac/Linux) to exit.

### Test 3: Run the Installation Check Script

We've provided a script that checks your Python installation. Save this as `install_check.py` and run it:

**Exercise**: See [day01_exercises/install_check.py](./day01_exercises/install_check.py)

Run it with:
```bash
# Windows
python day01_exercises\install_check.py

# Mac/Linux
python3 day01_exercises/install_check.py
```

---

## What's Next?

Now that Python is installed, tomorrow we'll set up a proper coding environment with **Visual Studio Code**—a free, powerful editor that will make writing Python much easier.

**Next**: [Day 02: Setting Up Your Environment](./day02_environment_setup.md)

---

## Summary Checklist

- [ ] Downloaded Python 3.8+ from python.org
- [ ] Installed Python (with "Add to PATH" checked on Windows)
- [ ] Verified installation with `python --version` (or `python3 --version`)
- [ ] Ran the installation check script successfully
- [ ] Can start Python interactive mode

---

## Quick Reference Card

| Action | Windows | Mac | Linux |
|--------|---------|-----|-------|
| Check version | `python --version` | `python3 --version` | `python3 --version` |
| Run Python file | `python file.py` | `python3 file.py` | `python3 file.py` |
| Open interactive mode | `python` | `python3` | `python3` |
| Exit interactive mode | `Ctrl+Z`, Enter | `Ctrl+D` | `Ctrl+D` |
