"""Solution for Problem 02: Date Helper."""

from __future__ import annotations


class DateHelper:
    """Utility class for date-related operations."""
    
    _days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Check if a year is a leap year.
        
        A year is a leap year if:
        - Divisible by 4, but not by 100, OR
        - Divisible by 400
        
        Args:
            year: The year to check
            
        Returns:
            True if leap year, False otherwise
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """Get the number of days in a given month.
        
        Args:
            year: The year (for leap year calculation)
            month: The month (1-12)
            
        Returns:
            Number of days in the month
        """
        if month == 2 and DateHelper.is_leap_year(year):
            return 29
        return DateHelper._days_in_months[month]
    
    @staticmethod
    def is_valid_date(year: int, month: int, day: int) -> bool:
        """Check if a date is valid.
        
        Args:
            year: The year
            month: The month (1-12)
            day: The day (1-31 depending on month)
            
        Returns:
            True if date is valid, False otherwise
        """
        if month < 1 or month > 12:
            return False
        if day < 1:
            return False
        max_days = DateHelper.days_in_month(year, month)
        return day <= max_days
