"""Schemas for AI-powered hints and code assistance."""

from pydantic import BaseModel, Field


class AIHint(BaseModel):
    """AI-generated hint for a problem."""
    
    hint: str = Field(..., description="The hint text")
    relevant_lines: list[int] = Field(
        default_factory=list, 
        description="Line numbers in user's code referenced by this hint"
    )
    explanation: str = Field(
        default="", 
        description="Brief explanation of what this hint addresses"
    )
    hint_level: int = Field(
        default=1, 
        ge=1, 
        le=3, 
        description="Level of the hint (1-3)"
    )


class AIHintRequest(BaseModel):
    """Request to generate an AI hint."""
    
    problem_slug: str = Field(..., description="Problem identifier")
    code: str = Field(..., description="User's current code")
    test_results: dict | None = Field(
        None, 
        description="Optional test results to inform hint generation"
    )
    hint_level: int = Field(
        default=1, 
        ge=1, 
        le=3, 
        description="Hint level (1=conceptual, 2=structural, 3=specific)"
    )
    previous_hints: list[str] = Field(
        default_factory=list, 
        description="Previously shown hints to avoid repetition"
    )


class AIHintResponse(BaseModel):
    """Response with AI-generated hint."""
    
    hint: str = Field(..., description="The generated hint")
    relevant_lines: list[int] = Field(
        default_factory=list, 
        description="Line numbers referenced in the hint"
    )
    explanation: str = Field(..., description="Explanation of the hint")
    hint_level: int = Field(..., description="Level of hint provided")


class AIErrorExplanation(BaseModel):
    """AI explanation of an error."""
    
    explanation: str = Field(..., description="Plain English explanation of the error")
    suggestion: str = Field(..., description="Suggestion on how to fix the error")
    relevant_lines: list[int] = Field(
        default_factory=list, 
        description="Line numbers where the error likely occurs"
    )


class AIErrorRequest(BaseModel):
    """Request to explain an error."""
    
    error_message: str = Field(..., description="The error message to explain")
    code: str = Field(..., description="User's code that generated the error")
    problem_slug: str | None = Field(
        None, 
        description="Optional problem identifier for context"
    )


class AIErrorResponse(BaseModel):
    """Response with error explanation."""
    
    explanation: str = Field(..., description="Plain English explanation")
    suggestion: str = Field(..., description="How to approach fixing the error")
    relevant_lines: list[int] = Field(
        default_factory=list, 
        description="Line numbers to focus on"
    )


class CodeReviewRequest(BaseModel):
    """Request for AI code review."""
    
    files: dict[str, str] = Field(
        ..., 
        description="Dictionary of file paths to content"
    )
    project_slug: str = Field(..., description="Project identifier")
    rubric: list[dict] | None = Field(
        None, 
        description="Optional rubric criteria to check against"
    )


class CodeReviewResult(BaseModel):
    """Result of AI code review."""
    
    overall_feedback: str = Field(..., description="Summary of the review")
    strengths: list[str] = Field(
        default_factory=list, 
        description="What was done well"
    )
    improvements: list[str] = Field(
        default_factory=list, 
        description="Suggested improvements"
    )
    rubric_assessment: dict = Field(
        default_factory=dict, 
        description="Assessment against each rubric criterion"
    )
    encouragement: str = Field(
        default="", 
        description="Final encouraging message"
    )


class AIHintFeedback(BaseModel):
    """User feedback on an AI hint."""
    
    hint_id: str | None = Field(
        None, 
        description="Optional hint identifier"
    )
    problem_slug: str = Field(..., description="Problem identifier")
    hint_level: int = Field(..., description="Level of hint")
    was_helpful: bool = Field(..., description="Whether the hint was helpful")
    feedback_text: str | None = Field(
        None, 
        description="Optional detailed feedback"
    )


class AIReportRequest(BaseModel):
    """Request to report a problematic AI hint."""
    
    problem_slug: str = Field(..., description="Problem identifier")
    hint_level: int = Field(..., description="Level of problematic hint")
    hint_text: str = Field(..., description="The problematic hint text")
    reason: str = Field(..., description="Reason for reporting")
    user_code: str | None = Field(
        None, 
        description="Optional user's code for context"
    )
