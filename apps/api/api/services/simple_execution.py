"""Simple subprocess-based code execution for Render free tier.

This replaces Docker/Piston for environments where containerization isn't available.
Uses resource limits and timeouts for basic security.
"""

import ast
import logging
import os
import resource
import signal
import subprocess
import sys
import tempfile
from typing import Optional, Tuple

from api.schemas.execution import CodeExecutionRequest, ExecutionResult

logger = logging.getLogger(__name__)

# Resource limits
MAX_MEMORY_MB = 256
MAX_EXECUTION_TIME_SECONDS = 10
MAX_OUTPUT_SIZE = 10240  # 10KB


def set_resource_limits():
    """Set resource limits for the child process."""
    # Limit memory
    max_memory_bytes = MAX_MEMORY_MB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))
    
    # Limit CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (MAX_EXECUTION_TIME_SECONDS, MAX_EXECUTION_TIME_SECONDS))
    
    # Limit file size
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT_SIZE, MAX_OUTPUT_SIZE))


class SimpleExecutionService:
    """Simple code execution using subprocess with resource limits."""

    def __init__(self):
        pass

    def execute(self, request: CodeExecutionRequest) -> ExecutionResult:
        """Execute Python code in a subprocess with resource limits."""
        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(request.code)
                temp_file = f.name

            try:
                # Run the code with resource limits
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=MAX_EXECUTION_TIME_SECONDS,
                    preexec_fn=set_resource_limits,
                )

                # Truncate output if too large
                stdout = result.stdout[:MAX_OUTPUT_SIZE]
                stderr = result.stderr[:MAX_OUTPUT_SIZE]

                return ExecutionResult(
                    stdout=stdout,
                    stderr=stderr,
                    exit_code=result.returncode,
                    execution_time_ms=0,  # Could add timing if needed
                    timeout=False,
                )

            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    stdout="",
                    stderr="Execution timed out",
                    exit_code=1,
                    execution_time_ms=MAX_EXECUTION_TIME_SECONDS * 1000,
                    timeout=True,
                )

            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except Exception as e:
            logger.exception("Execution error")
            return ExecutionResult(
                stdout="",
                stderr=f"Execution error: {str(e)}",
                exit_code=1,
                timeout=False,
            )

    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax without executing."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)


# Singleton instance
_simple_service: Optional[SimpleExecutionService] = None


def get_simple_execution_service() -> SimpleExecutionService:
    """Get or create simple execution service singleton."""
    global _simple_service
    if _simple_service is None:
        _simple_service = SimpleExecutionService()
    return _simple_service
