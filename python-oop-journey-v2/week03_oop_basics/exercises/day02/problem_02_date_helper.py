"""Problem 02: Date Helper

Topic: @staticmethod
Difficulty: Easy

Create a DateHelper class with static methods for common date utilities.

Example:
    >>> DateHelper.is_leap_year(2024)
    True
    >>> DateHelper.is_leap_year(2023)
    False
    >>> DateHelper.days_in_month(2024, 2)
    29
    >>> DateHelper.days_in_month(2023, 2)
    28
    >>> DateHelper.is_valid_date(2024, 12, 25)
    True
    >>> DateHelper.is_valid_date(2024, 13, 1)
    False

Requirements:
    - is_leap_year(year: int) -> bool: static method
    - days_in_month(year: int, month: int) -> int: static method  
    - is_valid_date(year: int, month: int, day: int) -> bool: static method
    - All methods must be @staticmethod
    - Handle leap years correctly for February
"""

from __future__ import annotations


class DateHelper:
    """Utility class for date-related operations."""
    
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
        raise NotImplementedError("Implement is_leap_year")
    
    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """Get the number of days in a given month.
        
        Args:
            year: The year (for leap year calculation)
            month: The month (1-12)
            
        Returns:
            Number of days in the month
        """
        raise NotImplementedError("Implement days_in_month")
    
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
        raise NotImplementedError("Implement is_valid_date")
