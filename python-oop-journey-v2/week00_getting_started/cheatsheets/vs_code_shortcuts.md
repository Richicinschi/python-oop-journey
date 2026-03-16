# VS Code Shortcuts Cheatsheet

Essential keyboard shortcuts and tips for Python development in Visual Studio Code.

---

## Most Important Shortcuts

| Shortcut | Windows/Linux | Mac | Description |
|----------|---------------|-----|-------------|
| Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` | Access all commands |
| Quick Open | `Ctrl+P` | `Cmd+P` | Open files quickly |
| Search Files | `Ctrl+Shift+F` | `Cmd+Shift+F` | Search across project |
| Terminal | `` Ctrl+` `` | `` Cmd+` `` | Toggle integrated terminal |

---

## Editing Shortcuts

### Basic Editing

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Copy line (no selection) | `Ctrl+C` | `Cmd+C` |
| Cut line (no selection) | `Ctrl+X` | `Cmd+X` |
| Move line up/down | `Alt+↑/↓` | `Opt+↑/↓` |
| Copy line up/down | `Shift+Alt+↑/↓` | `Shift+Opt+↑/↓` |
| Delete line | `Ctrl+Shift+K` | `Cmd+Shift+K` |
| Insert line below | `Ctrl+Enter` | `Cmd+Enter` |
| Insert line above | `Ctrl+Shift+Enter` | `Cmd+Shift+Enter` |

### Multi-Cursor Editing

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Add cursor above/below | `Ctrl+Alt+↑/↓` | `Cmd+Opt+↑/↓` |
| Add cursor to next match | `Ctrl+D` | `Cmd+D` |
| Select all matches | `Ctrl+Shift+L` | `Cmd+Shift+L` |
| Undo last cursor | `Ctrl+U` | `Cmd+U` |

```
Example: Multi-Cursor
1. Click on a variable name
2. Press Ctrl+D to select it
3. Press Ctrl+D again to select next occurrence
4. Type to edit all at once
```

---

## Navigation Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Go to file | `Ctrl+P` | `Cmd+P` |
| Go to symbol | `Ctrl+Shift+O` | `Cmd+Shift+O` |
| Go to line | `Ctrl+G` | `Ctrl+G` |
| Go to definition | `F12` | `F12` |
| Peek definition | `Alt+F12` | `Opt+F12` |
| Go back/forward | `Alt+←/→` | `Ctrl+-` / `Ctrl+Shift+-` |
| Next/previous error | `F8` / `Shift+F8` | `F8` / `Shift+F8` |

---

## Code Formatting & Intellisense

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Format document | `Shift+Alt+F` | `Shift+Opt+F` |
| Format selection | `Ctrl+K Ctrl+F` | `Cmd+K Cmd+F` |
| Trigger suggestion | `Ctrl+Space` | `Ctrl+Space` |
| Quick fix | `Ctrl+.` | `Cmd+.` |
| Rename symbol | `F2` | `F2` |
| Refactor | `Ctrl+Shift+R` | `Ctrl+Shift+R` |

---

## Python Extension Features

### Python-Specific Shortcuts (with Python extension)

| Action | Shortcut | Description |
|--------|----------|-------------|
| Run Python file | Play button or `Ctrl+F5` | Execute current file |
| Start debugging | `F5` | Run with debugger |
| Select interpreter | `Ctrl+Shift+P` → "Python: Select Interpreter" | Choose Python version |
| Create terminal | `Ctrl+Shift+`` | Open Python-aware terminal |

### Code Actions (Lightbulb 💡)

When you see a 💡, press `Ctrl+.` (Windows/Linux) or `Cmd+.` (Mac) for:

- **Import suggestions** - Auto-import missing modules
- **Refactoring options** - Extract method, variable, etc.
- **Quick fixes** - Fix common errors automatically

---

