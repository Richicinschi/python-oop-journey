"""Verification endpoints for test execution."""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.schemas.verification import VerificationRequest, VerificationResponse
from api.services.verification import get_verification_service

router = APIRouter()

# Service instance
verification_service = get_verification_service()


def _check_rate_limit(request: Request, limit: str = "60/minute"):
    """Helper function to check rate limits.
    
    Args:
        request: The incoming request
        limit: Rate limit string (e.g., "60/minute")
    
    Raises:
        HTTPException: If rate limit is exceeded
    """
    from api.main import limiter
    from slowapi.util import get_remote_address
    
    try:
        import asyncio
        # Run the synchronous check in a thread
        loop = asyncio.get_event_loop()
        # The limiter.check is async, so we await it directly
        # But we need to handle the case where it raises an exception
        return limiter.check(request, limit, get_remote_address, [])
    except Exception:
        # We'll handle the actual check via async method
        pass


@router.post(
    "/verify",
    response_model=VerificationResponse,
    summary="Verify solution against tests",
    description="Execute learner code against test cases and return detailed results.",
    responses={
        400: {"description": "Invalid code"},
        404: {"description": "Problem not found"},
        429: {"description": "Rate limit exceeded"},
    },
)
async def verify_solution(
    request: Request,
    request_data: VerificationRequest
) -> VerificationResponse:
    """Verify a learner's solution against test cases.

    This endpoint:
    1. Validates the code syntax
    2. Loads test cases for the problem
    3. Executes tests in a sandboxed environment
    4. Returns detailed results with learner-friendly feedback

    Rate limit: 60 requests per minute per IP address.

    Example request:
    ```json
    {
        "code": "def add(a, b): return a + b",
        "problem_slug": "w01d01-hello-object"
    }
    ```
    """
    # Apply rate limiting check
    from api.main import limiter
    from slowapi.util import get_remote_address
    
    try:
        await limiter.check(request, "60/minute", get_remote_address, [])
    except Exception as e:
        if "Rate limit exceeded" in str(e):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Maximum 60 verification requests per minute allowed.",
            )
        raise
    
    # Validate code is not empty
    if not request_data.code or not request_data.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code cannot be empty",
        )

    # Run verification
    result = await verification_service.verify_and_update_progress(request_data)

    return result


@router.post(
    "/verify/{problem_slug}",
    response_model=VerificationResponse,
    summary="Verify solution for specific problem",
    description="Verify code for a specific problem by slug.",
    responses={
        429: {"description": "Rate limit exceeded"},
    },
)
async def verify_solution_for_problem(
    request: Request,
    problem_slug: str,
    code: str
) -> VerificationResponse:
    """Verify solution for a specific problem.

    This is a convenience endpoint that takes the problem slug from the URL.
    
    Rate limit: 60 requests per minute per IP address.
    """
    # Apply rate limiting check
    from api.main import limiter
    from slowapi.util import get_remote_address
    
    try:
        await limiter.check(request, "60/minute", get_remote_address, [])
    except Exception as e:
        if "Rate limit exceeded" in str(e):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Maximum 60 verification requests per minute allowed.",
            )
        raise
    
    request_data = VerificationRequest(code=code, problem_slug=problem_slug)
    return await verify_solution(request, request_data)


@router.post(
    "/validate-syntax",
    summary="Validate code syntax",
    description="Check if Python code has valid syntax without executing tests.",
)
async def validate_syntax_endpoint(
    request: Request,
    code: str
) -> dict:
    """Validate Python syntax without running tests.

    Returns whether the code is syntactically valid and any error messages.
    
    Rate limit: 60 requests per minute per IP address.
    """
    # Apply rate limiting check
    from api.main import limiter
    from slowapi.util import get_remote_address
    
    try:
        await limiter.check(request, "60/minute", get_remote_address, [])
    except Exception as e:
        if "Rate limit exceeded" in str(e):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Maximum 60 syntax validation requests per minute allowed.",
            )
        raise
    
    # Use the Docker runner's syntax validation (AST-based, no Docker needed)
    from api.services.docker_runner import get_docker_runner
    runner = get_docker_runner()
    is_valid, error_msg, line, col = runner.validate_syntax(code)

    return {
        "valid": is_valid,
        "error": error_msg,
        "line": line,
        "column": col,
        "message": "Syntax is valid" if is_valid else error_msg,
    }


@router.get(
    "/test-info/{problem_slug}",
    summary="Get test information",
    description="Get information about tests for a problem without running them.",
)
async def get_test_info(problem_slug: str) -> dict:
    """Get test information for a problem.

    Returns metadata about the tests including count and names.
    """
    from api.services.curriculum import CurriculumService

    curriculum_service = CurriculumService()
    problem_data = curriculum_service.get_problem(problem_slug)

    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem not found: {problem_slug}",
        )

    test_code = problem_data["problem"].test_code

    # Extract test names from test code
    import re

    test_names = re.findall(r"def\s+(test_\w+)", test_code)

    return {
        "problem_slug": problem_slug,
        "problem_title": problem_data["problem"].title,
        "test_count": len(test_names),
        "test_names": test_names,
        "has_tests": len(test_names) > 0,
    }
