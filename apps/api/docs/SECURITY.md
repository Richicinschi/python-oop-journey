# Code Execution Security

This document describes the security measures implemented for user code execution in the Python Playground API.

## Overview

The code execution service uses a **defense-in-depth** strategy with multiple security layers:

1. **Static Analysis (AST Scanning)** - Blocks dangerous code patterns before execution
2. **Restricted Execution Environment** - Removes dangerous builtins from user code
3. **Subprocess Isolation** - Runs code in separate process with timeout
4. **Resource Limits** - Memory, CPU, and output size constraints
5. **Network/File System Isolation** - Blocked via import restrictions

## Security Layers

### Layer 1: Static Analysis

Before any code is executed, it is parsed into an Abstract Syntax Tree (AST) and analyzed for security violations.

**Blocked Modules:**
- `os` - System commands and file operations
- `subprocess` - Process spawning
- `socket`, `ssl`, `asyncio` - Network access
- `urllib`, `http`, `ftplib` - Web/network protocols
- `sys` - System internals
- `ctypes` - Foreign function interface
- `pickle` - Unsafe serialization
- `inspect` - Runtime introspection
- And many more...

**Blocked Functions:**
- `eval()` - Arbitrary code execution
- `exec()` - Dynamic code execution
- `compile()` - Code compilation
- `open()` - File access
- `__import__()` - Dynamic imports
- `breakpoint()` - Debugger access

**Blocked Attributes:**
- `__subclasses__` - Class hierarchy traversal
- `__globals__`, `__code__` - Function introspection
- `__mro__`, `__bases__` - Class inspection
- `__dict__`, `__class__` - Object introspection

### Layer 2: Restricted Execution

User code runs with a restricted set of builtins:

**Allowed Builtins:**
- Basic types: `int`, `str`, `list`, `dict`, `set`, `tuple`, `bool`
- Math functions: `abs`, `round`, `sum`, `min`, `max`, `pow`, `divmod`
- Iteration: `range`, `enumerate`, `zip`, `map`, `filter`, `iter`, `next`
- Object functions: `len`, `repr`, `hash`, `id`, `isinstance`, `issubclass`
- Output: `print` (output is captured)
- Type conversion: `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `set`

**Removed Builtins:**
- `open`, `eval`, `exec`, `compile`
- `input`, `breakpoint`
- `exit`, `quit`, `help`

### Layer 3: Subprocess Isolation

Code executes in a separate Python process:
- Timeout enforcement (default: 10 seconds)
- Memory limits (Unix: 256 MB via `resource` module)
- CPU limits (Unix)
- File size limits (Unix)
- Output truncation (10 KB max)

### Layer 4: Windows-Specific Considerations

On Windows (where `resource` module is unavailable):
- Process timeout is strictly enforced via `subprocess.timeout`
- Output size limiting prevents DoS via large output
- No shell execution (`shell=False`)

## Security Error Messages

When code is blocked, users receive clear error messages:

```
Security violation: Line 1: Import of dangerous module 'os' is not allowed
```

```
Security violation: Line 3: Call to dangerous function 'eval' is not allowed
```

```
Security violation: Line 5: Access to dangerous attribute '__subclasses__' is not allowed
```

## What Is Allowed

Users can safely execute:
- Basic arithmetic and math operations
- String and list operations
- Function definitions and calls
- Class definitions (without metaclass tricks)
- Control flow (if/else, for, while, try/except)
- Comprehensions and generators
- Standard library modules like `math`, `random`, `datetime`, `json`, `re`

## Testing Security

Run the security test suite:

```bash
cd website-playground/apps/api
python -m pytest tests/test_execution_security.py -v
```

## Reporting Security Issues

If you discover a security vulnerability in the code execution system:

1. Do NOT open a public issue
2. Contact the maintainers privately
3. Provide a proof-of-concept that demonstrates the vulnerability
4. Allow time for remediation before public disclosure

## Security Statistics

The execution service tracks security metrics:

```python
service = get_simple_execution_service()
stats = service.get_security_stats()
# Returns: {'executions': N, 'blocked_by_scanner': N, 'timeout': N, 'errors': N}
```

## Future Improvements

Potential future security enhancements:

1. **Windows Job Objects** - Better resource control on Windows
2. **Seccomp/AppArmor** - Linux sandboxing (if deployed on Linux)
3. **Network Namespaces** - Complete network isolation
4. **Filesystem Sandboxing** - chroot or container-based isolation
5. **Rate Limiting** - Per-user execution limits
6. **Content Security Policy** - For browser-based components

## References

- [Python AST Module](https://docs.python.org/3/library/ast.html)
- [OWASP Code Injection](https://owasp.org/www-community/attacks/Code_Injection)
- [Python Sandboxing](https://security.stackexchange.com/questions/215663/how-to-sandbox-untrusted-python-code)
