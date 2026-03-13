"""Code execution endpoints."""

import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from api.schemas.execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    CodeValidationExecutionRequest,
    CodeValidationExecutionResponse,
    ExecutionJobResponse,
    ExecutionJobResult,
    ExecutionMetrics,
    ValidationResponse,
)
from api.services.execution import get_execution_service
from api.services.monitoring import get_monitor

logger = logging.getLogger(__name__)
router = APIRouter()

# Service instance
execution_service = get_execution_service()


async def get_client_info(request: Request) -> tuple[str | None, str | None]:
    """Extract client IP and user agent from request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Tuple of (ip_address, user_agent)
    """
    # Get IP address
    if "x-forwarded-for" in request.headers:
        ip = request.headers["x-forwarded-for"].split(",")[0].strip()
    else:
        ip = request.client.host if request.client else None
    
    # Get user agent
    user_agent = request.headers.get("user-agent")
    
    return ip, user_agent


@router.post(
    "/execute/run",
    response_model=CodeExecutionResponse,
    summary="Execute Python code",
    description="Safely execute Python code in a Docker sandbox with resource limits.",
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
    """Execute Python code safely.
    
    The code is executed in an isolated Docker container with:
    - 256MB memory limit
    - 0.5 CPU limit
    - No network access
    - Read-only filesystem
    - 10 second timeout (configurable up to 60s)
    """
    # Get client info
    ip_address, user_agent = await get_client_info(request)
    
    # Check rate limit (TODO: Get actual user_id from auth)
    user_id = None  # Will come from auth token
    allowed, current_count, limit = await execution_service.check_rate_limit(
        user_id, ip_address
    )
    
    if not allowed:
        logger.warning(f"Rate limit exceeded for {ip_address}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {limit} executions per minute.",
        )
    
    # Validate syntax first
    validation = await execution_service.validate_syntax(exec_request.code)
    if not validation.valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": validation.error,
                "line": validation.syntax_error_line,
                "column": validation.syntax_error_col,
            },
        )
    
    # Execute the code
    result = await execution_service.execute(
        exec_request,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    return result


@router.post(
    "/execute/async",
    response_model=ExecutionJobResponse,
    summary="Execute Python code asynchronously",
    description="Submit code for async execution and get a job ID to poll for results.",
    responses={
        400: {"description": "Invalid code"},
        429: {"description": "Rate limit exceeded"},
    },
)
async def execute_code_async(
    request: Request,
    exec_request: CodeExecutionRequest,
) -> ExecutionJobResponse:
    """Submit code for asynchronous execution.
    
    Returns a job ID that can be used to poll for results via /execute/jobs/{job_id}.
    """
    # Get client info
    ip_address, user_agent = await get_client_info(request)
    
    # Check rate limit
    user_id = None
    allowed, current_count, limit = await execution_service.check_rate_limit(
        user_id, ip_address
    )
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {limit} executions per minute.",
        )
    
    # Validate syntax
    validation = await execution_service.validate_syntax(exec_request.code)
    if not validation.valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": validation.error,
                "line": validation.syntax_error_line,
                "column": validation.syntax_error_col,
            },
        )
    
    # Submit async job
    result = await execution_service.execute_async(exec_request, user_id=user_id)
    return result


@router.get(
    "/execute/jobs/{job_id}",
    response_model=ExecutionJobResult,
    summary="Get async execution result",
    description="Get the status and result of an asynchronous execution job.",
    responses={
        404: {"description": "Job not found"},
    },
)
async def get_execution_job(job_id: str) -> ExecutionJobResult:
    """Get result of an asynchronous execution job."""
    result = await execution_service.get_job_result(job_id)
    return result


@router.post(
    "/execute/validate",
    response_model=CodeValidationExecutionResponse,
    summary="Execute and validate code with tests",
    description="Execute code and run test cases against it.",
    responses={
        400: {"description": "Invalid code"},
        429: {"description": "Rate limit exceeded"},
    },
)
async def validate_code_with_tests(
    request: Request,
    validation_request: CodeValidationExecutionRequest,
) -> CodeValidationExecutionResponse:
    """Execute code with test validation.
    
    Runs the provided code and then executes the test code against it.
    Returns detailed test results including pass/fail status.
    """
    # Get client info
    ip_address, user_agent = await get_client_info(request)
    
    # Check rate limit
    user_id = None
    allowed, current_count, limit = await execution_service.check_rate_limit(
        user_id, ip_address
    )
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {limit} executions per minute.",
        )
    
    # Validate syntax first
    validation = await execution_service.validate_syntax(validation_request.code)
    if not validation.valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": validation.error,
                "line": validation.syntax_error_line,
                "column": validation.syntax_error_col,
            },
        )
    
    # Execute with tests
    result = await execution_service.validate_and_test(
        validation_request,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    return result


@router.post(
    "/execute/syntax-check",
    response_model=ValidationResponse,
    summary="Check code syntax",
    description="Validate Python code syntax without executing.",
)
async def check_syntax(code: str) -> ValidationResponse:
    """Validate Python syntax without executing."""
    result = await execution_service.validate_syntax(code)
    return result


@router.get(
    "/execute/metrics",
    response_model=ExecutionMetrics,
    summary="Get execution metrics",
    description="Get execution statistics and metrics for monitoring.",
)
async def get_metrics(hours: int = 24) -> ExecutionMetrics:
    """Get execution metrics for the specified time period.
    
    Args:
        hours: Number of hours to include (default: 24, max: 168)
    """
    if hours < 1 or hours > 168:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hours must be between 1 and 168",
        )
    
    metrics = await execution_service.get_metrics(hours)
    return metrics


@router.get(
    "/execute/health",
    summary="Execution service health check",
    description="Check the health of the Docker execution infrastructure.",
)
async def execution_health():
    """Check execution service health."""
    from api.services.docker_runner import get_docker_runner
    
    runner = get_docker_runner()
    health = runner.health_check()
    
    if not health["docker_available"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "error": "Docker not available",
                "details": health,
            },
        )
    
    if not health["image_available"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "error": f"Sandbox image not available",
                "details": health,
            },
        )
    
    return {
        "status": "healthy" if health["can_run_containers"] else "degraded",
        "details": health,
    }


# Legacy endpoints for backward compatibility
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
