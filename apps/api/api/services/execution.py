"""Code execution service."""

import logging
import uuid
from datetime import datetime

from api.schemas.execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    CodeValidationExecutionRequest,
    CodeValidationExecutionResponse,
    ExecutionJobResponse,
    ExecutionJobResult,
    ExecutionMetrics,
    ExecutionStatus,
    TestResult,
    ValidationResponse,
)
from api.services.docker_runner import get_docker_runner
from api.services.simple_execution import get_simple_execution_service
from api.services.monitoring import get_monitor
from api.tasks import execute_code_task, validate_code_task

logger = logging.getLogger(__name__)


class ExecutionService:
    """Service for safe code execution using subprocess sandboxing.
    
    Primary execution uses subprocess for compatibility with Render free tier.
    Docker execution is available as fallback when configured.
    """

    def __init__(self):
        """Initialize execution service."""
        self.monitor = get_monitor()
        self._docker_runner = None
        self._simple_service = None
    
    def _get_runner(self):
        """Get the appropriate execution runner.
        
        Returns:
            Simple execution service (primary) or Docker runner (if available)
        """
        if self._simple_service is None:
            self._simple_service = get_simple_execution_service()
        return self._simple_service
    
    def _get_docker_runner(self):
        """Get Docker runner if available.
        
        Returns:
            Docker runner or None if not available
        """
        if self._docker_runner is None:
            self._docker_runner = get_docker_runner()
            # Check if Docker is actually available
            if self._docker_runner._client is None:
                self._docker_runner = None
        return self._docker_runner

    async def execute(
        self, 
        request: CodeExecutionRequest,
        user_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None
    ) -> CodeExecutionResponse:
        """Execute Python code safely in a Docker container.
        
        Args:
            request: Code execution request
            user_id: Optional user identifier
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Code execution response
        """
        execution_id = str(uuid.uuid4())
        
        logger.info(f"Starting execution {execution_id} for user {user_id}")
        
        # Combine code with test code if provided
        code_to_run = request.code
        if request.test_code:
            code_to_run = f"""# User code
{request.code}

# Test code
{request.test_code}
"""
        
        # Execute using subprocess (primary method for Render compatibility)
        from api.schemas.execution import CodeExecutionRequest as SimpleRequest
        simple_request = SimpleRequest(code=code_to_run, timeout=request.timeout)
        result = self._get_runner().execute(simple_request)
        
        # Determine status
        if result.timeout:
            status = ExecutionStatus.TIMEOUT
        elif result.success:
            status = ExecutionStatus.COMPLETED
        else:
            status = ExecutionStatus.FAILED
        
        # Log execution
        self.monitor.log_execution(
            execution_id=execution_id,
            user_id=user_id,
            code=request.code,
            status=status,
            duration_ms=result.duration_ms,
            exit_code=result.exit_code,
            error=result.error,
            memory_usage_mb=result.memory_usage_mb,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return CodeExecutionResponse(
            success=result.success,
            output=result.stdout,
            error=result.error,
            execution_time_ms=result.duration_ms,
            exit_code=result.exit_code,
            timeout=result.timeout,
        )

    async def execute_async(
        self, 
        request: CodeExecutionRequest,
        user_id: str | None = None
    ) -> ExecutionJobResponse:
        """Submit code for async execution via Celery.
        
        Args:
            request: Code execution request
            user_id: Optional user identifier
            
        Returns:
            Job response with task ID
        """
        # Combine code with test code if provided
        code_to_run = request.code
        if request.test_code:
            code_to_run = f"""# User code
{request.code}

# Test code
{request.test_code}
"""
        
        # Submit to Celery
        task = execute_code_task.delay(code_to_run, request.timeout)
        
        logger.info(f"Submitted async execution task {task.id} for user {user_id}")
        
        return ExecutionJobResponse(
            job_id=task.id,
            status=ExecutionStatus.PENDING,
            message="Job submitted successfully",
            result_url=f"/api/v1/execute/jobs/{task.id}"
        )

    async def get_job_result(self, job_id: str) -> ExecutionJobResult:
        """Get result of async execution job.
        
        Args:
            job_id: Celery task ID
            
        Returns:
            Job result with status and output
        """
        from celery.result import AsyncResult
        from api.celery_app import app
        
        result = AsyncResult(job_id, app=app)
        
        # Map Celery states to our status
        state_map = {
            "PENDING": ExecutionStatus.PENDING,
            "STARTED": ExecutionStatus.RUNNING,
            "SUCCESS": ExecutionStatus.COMPLETED,
            "FAILURE": ExecutionStatus.FAILED,
            "RETRY": ExecutionStatus.PENDING,
            "REVOKED": ExecutionStatus.CANCELLED,
        }
        
        status = state_map.get(result.state, ExecutionStatus.FAILED)
        
        # Build response
        response = ExecutionJobResult(
            job_id=job_id,
            status=status,
        )
        
        # Add result if available
        if result.ready():
            if result.successful():
                task_result = result.get()
                response.result = CodeExecutionResponse(
                    success=task_result.get("success", False),
                    output=task_result.get("stdout", ""),
                    error=task_result.get("error"),
                    execution_time_ms=task_result.get("duration_ms", 0),
                    exit_code=task_result.get("exit_code"),
                    timeout=task_result.get("timeout", False),
                )
            else:
                response.result = CodeExecutionResponse(
                    success=False,
                    output="",
                    error=str(result.result) if result.result else "Task failed",
                    execution_time_ms=0,
                    exit_code=-1,
                    timeout=False,
                )
        
        return response

    async def validate_syntax(self, code: str) -> ValidationResponse:
        """Validate Python syntax without executing.
        
        Args:
            code: Python code to validate
            
        Returns:
            Validation response
        """
        is_valid, error = self._get_runner().validate_syntax(code)
        line = col = None  # Simple execution returns tuple of (is_valid, error)
        
        return ValidationResponse(
            valid=is_valid,
            error=error,
            syntax_error_line=line,
            syntax_error_col=col,
        )

    async def validate_and_test(
        self,
        request: CodeValidationExecutionRequest,
        user_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None
    ) -> CodeValidationExecutionResponse:
        """Execute code with test validation.
        
        Args:
            request: Validation request with code and tests
            user_id: Optional user identifier
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Validation response with test results
        """
        execution_id = str(uuid.uuid4())
        
        # Build test wrapper code
        test_wrapper = f'''
import sys
import io
import traceback
import unittest
from typing import Any

# Capture user code output
user_output = io.StringIO()
user_stderr = io.StringIO()

# Execute user code in isolated namespace
user_namespace = {{}}
original_stdout = sys.stdout
original_stderr = sys.stderr

try:
    sys.stdout = user_output
    sys.stderr = user_stderr
    
{self._indent_code(request.code, 4)}
    
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    
    # Run tests
    test_output = io.StringIO()
    sys.stdout = test_output
    
{self._indent_code(request.test_code, 4)}
    
    sys.stdout = original_stdout
    
    # Output results
    print("TEST_RUNNER_SUCCESS")
    print(user_output.getvalue())
    print(test_output.getvalue())
    
except Exception as e:
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    print("TEST_RUNNER_ERROR")
    print(f"Error: {{e}}")
    traceback.print_exc()
    sys.exit(1)
'''
        
        # Execute using subprocess
        from api.schemas.execution import CodeExecutionRequest as SimpleRequest
        simple_request = SimpleRequest(code=test_wrapper, timeout=request.timeout)
        result = self._get_runner().execute(simple_request)
        
        # Determine status
        if result.timeout:
            status = ExecutionStatus.TIMEOUT
        elif result.success:
            status = ExecutionStatus.COMPLETED
        else:
            status = ExecutionStatus.FAILED
        
        # Log execution
        self.monitor.log_execution(
            execution_id=execution_id,
            user_id=user_id,
            code=request.code,
            status=status,
            duration_ms=result.duration_ms,
            exit_code=result.exit_code,
            error=result.error,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Parse test results
        test_results = []
        tests_passed = 0
        tests_failed = 0
        
        if result.success:
            # Simple parsing of test output
            # In production, use a proper test runner framework
            output_lines = result.stdout.split('\n')
            
            for line in output_lines:
                if line.startswith('test_'):
                    # Parse test result line
                    if 'ok' in line.lower():
                        test_results.append(TestResult(
                            name=line.split()[0],
                            passed=True,
                            output=line,
                            duration_ms=0
                        ))
                        tests_passed += 1
                    elif 'fail' in line.lower() or 'error' in line.lower():
                        test_results.append(TestResult(
                            name=line.split()[0],
                            passed=False,
                            output=line,
                            error="Test failed",
                            duration_ms=0
                        ))
                        tests_failed += 1
        
        total_tests = tests_passed + tests_failed
        
        return CodeValidationExecutionResponse(
            success=result.success or not result.timeout,
            passed=tests_failed == 0 and total_tests > 0,
            tests_run=total_tests,
            tests_passed=tests_passed,
            tests_failed=tests_failed,
            test_results=test_results,
            stdout=result.stdout,
            stderr=result.stderr,
            execution_time_ms=result.duration_ms,
            error=result.error
        )

    async def check_rate_limit(
        self, 
        user_id: str | None, 
        ip_address: str | None
    ) -> tuple[bool, int, int]:
        """Check if user has exceeded rate limit.
        
        Args:
            user_id: User identifier
            ip_address: IP address
            
        Returns:
            Tuple of (allowed, current_count, limit)
        """
        return self.monitor.check_rate_limit(user_id, ip_address)

    async def get_metrics(self, hours: int = 24) -> ExecutionMetrics:
        """Get execution metrics.
        
        Args:
            hours: Time period in hours
            
        Returns:
            Execution metrics
        """
        return self.monitor.get_metrics(hours)

    def _indent_code(self, code: str, spaces: int = 4) -> str:
        """Indent code for embedding.
        
        Args:
            code: Code to indent
            spaces: Number of spaces to indent
            
        Returns:
            Indented code
        """
        indent = " " * spaces
        lines = code.strip().split("\n")
        return "\n".join(indent + line for line in lines)


# Service singleton
_execution_service: ExecutionService | None = None


def get_execution_service() -> ExecutionService:
    """Get or create execution service singleton."""
    global _execution_service
    if _execution_service is None:
        _execution_service = ExecutionService()
    return _execution_service


def reset_execution_service() -> None:
    """Reset execution service (for testing)."""
    global _execution_service
    _execution_service = None
