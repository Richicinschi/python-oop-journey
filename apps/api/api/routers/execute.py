"""Code execution endpoints using simple subprocess-based sandbox."""

import logging
import os

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from api.core.rate_limit import rate_limit_per_minute
from api.schemas.execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    ValidationResponse,
)
from api.services.simple_execution import get_simple_execution_service

logger = logging.getLogger(__name__)
router = APIRouter()


class ExecutionHealthResponse(BaseModel):
    """Execution service health check response."""
    status: str
    mode: str
    platform: str
    note: str


@router.post(
    "/execute/run",
    response_model=CodeExecutionResponse,
    summary="Execute Python code",
    description="Safely execute Python code with resource limits.",
    responses={
        400: {"description": "Invalid code or syntax error"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Execution service unavailable"},
    },
)
@rate_limit_per_minute(30)
async def execute_code(
    request: Request,
    exec_request: CodeExecutionRequest,
) -> CodeExecutionResponse:
    """Execute Python code safely in a subprocess with resource limits."""
    # Get execution service
    service = get_simple_execution_service()
    
    # Validate syntax first
    is_valid, error = service.validate_syntax(exec_request.code)
    if not is_valid:
        # Return a proper response instead of raising exception
        # This allows frontend to handle syntax errors gracefully
        return CodeExecutionResponse(
            success=False,
            output="",
            error=error,
            execution_time_ms=0,
            exit_code=1,
            timeout=False,
        )
    
    # Execute the code (synchronous call wrapped)
    import asyncio
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,  # Default executor
        service.execute,
        exec_request
    )
    
    return CodeExecutionResponse(
        success=result.success,
        output=result.stdout,
        error=result.stderr if result.stderr else None,
        execution_time_ms=result.duration_ms,
        exit_code=result.exit_code,
        timeout=result.timeout,
    )


@router.post(
    "/execute/syntax-check",
    response_model=ValidationResponse,
    summary="Check code syntax",
    description="Validate Python code syntax without executing.",
)
@rate_limit_per_minute(60)
async def check_syntax(
    request: Request,
    exec_request: CodeExecutionRequest
) -> ValidationResponse:
    """Validate Python syntax without executing."""
    service = get_simple_execution_service()
    is_valid, error = service.validate_syntax(exec_request.code)
    
    # Parse line/column from error message if syntax error
    line = None
    col = None
    if error and "line" in error.lower():
        try:
            # Try to extract line and column from error message
            import re
            line_match = re.search(r'line (\d+)', error, re.IGNORECASE)
            col_match = re.search(r'column (\d+)', error, re.IGNORECASE)
            if line_match:
                try:
                    line = int(line_match.group(1))
                except (ValueError, IndexError) as e:
                    logger.warning(f"Failed to parse line number from error: {e}")
            if col_match:
                try:
                    col = int(col_match.group(1))
                except (ValueError, IndexError) as e:
                    logger.warning(f"Failed to parse column number from error: {e}")
        except re.error as e:
            logger.error(f"Regex error parsing syntax error message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing syntax error message: {e}")
    
    return ValidationResponse(
        valid=is_valid,
        error=error,
        syntax_error_line=line,
        syntax_error_col=col,
    )


@router.get(
    "/execute/health",
    response_model=ExecutionHealthResponse,
    summary="Execution service health check",
    description="Check the health of the code execution service.",
)
async def execution_health():
    """Check execution service health."""
    # Quick test to verify execution works
    service = get_simple_execution_service()
    test_result = service.validate_syntax("print('hello')")
    
    return ExecutionHealthResponse(
        status="healthy" if test_result[0] else "unhealthy",
        mode="subprocess",
        platform="unix" if os.name == 'posix' else "windows/other",
        note="Using simple subprocess-based execution (Render free tier)",
    )


# Legacy endpoint for backward compatibility
@router.post(
    "/execute",
    response_model=CodeExecutionResponse,
    summary="Execute Python code (legacy)",
    description="Legacy endpoint - use /execute/run instead.",
    deprecated=True,
    responses={
        429: {"description": "Rate limit exceeded"},
    },
)
@rate_limit_per_minute(30)
async def execute_code_legacy(
    request: Request,
    exec_request: CodeExecutionRequest,
) -> CodeExecutionResponse:
    """Legacy execution endpoint."""
    return await execute_code(request, exec_request)
