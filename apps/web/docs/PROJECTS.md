# Projects Documentation

## Overview

The Projects feature in Python OOP Journey provides a hands-on, multi-file coding environment where learners can build real applications to reinforce their understanding of Object-Oriented Programming concepts.

## Features

### Multi-File Editor
- **File Tree Explorer**: Navigate through your project files with an expandable tree view
- **Tabbed Interface**: Work on multiple files simultaneously with tabs
- **Auto-Save**: Files are automatically saved to localStorage (with debouncing)
- **Syntax Highlighting**: Full Python syntax support via Monaco Editor
- **File Operations**: Create, delete, and rename files

### Code Execution
- **Run Code**: Execute your Python code directly in the browser (Ctrl+R)
- **Run Tests**: Verify your solution against test cases (Ctrl+T)
- **Output Panel**: View execution results, test output, and error messages

### Project Progress Tracking
- **Status Tracking**: Projects can be Not Started, In Progress, or Submitted
- **Time Tracking**: Automatic tracking of time spent on each project
- **Completion Percentage**: Visual progress indicator based on saved files

## Keyboard Shortcuts

### File Operations
| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save current file |
| `Ctrl+Shift+S` | Save all files |
| `Ctrl+N` | Create new file |

### Code Execution
| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Run project |
| `Ctrl+T` | Run tests |
| `Ctrl+Enter` | Run current file |

### View
| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Toggle file tree |
| `Ctrl+\` | Split editor |
| `Ctrl+0` | Reset zoom |
| `Ctrl++` | Zoom in |
| `Ctrl+-` | Zoom out |

### Navigation
| Shortcut | Action |
|----------|--------|
| `Ctrl+Tab` | Next tab |
| `Ctrl+Shift+Tab` | Previous tab |
| `Ctrl+W` | Close current tab |

### General
| Shortcut | Action |
|----------|--------|
| `?` | Show keyboard shortcuts help |

## Best Practices

### Before Starting a Project

1. **Read the README**: Always start by reading the README.md file for project requirements
2. **Review Requirements**: Understand what you need to build before writing code
3. **Plan Your Approach**: Think about the classes and structure you'll need

### While Working

1. **Save Frequently**: Use Ctrl+S to save your work regularly
2. **Test Often**: Run your code frequently to catch errors early
3. **Use Version Control**: Although we auto-save, consider copying important milestones
4. **Read Error Messages**: Python error messages are helpful - read them carefully

### File Organization

```
project/
├── README.md          # Project requirements and instructions
├── main.py            # Main entry point
├── models.py          # Class definitions
├── utils.py           # Helper functions
└── tests.py           # Test cases (if required)
```

### Code Style

1. **Follow PEP 8**: Use standard Python naming conventions
   - `snake_case` for functions and variables
   - `PascalCase` for classes
   - `UPPER_CASE` for constants

2. **Write Docstrings**: Document your functions and classes
   ```python
   def calculate_area(radius):
       """Calculate the area of a circle.
       
       Args:
           radius (float): The radius of the circle
           
       Returns:
           float: The area of the circle
       """
       return 3.14159 * radius ** 2
   ```

3. **Add Comments**: Explain complex logic, but prefer clear code over comments

## Troubleshooting

### Code Won't Run

**Problem**: Clicking Run produces no output

**Solutions**:
1. Check that you're editing the right file
2. Ensure your code has no syntax errors
3. Verify the file is saved (no dot indicator on tab)
4. Try refreshing the page

### Changes Not Saving

**Problem**: Files show as modified after saving

**Solutions**:
1. Wait a moment - auto-save has a 1-second debounce
2. Try Ctrl+S again
3. Check browser console for errors
4. Ensure localStorage is not disabled

### Editor Not Loading

**Problem**: Code editor shows blank or loading spinner

**Solutions**:
1. Wait a few seconds - Monaco Editor is loading
2. Refresh the page
3. Clear browser cache
4. Check internet connection (for CDN resources)

### Project Won't Submit

**Problem**: Submit button doesn't work

**Solutions**:
1. Ensure all files are saved
2. Check browser console for errors
3. Verify you're connected to the internet
4. Try again after a moment

## Project Structure

### Week 1: CLI Calculator
- **Difficulty**: Beginner
- **Time**: 2 hours
- **Concepts**: Basic Python, user input, functions
- **Files**: `main.py`, `calculator.py`, `README.md`

### Week 4: Library Management System
- **Difficulty**: Intermediate
- **Time**: 3 hours
- **Concepts**: Classes, inheritance, file I/O
- **Files**: `main.py`, `book.py`, `patron.py`, `library.py`

### Week 8: E-Commerce System (Capstone)
- **Difficulty**: Expert
- **Time**: 6 hours
- **Concepts**: All OOP principles, design patterns
- **Files**: Multiple modules with comprehensive structure

## Tips for Success

1. **Start Simple**: Get a basic version working before adding features
2. **Test Incrementally**: Run your code after every small change
3. **Use the Hints**: They're there to help when you're stuck
4. **Review Solutions**: After submitting, compare with reference solutions
5. **Practice**: The more projects you complete, the better you'll understand OOP

## Accessibility

The Projects feature includes:
- Full keyboard navigation support
- ARIA labels for screen readers
- High contrast mode support
- Resizable panels for different screen sizes

## Data Storage

- Project files are stored in browser localStorage
- Progress syncs across tabs
- Data persists between sessions
- Clear browser data to reset progress

## Getting Help

If you encounter issues:
1. Check this documentation
2. Review the keyboard shortcuts (press `?`)
3. Take the tour (available in project settings)
4. Contact support with specific error messages
