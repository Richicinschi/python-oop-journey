"""Verification endpoints for test execution."""

import logging
import re

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.core.rate_limit import rate_limit_per_minute
from api.schemas.verification import VerificationRequest, VerificationResponse, SyntaxValidationResponse
from api.services.curriculum import CurriculumService
from api.services.verification import get_verification_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Service instance
verification_service = get_verification_service()


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
@rate_limit_per_minute(60)
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

    Example request:
    ```json
    {
        "code": "def add(a, b): return a + b",
        "problem_slug": "w01d01-hello-object"
    }
    ```
    """
    # Validate code is not empty
    if not request_data.code or not request_data.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code cannot be empty",
        )

    # Run verification
    try:
        result = await verification_service.verify_and_update_progress(request_data)
        return result
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}",
        )


@router.post(
    "/verify/{problem_slug}",
    response_model=VerificationResponse,
    summary="Verify solution for specific problem",
    description="Verify code for a specific problem by slug.",
    responses={
        429: {"description": "Rate limit exceeded"},
    },
)
@rate_limit_per_minute(60)
async def verify_solution_for_problem(
    request: Request,
    problem_slug: str,
    code: str
) -> VerificationResponse:
    """Verify solution for a specific problem.

    This is a convenience endpoint that takes the problem slug from the URL.
    """
    request_data = VerificationRequest(code=code, problem_slug=problem_slug)
    return await verify_solution(request, request_data)


@router.post(
    "/validate-syntax",
    response_model=SyntaxValidationResponse,
    summary="Validate code syntax",
    description="Check if Python code has valid syntax without executing tests.",
    responses={
        429: {"description": "Rate limit exceeded"},
    },
)
@rate_limit_per_minute(120)
async def validate_syntax_endpoint(
    request: Request,
    code: str
) -> SyntaxValidationResponse:
    """Validate Python syntax without running tests.

    Returns whether the code is syntactically valid and any error messages.
    """
    try:
        # Use the Docker runner's syntax validation (AST-based, no Docker needed)
        from api.services.docker_runner import get_docker_runner
        runner = get_docker_runner()
        is_valid, error_msg, line, col = runner.validate_syntax(code)

        return SyntaxValidationResponse(
            valid=is_valid,
            error=error_msg,
            line=line,
            column=col,
            message="Syntax is valid" if is_valid else (error_msg or "Syntax error"),
        )
    except Exception as e:
        logger.error(f"Syntax validation failed: {e}")
        return SyntaxValidationResponse(
            valid=False,
            error=str(e),
            line=None,
            column=None,
            message=f"Syntax validation failed: {str(e)}",
        )


@router.get(
    "/test-info/{problem_slug}",
    summary="Get test information",
    description="Get information about tests for a problem without running them.",
    responses={
        404: {"description": "Problem not found"},
        500: {"description": "Server error"},
    },
)
async def get_test_info(problem_slug: str) -> dict:
    """Get test information for a problem.

    Returns metadata about the tests including count and names.
    """
    try:
        curriculum_service = CurriculumService()
        problem_data = curriculum_service.get_problem(problem_slug)

        if not problem_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Problem not found: {problem_slug}",
            )

        # Safely access problem data
        problem = problem_data.get("problem")
        if not problem:
            logger.error(f"Problem data missing 'problem' key for slug: {problem_slug}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Problem data is corrupted",
            )

        # Get test_code safely
        test_code = getattr(problem, 'test_code', None)
        if test_code is None:
            logger.warning(f"Problem {problem_slug} has no test_code attribute")
            test_code = ""

        # Extract test names from test code
        test_names = re.findall(r"def\s+(test_\w+)", test_code)

        return {
            "problem_slug": problem_slug,
            "problem_title": getattr(problem, 'title', 'Unknown'),
            "test_count": len(test_names),
            "test_names": test_names,
            "has_tests": len(test_names) > 0,
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error getting test info for {problem_slug}: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get test info: {str(e)}",
        )
