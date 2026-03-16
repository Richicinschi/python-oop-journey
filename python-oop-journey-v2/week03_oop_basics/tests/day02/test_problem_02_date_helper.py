"""Tests for Problem 02: Date Helper."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_02_date_helper import DateHelper


class TestIsLeapYear:
    """Test suite for is_leap_year static method."""
    
    def test_typical_leap_year(self) -> None:
        """Test years divisible by 4 but not 100."""
        assert DateHelper.is_leap_year(2024) is True
        assert DateHelper.is_leap_year(2020) is True
        assert DateHelper.is_leap_year(2016) is True
    
    def test_typical_non_leap_year(self) -> None:
        """Test years not divisible by 4."""
        assert DateHelper.is_leap_year(2023) is False
        assert DateHelper.is_leap_year(2021) is False
        assert DateHelper.is_leap_year(2019) is False
    
    def test_century_non_leap_year(self) -> None:
        """Test century years not divisible by 400."""
        assert DateHelper.is_leap_year(1900) is False
        assert DateHelper.is_leap_year(2100) is False
    
    def test_century_leap_year(self) -> None:
        """Test century years divisible by 400."""
        assert DateHelper.is_leap_year(2000) is True
        assert DateHelper.is_leap_year(2400) is True


class TestDaysInMonth:
    """Test suite for days_in_month static method."""
    
    def test_31_day_months(self) -> None:
        """Test months with 31 days."""
        assert DateHelper.days_in_month(2023, 1) == 31
        assert DateHelper.days_in_month(2023, 3) == 31
        assert DateHelper.days_in_month(2023, 5) == 31
        assert DateHelper.days_in_month(2023, 7) == 31
        assert DateHelper.days_in_month(2023, 8) == 31
        assert DateHelper.days_in_month(2023, 10) == 31
        assert DateHelper.days_in_month(2023, 12) == 31
    
    def test_30_day_months(self) -> None:
        """Test months with 30 days."""
        assert DateHelper.days_in_month(2023, 4) == 30
        assert DateHelper.days_in_month(2023, 6) == 30
        assert DateHelper.days_in_month(2023, 9) == 30
        assert DateHelper.days_in_month(2023, 11) == 30
    
    def test_february_non_leap(self) -> None:
        """Test February in non-leap year."""
        assert DateHelper.days_in_month(2023, 2) == 28
    
    def test_february_leap(self) -> None:
        """Test February in leap year."""
        assert DateHelper.days_in_month(2024, 2) == 29


class TestIsValidDate:
    """Test suite for is_valid_date static method."""
    
    def test_valid_dates(self) -> None:
        """Test various valid dates."""
        assert DateHelper.is_valid_date(2024, 1, 1) is True
        assert DateHelper.is_valid_date(2024, 12, 31) is True
        assert DateHelper.is_valid_date(2024, 6, 15) is True
    
    def test_invalid_month(self) -> None:
        """Test invalid month values."""
        assert DateHelper.is_valid_date(2024, 0, 15) is False
        assert DateHelper.is_valid_date(2024, 13, 15) is False
        assert DateHelper.is_valid_date(2024, -1, 15) is False
    
    def test_invalid_day(self) -> None:
        """Test invalid day values."""
        assert DateHelper.is_valid_date(2024, 1, 0) is False
        assert DateHelper.is_valid_date(2024, 1, 32) is False
        assert DateHelper.is_valid_date(2024, 4, 31) is False  # April has 30 days
    
    def test_february_edge_cases(self) -> None:
        """Test February edge cases."""
        assert DateHelper.is_valid_date(2024, 2, 29) is True   # Leap year
        assert DateHelper.is_valid_date(2023, 2, 29) is False  # Non-leap year
        assert DateHelper.is_valid_date(2023, 2, 28) is True   # Valid
