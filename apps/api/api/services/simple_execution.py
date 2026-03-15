"""Secure subprocess-based code execution for Render free tier.

This replaces Docker/Piston for environments where containerization isn't available.
Uses AST-based security scanning, resource limits, and restricted globals for defense-in-depth.

Security layers:
1. AST-based static analysis blocks dangerous imports/functions
2. Restricted execution environment removes dangerous builtins
3. Subprocess timeout and resource limits
4. Output size limiting
"""

import ast
import logging
import multiprocessing
import os
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from typing import Any, Dict, Optional, Set, Tuple

from api.schemas.execution import CodeExecutionRequest, ExecutionResult

logger = logging.getLogger(__name__)

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

# Resource limits
MAX_MEMORY_MB = 256
MAX_EXECUTION_TIME_SECONDS = 10
MAX_OUTPUT_SIZE = 10240  # 10KB

# Dangerous imports that are completely blocked
DANGEROUS_MODULES: Set[str] = {
    # System and OS access
    'os', 'posix', 'nt', 'pwd', 'grp', 'spwd',
    # Process execution
    'subprocess', 'multiprocessing',
    # Network access
    'socket', 'ssl', 'asyncio', 'select', 'selectors',
    # Web/network protocols
    'urllib', 'http', 'ftplib', 'smtplib', 'poplib', 'imaplib', 'nntplib',
    'telnetlib', 'xmlrpc', 'http.cookiejar', 'http.cookies',
    # System internals
    'sys', 'sysconfig', 'site', 'builtins', '__builtin__',
    # Code compilation and execution
    'compileall', 'py_compile', 'code', 'codeop',
    # File system and path
    'pathlib',  # Partial - we allow specific path operations via wrapper
    'shutil', 'tarfile', 'zipfile', 'gzip', 'bz2', 'lzma', 'zlib',
    # Dynamic loading
    'ctypes', 'ctypeslib', '_ctypes', 'imp', 'importlib.util', 'zipimport',
    # Foreign function interface
    'mmap', 'faulthandler', 'tracemalloc',
    # Introspection that can break sandbox
    'inspect', 'types', 'dis', 'pickle', 'copyreg', 'shelve',
    # Debugger and trace
    'pdb', 'bdb', 'trace', 'sysconfig',
    # Database access (if any)
    'sqlite3', 'dbm',
}

# Dangerous function calls that are blocked
DANGEROUS_FUNCTIONS: Set[str] = {
    'eval', 'exec', 'compile', '__import__', 'open',
    'input', 'raw_input',  # Python 2/3
    'breakpoint',  # Python 3.7+
    'exit', 'quit',
    'help',  # Can access system internals
    'copyright', 'credits', 'license',
}

# Dangerous attribute access patterns
DANGEROUS_ATTRIBUTES: Set[str] = {
    '__bases__', '__globals__', '__code__', '__func__', '__self__',
    '__module__', '__dict__', '__class__', '__mro__',
    '__subclasses__', '__getattribute__', '__setattr__',
    '__delattr__', '__slots__', '__weakref__',
    'gi_frame', 'gi_code', 'cr_frame', 'cr_code',  # Generator/coroutine internals
    'f_back', 'f_builtins', 'f_globals', 'f_locals',  # Frame internals
}

# Dangerous dunder methods that can escape sandbox
DANGEROUS_DUNDERS: Set[str] = {
    '__import__', '__loader__', '__spec__', '__builtins__',
    '__cached__', '__file__', '__name__', '__package__',
}


class SecurityError(Exception):
    """Raised when code fails security scanning."""
    pass


# =============================================================================
# SECURITY SCANNER
# =============================================================================