## Debugging Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Start debugging | `F5` | `F5` |
| Run without debugging | `Ctrl+F5` | `Ctrl+F5` |
| Stop debugging | `Shift+F5` | `Shift+F5` |
| Toggle breakpoint | `F9` | `F9` |
| Step over | `F10` | `F10` |
| Step into | `F11` | `F11` |
| Step out | `Shift+F11` | `Shift+F11` |
| Continue | `F5` | `F5` |

### Debugging Workflow

```
1. Set breakpoint (F9) on the line you want to pause
2. Start debugging (F5)
3. Use F10 to step over (execute current line, move to next)
4. Use F11 to step into (enter function calls)
5. Watch variables in the left panel
6. Use Debug Console to inspect values
```

---

## Terminal Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Toggle terminal | `` Ctrl+` `` | `` Cmd+` `` |
| New terminal | `` Ctrl+Shift+` `` | `` Cmd+Shift+` `` |
| Close terminal | `Ctrl+Shift+W` | `Cmd+Shift+W` |
| Clear terminal | `Ctrl+K` | `Cmd+K` |
| Kill terminal | `Ctrl+C` | `Ctrl+C` |

---

## Essential VS Code Settings for Python

Add to your `settings.json` (`Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"):

```json
{
    // Python
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    
    // Editor
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.formatOnSave": true,
    "editor.rulers": [79, 120],
    
    // Whitespace visibility
    "editor.renderWhitespace": "boundary",
    "editor.renderIndentGuides": true,
    
    // Files
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
}
```

---

## Recommended Extensions

### Must-Have Extensions

| Extension | Purpose |
|-----------|---------|
| **Python** (Microsoft) | Core Python support |
| **Pylance** (Microsoft) | Fast language server |
| **Python Test Explorer** | Run and debug tests |

### Helpful Extensions

| Extension | Purpose |
|-----------|---------|
| **autoDocstring** | Generate docstrings |
| **Python Indent** | Correct indentation |
| **Error Lens** | Inline error display |
| **GitLens** | Enhanced Git integration |
| **Material Icon Theme** | File icons |

---

## Command Palette (Ctrl+Shift+P / Cmd+Shift+P)

Most powerful VS Code feature! Type to find any command:

| Search Term | Action |
|-------------|--------|
| `>python:` | All Python commands |
| `>python: select interpreter` | Choose Python version |
| `>python: create terminal` | Open Python terminal |
| `>python: run tests` | Execute pytest |
| `>format document` | Format current file |
| `>preferences: open settings` | Edit settings |
| `>git:` | Git commands |

---

## Python-Specific Tips

### Virtual Environment Workflow

```bash
# 1. Create virtual environment
python -m venv venv

# 2. VS Code will detect it, or select it:
#    Ctrl+Shift+P → "Python: Select Interpreter"
#    Choose ./venv/bin/python (or .\venv\Scripts\python.exe on Windows)

# 3. Open integrated terminal
#    It automatically activates the venv

# 4. Install packages
pip install package_name
```

### Running Python Code

| Method | How |
|--------|-----|
| Current file | Click ▶️ in top-right or `Ctrl+F5` |
| Selection | Right-click → "Run Selection/Line in Terminal" |
| Interactive | Shift+Enter to send to Python terminal |

---

## Snippets (Type then press Tab)

| Snippet | Expands To |
|---------|------------|
| `def` | Function definition |
| `if` | If statement |
| `for` | For loop |
| `while` | While loop |
| `class` | Class definition |
| `ifmain` | `if __name__ == "__main__":` |

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | `Ctrl+Shift+P` → "Python: Select Interpreter" |
| Formatting not working | Install Black: `pip install black` |
| Linting not working | Enable in settings, install pylint |
| Terminal not activating venv | Close and reopen terminal |
| IntelliSense slow | Install Pylance extension |
| Import errors | Check selected interpreter matches your venv |

---

## Learning More

- **Command Palette**: `Ctrl+Shift+P` → type "keyboard shortcuts"
- **Printable PDF**: Open Command Palette → "Preferences: Open Keyboard Shortcuts" → Click icon for PDF
- **Interactive Tutorial**: Help → Welcome → Interactive Playground
