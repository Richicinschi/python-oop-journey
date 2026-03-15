"""Tests for code execution security features.

This test suite verifies that the security scanner correctly blocks
dangerous operations while allowing safe code execution.
"""

import pytest
from api.services.simple_execution import (
    scan_code_security,
    SecurityScanner,
    DANGEROUS_MODULES,
    DANGEROUS_FUNCTIONS,
    SimpleExecutionService,
)
from api.schemas.execution import CodeExecutionRequest


class TestSecurityScanner:
    """Tests for the AST-based security scanner."""
    
    def test_allows_safe_code(self):
        """Scanner should allow safe code."""
        safe_code = """
# Simple arithmetic
x = 1 + 2
print(x)

# List operations
items = [1, 2, 3]
result = sum(items)

# Function definition
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
"""
        is_safe, error = scan_code_security(safe_code)
        assert is_safe is True
        assert error is None
    
    def test_blocks_os_import(self):
        """Scanner should block os module imports."""
        code = "import os"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "os" in error.lower()
        assert "not allowed" in error.lower()
    
    def test_blocks_subprocess_import(self):
        """Scanner should block subprocess imports."""
        code = "import subprocess"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "subprocess" in error.lower()
    
    def test_blocks_socket_import(self):
        """Scanner should block socket imports."""
        code = "import socket"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "socket" in error.lower()
    
    def test_blocks_sys_import(self):
        """Scanner should block sys module imports."""
        code = "import sys"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "sys" in error.lower()
    
    def test_blocks_from_import(self):
        """Scanner should block from-imports of dangerous modules."""
        code = "from os import system"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "os" in error.lower()
    
    def test_blocks_eval(self):
        """Scanner should block eval() calls."""
        code = 'eval("1 + 2")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "eval" in error.lower()
    
    def test_blocks_exec(self):
        """Scanner should block exec() calls."""
        code = 'exec("print(1)")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "exec" in error.lower()
    
    def test_blocks_compile(self):
        """Scanner should block compile() calls."""
        code = 'compile("x = 1", "", "exec")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "compile" in error.lower()
    
    def test_blocks_open(self):
        """Scanner should block open() calls."""
        code = 'open("/etc/passwd")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "open" in error.lower()
    
    def test_blocks_underscore_import(self):
        """Scanner should block __import__ calls."""
        code = '__import__("os")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False
    
    def test_blocks_dangerous_attributes(self):
        """Scanner should block access to dangerous attributes like __subclasses__."""
        code = "().__class__.__subclasses__()"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
        assert "__subclasses__" in error
    
    def test_blocks_globals_access(self):
        """Scanner should block __globals__ access."""
        code = "lambda: None.__globals__"
        is_safe, error = scan_code_security(code)
        assert is_safe is False
    
    def test_blocks_getattr_with_dangerous_attr(self):
        """Scanner should block getattr with dangerous attribute names."""
        code = 'getattr(str, "__subclasses__")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False
    
    def test_allows_safe_getattr(self):
        """Scanner should allow getattr with safe attribute names."""
        code = 'getattr(str, "upper")'
        is_safe, error = scan_code_security(code)
        assert is_safe is True


