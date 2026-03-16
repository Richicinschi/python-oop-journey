"""Tests for Problem 10: Fallback Value Resolver."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_10_fallback_value_resolver import (
    fallback_value_resolver,
)


def test_fallback_first_source_succeeds() -> None:
    """Test returns first successful result."""
    sources = [
        lambda: "first",
        lambda: "second",
        lambda: "third",
    ]
    result = fallback_value_resolver(sources)
    assert result == "first"


def test_fallback_skips_failed_sources() -> None:
    """Test skips failed sources and returns first success."""
    sources = [
        lambda: (_ for _ in ()).throw(ValueError("first failed")),
        lambda: "second success",
        lambda: "third",
    ]
    result = fallback_value_resolver(sources)
    assert result == "second success"


def test_fallback_last_source_succeeds() -> None:
    """Test succeeds when only last source works."""
    sources = [
        lambda: (_ for _ in ()).throw(ValueError("fail 1")),
        lambda: (_ for _ in ()).throw(TypeError("fail 2")),
        lambda: "success",
    ]
    result = fallback_value_resolver(sources)
    assert result == "success"


def test_fallback_all_fail() -> None:
    """Test raises last exception when all sources fail."""
    sources = [
        lambda: (_ for _ in ()).throw(ValueError("first error")),
        lambda: (_ for _ in ()).throw(TypeError("second error")),
        lambda: (_ for _ in ()).throw(RuntimeError("last error")),
    ]
    
    with pytest.raises(RuntimeError) as exc_info:
        fallback_value_resolver(sources)
    
    assert "last error" in str(exc_info.value)


def test_fallback_empty_sources() -> None:
    """Test raises ValueError when no sources provided."""
    with pytest.raises(ValueError) as exc_info:
        fallback_value_resolver([])
    
    assert "No sources provided" in str(exc_info.value)


def test_fallback_single_source_success() -> None:
    """Test with single successful source."""
    result = fallback_value_resolver([lambda: 42])
    assert result == 42


def test_fallback_single_source_failure() -> None:
    """Test with single failing source."""
    with pytest.raises(ValueError):
        fallback_value_resolver([lambda: (_ for _ in ()).throw(ValueError("fail"))])


def test_fallback_different_return_types() -> None:
    """Test with different return types."""
    sources = [
        lambda: (_ for _ in ()).throw(ValueError("fail")),
        lambda: {"key": "value"},
    ]
    result = fallback_value_resolver(sources)
    assert result == {"key": "value"}


def test_fallback_various_exception_types() -> None:
    """Test handling various exception types."""
    sources = [
        lambda: (_ for _ in ()).throw(KeyError("missing")),
        lambda: (_ for _ in ()).throw(IndexError("out of range")),
        lambda: (_ for _ in ()).throw(AttributeError("no attr")),
        lambda: "finally success",
    ]
    result = fallback_value_resolver(sources)
    assert result == "finally success"


def test_fallback_zero_attempts() -> None:
    """Test that empty list is handled correctly."""
    with pytest.raises(ValueError, match="No sources"):
        fallback_value_resolver([])
