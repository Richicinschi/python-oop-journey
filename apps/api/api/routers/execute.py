"""Code execution endpoints using simple subprocess-based sandbox."""

import logging
import os

from fastapi import APIRouter, HTTPException, Request, status

from api.schemas.execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    ValidationResponse,
)
from api.services.simple_execution import get_simple_execution_service

logger = logging.getLogger(__name__)
router = APIRouter()


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error},
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
        success=result.exit_code == 0 and not result.timeout,
        output=result.stdout,
        error=result.stderr if result.stderr else None,
        execution_time_ms=result.execution_time_ms,
        exit_code=result.exit_code,
        timeout=result.timeout,
    )


@router.post(
    "/execute/syntax-check",
    response_model=ValidationResponse,
    summary="Check code syntax",
    description="Validate Python code syntax without executing.",
)
async def check_syntax(code: str) -> ValidationResponse:
    """Validate Python syntax without executing."""
    service = get_simple_execution_service()
    is_valid, error = service.validate_syntax(code)
    return ValidationResponse(
        valid=is_valid,
        error=error,
    )


@router.get(
    "/execute/health",
    summary="Execution service health check",
    description="Check the health of the code execution service.",
)
async def execution_health():
    """Check execution service health."""
    return {
        "status": "healthy",
        "mode": "subprocess",
        "note": "Using simple subprocess-based execution (Render free tier)",
    }


# Legacy endpoint for backward compatibility
@router.post(
    "/execute",
    response_model=CodeExecutionResponse,
    summary="Execute Python code (legacy)",
    description="Legacy endpoint - use /execute/run instead.",
    deprecated=True,
)
async def execute_code_legacy(
    request: Request,
    exec_request: CodeExecutionRequest,
) -> CodeExecutionResponse:
    """Legacy execution endpoint."""
    return await execute_code(request, exec_request)
