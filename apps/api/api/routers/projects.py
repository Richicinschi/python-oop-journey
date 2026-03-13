"""Project execution endpoints for multi-file projects."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request, status

from api.schemas.execution import (
    ProjectExecutionRequest,
    ProjectExecutionResponse,
    ProjectMetadata,
    ProjectRunRequest,
    ProjectSaveRequest,
    ProjectSaveResponse,
    ProjectSubmissionResponse,
    ProjectTemplate,
    ProjectTestRequest,
    ProjectTestResult,
    ProjectValidationResponse,
)
from api.services.project_execution import get_project_execution_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Service instance
project_service = get_project_execution_service()


@router.get(
    "/projects/{slug}",
    response_model=ProjectMetadata,
    summary="Get project metadata",
    description="Returns project metadata including file structure and templates.",
    responses={
        404: {"description": "Project not found"},
    },
)
async def get_project(slug: str) -> ProjectMetadata:
    """Get project metadata by slug.

    Returns project information including:
    - Project metadata (title, description)
    - File structure
    - Starter templates
    - Required files
    """
    # Load from curriculum service
    from api.services.curriculum import CurriculumService

    curriculum_service = CurriculumService()

    # Try to find project in curriculum
    # Projects are typically associated with weeks
    week = curriculum_service.get_week(slug)

    if week:
        # Build file structure from week data
        file_structure = _build_file_structure(week)

        return ProjectMetadata(
            slug=slug,
            title=week.title,
            description=week.description,
            file_structure=file_structure,
            templates=_get_default_templates(),
            required_files=["src/main.py", "README.md"],
            entry_point="src/main.py",
            week_slug=slug,
        )

    # Check if it's a project-specific slug
    # For now, return a default project structure
    if "project" in slug.lower():
        return ProjectMetadata(
            slug=slug,
            title=f"Project: {slug}",
            description="Multi-file project exercise",
            file_structure={
                "src": {
                    "type": "directory",
                    "children": {
                        "__init__.py": {"type": "file"},
                        "main.py": {"type": "file"},
                    },
                },
                "tests": {
                    "type": "directory",
                    "children": {
                        "__init__.py": {"type": "file"},
                        "test_main.py": {"type": "file"},
                    },
                },
                "README.md": {"type": "file"},
            },
            templates=_get_default_templates(),
            required_files=["src/main.py"],
            entry_point="src/main.py",
            week_slug=slug.replace("-project", ""),
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project '{slug}' not found",
    )


@router.post(
    "/projects/{slug}/run",
    response_model=ProjectExecutionResponse,
    summary="Run project",
    description="Execute a multi-file project.",
    responses={
        400: {"description": "Invalid request or missing files"},
        422: {"description": "Validation error"},
    },
)
async def run_project(
    slug: str,
    request: ProjectRunRequest,
) -> ProjectExecutionResponse:
    """Run a multi-file project.

    Executes the project entry point in a Docker sandbox with:
    - 512MB memory limit
    - 1 CPU core
    - 30 second timeout
    - No network access

    Request body:
    - files: Dictionary mapping file paths to content
    - entry_point: Optional override for entry point (default: src/main.py)
    """
    # Validate project exists
    project_meta = await get_project(slug)

    # Use default entry point if not specified
    entry_point = request.entry_point or project_meta.entry_point

    # Validate entry point exists in files
    if entry_point not in request.files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry point '{entry_point}' not found in files",
        )

    # Execute project
    result = await project_service.execute_project(
        files=request.files,
        entry_point=entry_point,
        timeout=30,
    )

    return ProjectExecutionResponse(
        success=result.success,
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.exit_code,
        timeout=result.timeout,
        error=result.error,
        execution_time_ms=result.duration_ms,
    )


@router.post(
    "/projects/{slug}/test",
    response_model=ProjectTestResult,
    summary="Run project tests",
    description="Run pytest on the project tests/ directory.",
    responses={
        400: {"description": "Invalid request"},
    },
)
async def run_project_tests(
    slug: str,
    request: ProjectTestRequest,
) -> ProjectTestResult:
    """Run tests for a multi-file project.

    Runs pytest on the tests/ directory and returns:
    - Per-test results (pass/fail)
    - Test summary
    - stdout/stderr output

    Request body:
    - files: Dictionary mapping file paths to content
    - test_path: Optional specific test file or directory (default: tests/)
    """
    test_path = request.test_path or "tests"

    # Run tests
    result = await project_service.run_project_tests(
        files=request.files,
        test_path=test_path,
        timeout=30,
    )

    return result


@router.post(
    "/projects/{slug}/validate",
    response_model=ProjectValidationResponse,
    summary="Validate project",
    description="Validate project files (syntax, imports, required files).",
)
async def validate_project(
    slug: str,
    files: dict[str, str],
) -> ProjectValidationResponse:
    """Validate project files.

    Performs the following validations:
    - Checks all required files are present
    - Validates Python syntax for each .py file
    - Checks imports can be resolved
    """
    # Get project metadata for required files
    try:
        project_meta = await get_project(slug)
        required_files = project_meta.required_files
    except HTTPException:
        required_files = None

    # Validate project
    result = await project_service.validate_project(
        files=files,
        required_files=required_files,
    )

    return result


@router.post(
    "/projects/{slug}/save",
    response_model=ProjectSaveResponse,
    summary="Save project state",
    description="Save current project state to drafts.",
)
async def save_project(
    slug: str,
    request: ProjectSaveRequest,
) -> ProjectSaveResponse:
    """Save project state.

    Saves the current project files to the user's drafts.
    Can be used for manual saves or auto-saves.

    Request body:
    - files: Dictionary mapping file paths to content
    - is_auto_save: Whether this is an auto-save
    """
    # TODO: Integrate with draft service to persist to database
    # For now, return success response

    logger.info(f"Saving project '{slug}' (auto_save={request.is_auto_save})")

    return ProjectSaveResponse(
        success=True,
        message="Project saved successfully",
    )


@router.post(
    "/projects/{slug}/submit",
    response_model=ProjectSubmissionResponse,
    summary="Submit project",
    description="Submit final project and run all tests.",
    responses={
        400: {"description": "Validation failed"},
    },
)
async def submit_project(
    slug: str,
    request: ProjectRunRequest,
) -> ProjectSubmissionResponse:
    """Submit project for final evaluation.

    This endpoint:
    1. Validates the project
    2. Runs all tests
    3. Marks as submitted if tests pass
    4. Creates a snapshot

    Request body:
    - files: Dictionary mapping file paths to content
    - entry_point: Optional override for entry point
    """
    # Validate project first
    validation = await validate_project(slug, request.files)
    if not validation.valid:
        return ProjectSubmissionResponse(
            success=False,
            all_tests_passed=False,
            message=f"Validation failed: {validation.message}",
        )

    # Run all tests
    test_result = await run_project_tests(
        slug,
        ProjectTestRequest(files=request.files),
    )

    all_passed = test_result.success and test_result.summary.failed == 0

    # TODO: Persist submission to database
    # TODO: Update user progress

    return ProjectSubmissionResponse(
        success=True,
        all_tests_passed=all_passed,
        test_result=test_result,
        message="All tests passed!" if all_passed else "Some tests failed",
    )


@router.get(
    "/projects/{slug}/template",
    response_model=ProjectTemplate,
    summary="Get project template",
    description="Get the starter template for a project.",
)
async def get_project_template(slug: str) -> ProjectTemplate:
    """Get project starter template.

    Returns the default file structure and starter code for a project.
    """
    project_meta = await get_project(slug)

    return ProjectTemplate(
        slug=slug,
        title=project_meta.title,
        description=project_meta.description,
        files=_get_template_files(project_meta),
        required_files=project_meta.required_files,
        entry_point=project_meta.entry_point,
        week_slug=project_meta.week_slug,
    )


def _build_file_structure(week: Any) -> dict[str, Any]:
    """Build file structure from week data."""
    # Default project structure
    return {
        "src": {
            "type": "directory",
            "children": {
                "__init__.py": {"type": "file"},
                "main.py": {"type": "file"},
            },
        },
        "tests": {
            "type": "directory",
            "children": {
                "__init__.py": {"type": "file"},
                "test_main.py": {"type": "file"},
            },
        },
        "README.md": {"type": "file"},
    }


def _get_default_templates() -> dict[str, str]:
    """Get default file templates."""
    return {
        "src/__init__.py": "",
        "src/main.py": '''def main():
    """Main entry point."""
    pass


if __name__ == "__main__":
    main()
''',
        "tests/__init__.py": "",
        "tests/test_main.py": '''import unittest


class TestMain(unittest.TestCase):
    """Tests for main module."""

    def test_example(self):
        """Example test."""
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',
        "README.md": """# Project

## Description

Add your project description here.

## Running

```bash
python src/main.py
```

## Testing

```bash
pytest tests/
```
""",
    }


def _get_template_files(project_meta: ProjectMetadata) -> list:
    """Get template files for a project."""
    from api.schemas.execution import ProjectTemplateFile

    templates = project_meta.templates or _get_default_templates()
    files = []

    for path, content in templates.items():
        files.append(
            ProjectTemplateFile(
                path=path,
                content=content,
                is_directory=False,
            )
        )

    return files
