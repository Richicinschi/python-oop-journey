"""Curriculum schemas."""

from pydantic import BaseModel, Field


class Problem(BaseModel):
    """Problem schema."""

    slug: str = Field(..., description="Unique problem identifier")
    title: str = Field(..., description="Problem title")
    description: str = Field(default="", description="Problem description")
    difficulty: str = Field(default="medium", description="Problem difficulty")
    starter_code: str = Field(default="", description="Starter code template")
    test_code: str = Field(default="", description="Test cases")
    hints: list[str] = Field(default_factory=list, description="Problem hints")

    model_config = {"extra": "allow"}


class Day(BaseModel):
    """Day schema."""

    slug: str = Field(..., description="Unique day identifier")
    title: str = Field(..., description="Day title")
    description: str = Field(default="", description="Day description")
    problems: list[Problem] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class Week(BaseModel):
    """Week schema."""

    slug: str = Field(..., description="Unique week identifier")
    title: str = Field(..., description="Week title")
    description: str = Field(default="", description="Week description")
    theme: str = Field(default="", description="Week theme")
    days: list[Day] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class Curriculum(BaseModel):
    """Full curriculum schema."""

    version: str = Field(default="1.0.0", description="Curriculum version")
    weeks: list[Week] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ProblemDetailResponse(BaseModel):
    """Problem detail response with week and day context."""

    week: Week
    day: Day
    problem: Problem

    model_config = {"extra": "allow"}


class ProblemListItem(BaseModel):
    """Problem list item for list endpoint."""

    slug: str
    title: str
    difficulty: str
    week_slug: str
    week_title: str
    day_slug: str
    day_title: str

    model_config = {"extra": "allow"}