class TestExecutionServiceSecurity:
    """Tests for the execution service with security features."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = SimpleExecutionService()
    
    def test_safe_code_execution(self):
        """Service should execute safe code."""
        request = CodeExecutionRequest(
            code="print('Hello, World!')",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is True
        assert "Hello, World!" in result.stdout
    
    def test_blocks_dangerous_code(self):
        """Service should block dangerous code patterns."""
        request = CodeExecutionRequest(
            code="import os; os.system('whoami')",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is False
        assert "Security violation" in result.stderr
        assert "os" in result.stderr.lower()
    
    def test_blocks_eval_in_code(self):
        """Service should block eval() usage."""
        request = CodeExecutionRequest(
            code='eval("1 + 2")',
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is False
        assert "Security violation" in result.stderr
        assert "eval" in result.stderr.lower()
    
    def test_blocks_file_access(self):
        """Service should block file operations."""
        request = CodeExecutionRequest(
            code='open("test.txt", "w")',
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is False
        assert "open" in result.stderr.lower() or "Security violation" in result.stderr
    
    def test_blocks_subprocess_attempts(self):
        """Service should block subprocess module usage."""
        request = CodeExecutionRequest(
            code="import subprocess; subprocess.run(['ls'])",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is False
        assert "Security violation" in result.stderr
    
    def test_blocks_urllib(self):
        """Service should block urllib network access."""
        request = CodeExecutionRequest(
            code="import urllib.request; urllib.request.urlopen('http://example.com')",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is False
        assert "urllib" in result.stderr.lower() or "Security violation" in result.stderr
    
    def test_math_operations_allowed(self):
        """Service should allow safe math operations."""
        request = CodeExecutionRequest(
            code="""
import math
result = math.sqrt(16)
print(f"Square root of 16 is {result}")
""",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is True
        assert "Square root" in result.stdout
    
    def test_string_operations_allowed(self):
        """Service should allow string operations."""
        request = CodeExecutionRequest(
            code="""
text = 'Hello, World!'
print(text.upper())
print(text.lower())
print(len(text))
""",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is True
        assert "HELLO, WORLD!" in result.stdout
    
    def test_list_operations_allowed(self):
        """Service should allow list operations."""
        request = CodeExecutionRequest(
            code="""
numbers = [3, 1, 4, 1, 5]
print(f"Sum: {sum(numbers)}")
print(f"Max: {max(numbers)}")
print(f"Sorted: {sorted(numbers)}")
""",
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is True
        assert "Sum:" in result.stdout
    
    def test_timeout_enforced(self):
        """Service should enforce execution timeouts."""
        request = CodeExecutionRequest(
            code="""
while True:
    pass
""",
            language="python",
            timeout=1
        )
        result = self.service.execute(request)
        # Should either timeout or take very long
        assert result.timeout is True or result.duration_ms > 900
    
    def test_output_size_limited(self):
        """Service should limit output size."""
        request = CodeExecutionRequest(
            code="print('x' * 50000)",  # Very large output
            language="python",
            timeout=5
        )
        result = self.service.execute(request)
        assert result.success is True
        assert len(result.stdout) <= 10240  # MAX_OUTPUT_SIZE


class TestAllDangerousModules:
    """Test that all dangerous modules are properly blocked."""
    
    @pytest.mark.parametrize("module", [
        "os", "subprocess", "socket", "sys", "urllib", "http",
        "ftplib", "shutil", "pickle", "ctypes", "inspect",
    ])
    def test_module_import_blocked(self, module):
        """Each dangerous module import should be blocked."""
        code = f"import {module}"
        is_safe, error = scan_code_security(code)
        assert is_safe is False, f"Import of {module} should be blocked"
        assert module in error.lower(), f"Error should mention {module}"


class TestAllDangerousFunctions:
    """Test that all dangerous functions are properly blocked."""
    
    @pytest.mark.parametrize("func", [
        "eval", "exec", "compile", "__import__", "open",
    ])
    def test_function_call_blocked(self, func):
        """Each dangerous function call should be blocked."""
        code = f'{func}("test")'
        is_safe, error = scan_code_security(code)
        assert is_safe is False, f"Call to {func} should be blocked"


class TestSecurityStats:
    """Tests for security statistics tracking."""
    
    def test_stats_tracked(self):
        """Service should track security statistics."""
        service = SimpleExecutionService()
        
        # Initial stats
        stats = service.get_security_stats()
        assert stats['executions'] == 0
        assert stats['blocked_by_scanner'] == 0
        
        # Execute blocked code
        request = CodeExecutionRequest(
            code="import os",
            language="python",
            timeout=5
        )
        service.execute(request)
        
        # Stats should be updated
        stats = service.get_security_stats()
        assert stats['blocked_by_scanner'] == 1
