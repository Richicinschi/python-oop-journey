"""Simple subprocess-based code execution for Render free tier.

This replaces Docker/Piston for environments where containerization isn't available.
Uses resource limits and timeouts for basic security.
"""

import ast
import logging
import os
import subprocess
import sys
import tempfile
import time
from typing import Optional, Tuple

from api.schemas.execution import CodeExecutionRequest, ExecutionResult

logger = logging.getLogger(__name__)

# Resource limits
MAX_MEMORY_MB = 256
MAX_EXECUTION_TIME_SECONDS = 10
MAX_OUTPUT_SIZE = 10240  # 10KB

# Check if resource module is available (Unix only)
try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False
    logger.warning("Resource module not available (Windows or restricted environment). "
                   "Memory/CPU limits will not be enforced at OS level.")


def set_resource_limits():
    """Set resource limits for the child process."""
    if not RESOURCE_AVAILABLE:
        return
    
    try:
        # Limit memory
        max_memory_bytes = MAX_MEMORY_MB * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))
        
        # Limit CPU time
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_EXECUTION_TIME_SECONDS, MAX_EXECUTION_TIME_SECONDS))
        
        # Limit file size
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT_SIZE, MAX_OUTPUT_SIZE))
    except Exception as e:
        # Log but don't fail - better to run without limits than not at all
        logger.warning(f"Failed to set resource limits: {e}")


class SimpleExecutionService:
    """Simple code execution using subprocess with resource limits."""

    def __init__(self):
        pass

    def execute(self, request: CodeExecutionRequest) -> ExecutionResult:
        """Execute Python code in a subprocess with resource limits."""
        start_time = time.time()
        temp_file = None
        
        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(request.code)
                temp_file = f.name

            try:
                # Prepare subprocess arguments
                subprocess_args = {
                    'capture_output': True,
                    'text': True,
                    'timeout': min(request.timeout, MAX_EXECUTION_TIME_SECONDS),
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

                # Truncate output if too large
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

            except subprocess.TimeoutExpired as e:
                execution_time_ms = int((time.time() - start_time) * 1000)
                stdout = e.stdout[:MAX_OUTPUT_SIZE] if e.stdout else ""
                stderr = (e.stderr[:MAX_OUTPUT_SIZE] if e.stderr else "") or "Execution timed out"
                
                return ExecutionResult(
                    success=False,
                    stdout=stdout,
                    stderr=stderr,
                    exit_code=1,
                    duration_ms=execution_time_ms,
                    timeout=True,
                )

            finally:
                # Clean up temp file
                if temp_file:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

        except Exception as e:
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

    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax without executing."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}, column {e.offset}: {e.msg}"
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
