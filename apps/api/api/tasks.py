"""Celery tasks for code execution."""

import logging
import uuid
from datetime import datetime

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from api.schemas.execution import (
    CodeExecutionResponse,
    ExecutionResult,
    ExecutionStatus,
)
from api.services.docker_runner import get_docker_runner
from api.services.monitoring import get_monitor

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def execute_code_task(self, code: str, timeout: int = 10) -> dict:
    """Execute Python code in a Docker sandbox (async task).
    
    Args:
        self: Celery task instance
        code: Python code to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Dictionary containing execution result
    """
    execution_id = str(uuid.uuid4())
    monitor = get_monitor()
    runner = get_docker_runner()
    
    logger.info(f"Starting async execution {execution_id}")
    
    try:
        # Run the code
        result = runner.execute(code, timeout=timeout)
        
        # Determine status
        if result.timeout:
            status = ExecutionStatus.TIMEOUT
        elif result.success:
            status = ExecutionStatus.COMPLETED
        else:
            status = ExecutionStatus.FAILED
        
        # Log execution
        monitor.log_execution(
            execution_id=execution_id,
            user_id=None,  # Will be set by caller if available
            code=code,
            status=status,
            duration_ms=result.duration_ms,
            exit_code=result.exit_code,
            error=result.error,
            memory_usage_mb=result.memory_usage_mb
        )
        
        # Return result as dictionary
        return {
            "execution_id": execution_id,
            "success": result.success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.exit_code,
            "timeout": result.timeout,
            "error": result.error,
            "duration_ms": result.duration_ms,
            "memory_usage_mb": result.memory_usage_mb,
            "status": status.value,
        }
        
    except SoftTimeLimitExceeded:
        logger.error(f"Task soft time limit exceeded for execution {execution_id}")
        
        monitor.log_execution(
            execution_id=execution_id,
            user_id=None,
            code=code,
            status=ExecutionStatus.TIMEOUT,
            duration_ms=timeout * 1000,
            exit_code=-1,
            error="Task exceeded maximum execution time"
        )
        
        return {
            "execution_id": execution_id,
            "success": False,
            "stdout": "",
            "stderr": "",
            "exit_code": -1,
            "timeout": True,
            "error": "Execution exceeded maximum allowed time",
            "duration_ms": timeout * 1000,
            "memory_usage_mb": None,
            "status": ExecutionStatus.TIMEOUT.value,
        }
        
    except Exception as exc:
        logger.exception(f"Unexpected error in execution task {execution_id}")
        
        # Retry on certain errors
        if self.request.retries < self.max_retries:
            logger.warning(f"Retrying execution {execution_id} (attempt {self.request.retries + 1})")
            raise self.retry(exc=exc)
        
        monitor.log_execution(
            execution_id=execution_id,
            user_id=None,
            code=code,
            status=ExecutionStatus.FAILED,
            duration_ms=0,
            exit_code=-1,
            error=str(exc)
        )
        
        return {
            "execution_id": execution_id,
            "success": False,
            "stdout": "",
            "stderr": str(exc),
            "exit_code": -1,
            "timeout": False,
            "error": f"Execution failed: {str(exc)}",
            "duration_ms": 0,
            "memory_usage_mb": None,
            "status": ExecutionStatus.FAILED.value,
        }


@shared_task
def validate_code_task(code: str) -> dict:
    """Validate Python code syntax (async task).
    
    Args:
        code: Python code to validate
        
    Returns:
        Dictionary containing validation result
    """
    runner = get_docker_runner()
    is_valid, error, line, col = runner.validate_syntax(code)
    
    return {
        "valid": is_valid,
        "error": error,
        "syntax_error_line": line,
        "syntax_error_col": col,
    }


@shared_task
def cleanup_old_results():
    """Clean up old execution results from result backend."""
    logger.info("Running cleanup of old execution results")
    # Celery result backend handles expiration automatically based on result_expires setting
    return {"status": "cleanup_completed"}


@shared_task
def health_check_task():
    """Perform health check of execution infrastructure."""
    runner = get_docker_runner()
    health = runner.health_check()
    
    logger.info(f"Health check result: {health}")
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "health": health,
    }