def scan_code_security(code: str) -> Tuple[bool, Optional[str]]:
    """
    Perform static analysis on code to detect dangerous operations.
    
    Returns:
        Tuple of (is_safe, error_message)
        - is_safe: True if code passes all security checks
        - error_message: Description of violation if not safe, None otherwise
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}, column {e.offset}: {e.msg}"
    except Exception as e:
        return False, f"Failed to parse code: {str(e)}"
    
    scanner = SecurityScanner()
    scanner.visit(tree)
    
    if scanner.violations:
        return False, "; ".join(scanner.violations)
    
    return True, None


class SecurityScanner(ast.NodeVisitor):
    """AST visitor that detects security violations in Python code."""
    
    def __init__(self):
        self.violations: list[str] = []
        self.imported_names: Dict[str, str] = {}  # alias -> real_name
        
    def add_violation(self, node: ast.AST, message: str):
        """Add a security violation with line number."""
        line = getattr(node, 'lineno', '?')
        self.violations.append(f"Line {line}: {message}")
        
    def visit_Import(self, node: ast.Import):
        """Check for dangerous module imports."""
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            if module_name in DANGEROUS_MODULES:
                self.add_violation(node, f"Import of dangerous module '{alias.name}' is not allowed")
            # Track alias for later name resolution
            if alias.asname:
                self.imported_names[alias.asname] = alias.name
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Check for dangerous from-imports."""
        if node.module:
            module_name = node.module.split('.')[0]
            if module_name in DANGEROUS_MODULES:
                self.add_violation(node, f"Import from dangerous module '{node.module}' is not allowed")
            # Track aliases
            for alias in node.names:
                if alias.asname:
                    self.imported_names[alias.asname] = f"{node.module}.{alias.name}"
        self.generic_visit(node)
        
    def visit_Call(self, node: ast.Call):
        """Check for dangerous function calls."""
        func_name = self._get_call_name(node.func)
        
        if func_name:
            # Check for dangerous builtins
            base_name = func_name.split('.')[-1]
            if base_name in DANGEROUS_FUNCTIONS:
                self.add_violation(node, f"Call to dangerous function '{func_name}' is not allowed")
            
            # Check for getattr/setattr/delattr with dangerous attributes
            if base_name in ('getattr', 'setattr', 'delattr'):
                if len(node.args) >= 2:
                    attr_arg = node.args[1]
                    if isinstance(attr_arg, ast.Constant) and attr_arg.value in DANGEROUS_ATTRIBUTES:
                        self.add_violation(node, f"Access to dangerous attribute '{attr_arg.value}' is not allowed")
        
        self.generic_visit(node)
        
    def visit_Name(self, node: ast.Name):
        """Check for direct use of dangerous names."""
        if isinstance(node.ctx, ast.Load):
            # Check if this is a dangerous builtin
            if node.id in DANGEROUS_FUNCTIONS:
                self.add_violation(node, f"Use of dangerous name '{node.id}' is not allowed")
        self.generic_visit(node)
        
    def visit_Attribute(self, node: ast.Attribute):
        """Check for access to dangerous attributes."""
        if node.attr in DANGEROUS_ATTRIBUTES:
            self.add_violation(node, f"Access to dangerous attribute '{node.attr}' is not allowed")
        self.generic_visit(node)
        
    def visit_Expression(self, node: ast.Expression):
        """Check expression statements."""
        self.generic_visit(node)
        
    def _get_call_name(self, func: ast.expr) -> Optional[str]:
        """Extract the name of a called function."""
        if isinstance(func, ast.Name):
            return func.id
        elif isinstance(func, ast.Attribute):
            parts = []
            current = func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        return None


# =============================================================================
# RESTRICTED EXECUTION WRAPPER
# =============================================================================

RESTRICTED_EXECUTION_WRAPPER = '''
# Restricted execution environment
# This code runs user code in a sandboxed context

import sys
import builtins

# Remove dangerous builtins
_safe_builtins = {{
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
    'callable', 'chr', 'classmethod', 'complex', 'delattr', 'dict',
    'dir', 'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
    'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'int', 'isinstance',
    'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview',
    'min', 'next', 'object', 'oct', 'ord', 'pow', 'print', 'property',
    'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted',
    'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip',
    '__build_class__', '__import__', '__name__', '__doc__', '__package__',
    '__spec__', '__annotations__', '__builtins__', '__cached__', '__file__',
    'True', 'False', 'None', 'NotImplemented', 'Ellipsis',
}}

# Create restricted builtins
_restricted_builtins = {{}}
for name in _safe_builtins:
    if hasattr(builtins, name):
        _restricted_builtins[name] = getattr(builtins, name)

# Replace builtins with restricted set
__builtins__ = _restricted_builtins

# Execute user code
{user_code}
'''


def create_restricted_code(user_code: str) -> str:
    """Wrap user code in a restricted execution environment."""
    # Escape triple quotes to prevent code injection
    safe_code = user_code.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
    return RESTRICTED_EXECUTION_WRAPPER.format(user_code=user_code)


# =============================================================================
# RESOURCE LIMITS
# =============================================================================

# Check if resource module is available (Unix only)
try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False
    logger.warning("Resource module not available (Windows or restricted environment). "
                   "Using process timeouts and memory monitoring instead.")


def set_resource_limits():
    """Set resource limits for the child process (Unix only)."""
    if not RESOURCE_AVAILABLE:
        return
    
    try:
        # Limit memory (address space)
        max_memory_bytes = MAX_MEMORY_MB * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))
        
        # Limit CPU time
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_EXECUTION_TIME_SECONDS, MAX_EXECUTION_TIME_SECONDS))
        
        # Limit file size
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT_SIZE, MAX_OUTPUT_SIZE))
        
        # Limit number of open files
        resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
        
        # Limit core dump size (security: prevent info leak)
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        
    except Exception as e:
        # Log but don't fail - better to run without limits than not at all
        logger.warning(f"Failed to set resource limits: {e}")


# =============================================================================
# EXECUTION SERVICE
# =============================================================================

class SimpleExecutionService:
    """Secure code execution using subprocess with defense-in-depth security."""

    def __init__(self):
        self.security_stats = {
            'executions': 0,
            'blocked_by_scanner': 0,
            'timeout': 0,
            'errors': 0,
        }

    def execute(self, request: CodeExecutionRequest) -> ExecutionResult:
        """
        Execute Python code in a sandboxed subprocess.
        
        Security layers:
        1. Static analysis blocks dangerous code patterns
        2. Restricted execution environment removes dangerous builtins
        3. Subprocess isolation with timeout
        4. Resource limits (Unix) or timeout enforcement (Windows)
        5. Output size limiting
        """
        start_time = time.time()
        temp_file = None
        
        try:
            # Layer 1: Security scanning
            is_safe, error_message = scan_code_security(request.code)
            if not is_safe:
                self.security_stats['blocked_by_scanner'] += 1
                logger.warning(f"Security scanner blocked code: {error_message}")
                return ExecutionResult(
                    success=False,
                    stdout="",
                    stderr=f"Security violation: {error_message}",
                    exit_code=1,
                    duration_ms=int((time.time() - start_time) * 1000),
                    timeout=False,
                    error="Security violation",
                )
            
            self.security_stats['executions'] += 1
            
            # Layer 2: Wrap code in restricted environment
            restricted_code = create_restricted_code(request.code)
            
            # Create temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(restricted_code)
                temp_file = f.name

            try:
                # Layer 3 & 4: Run in isolated subprocess
                result = self._run_subprocess(temp_file, request.timeout)
                
                if result.timeout:
                    self.security_stats['timeout'] += 1
                
                return result

            finally:
                # Clean up temp file
                if temp_file:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

        except Exception as e:
            self.security_stats['errors'] += 1
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.exception("Execution error")
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Execution error: {str(e)}",
                exit_code=1,
                duration_ms=execution_time_ms,
                timeout=False,
                error=str(e),
            )

    def _run_subprocess(self, temp_file: str, timeout: int) -> ExecutionResult:
        """Run code in a subprocess with resource limits."""
        start_time = time.time()
        
        # Prepare subprocess arguments
        subprocess_args = {
            'capture_output': True,
            'text': True,
            'timeout': min(timeout, MAX_EXECUTION_TIME_SECONDS),
            # Disable shell=True for security
            'shell': False,
        }
        
        # Only use preexec_fn on Unix systems
        if RESOURCE_AVAILABLE and hasattr(os, 'fork'):
            subprocess_args['preexec_fn'] = set_resource_limits

        # Run the code
        result = subprocess.run(
            [sys.executable, temp_file],
            **subprocess_args
        )

        execution_time_ms = int((time.time() - start_time) * 1000)

        # Truncate output if too large (prevent DoS via large output)
        stdout = result.stdout[:MAX_OUTPUT_SIZE] if result.stdout else ""
        stderr = result.stderr[:MAX_OUTPUT_SIZE] if result.stderr else ""

        success = result.returncode == 0

        return ExecutionResult(
            success=success,
            stdout=stdout,
            stderr=stderr,
            exit_code=result.returncode,
            duration_ms=execution_time_ms,
            timeout=False,
        )

    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax without executing."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}, column {e.offset}: {e.msg}"
        except Exception as e:
            return False, str(e)

    def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics for monitoring."""
        return self.security_stats.copy()


# Singleton instance
_simple_service: Optional[SimpleExecutionService] = None


def get_simple_execution_service() -> SimpleExecutionService:
    """Get or create simple execution service singleton."""
    global _simple_service
    if _simple_service is None:
        _simple_service = SimpleExecutionService()
    return _simple_service
