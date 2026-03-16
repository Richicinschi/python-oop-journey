"""Solution for Problem 03: Employee Role ABC.

Demonstrates abstract methods for different pay calculation strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmployeeRole(ABC):
    """Abstract base class for employee roles.
    
    Each role has a name and its own pay calculation logic.
    """
    
    @property
    @abstractmethod
    def role_name(self) -> str:
        """Return the name of this role."""
        pass
    
    @abstractmethod
    def calculate_pay(self, hours_worked: float) -> float:
        """Calculate pay based on hours worked.
        
        Args:
            hours_worked: Number of hours worked in the pay period.
        
        Returns:
            The calculated pay amount.
        """
        pass


class HourlyEmployee(EmployeeRole):
    """Employee paid by the hour.
    
    Attributes:
        _hourly_rate: Pay rate per hour.
    """
    
    OVERTIME_THRESHOLD = 40.0
    OVERTIME_MULTIPLIER = 1.5
    
    def __init__(self, hourly_rate: float) -> None:
        """Initialize hourly employee.
        
        Args:
            hourly_rate: Pay rate per hour (must be positive).
        
        Raises:
            ValueError: If hourly_rate is not positive.
        """
        if hourly_rate <= 0:
            raise ValueError("Hourly rate must be positive")
        self._hourly_rate = float(hourly_rate)
    
    @property
    def role_name(self) -> str:
        """Return role name."""
        return "Hourly"
    
    def calculate_pay(self, hours_worked: float) -> float:
        """Calculate pay with overtime (1.5x for hours over 40).
        
        Args:
            hours_worked: Hours worked in the pay period.
        
        Returns:
            Total pay including overtime if applicable.
        """
        if hours_worked <= self.OVERTIME_THRESHOLD:
            return hours_worked * self._hourly_rate
        
        regular_hours = self.OVERTIME_THRESHOLD
        overtime_hours = hours_worked - self.OVERTIME_THRESHOLD
        
        regular_pay = regular_hours * self._hourly_rate
        overtime_pay = overtime_hours * self._hourly_rate * self.OVERTIME_MULTIPLIER
        
        return regular_pay + overtime_pay


class SalariedEmployee(EmployeeRole):
    """Employee with fixed annual salary.
    
    Attributes:
        _annual_salary: Annual salary amount.
    """
    
    PAY_PERIODS_PER_YEAR = 26  # Biweekly
    
    def __init__(self, annual_salary: float) -> None:
        """Initialize salaried employee.
        
        Args:
            annual_salary: Annual salary amount (must be positive).
        
        Raises:
            ValueError: If annual_salary is not positive.
        """
        if annual_salary <= 0:
            raise ValueError("Annual salary must be positive")
        self._annual_salary = float(annual_salary)
    
    @property
    def role_name(self) -> str:
        """Return role name."""
        return "Salaried"
    
    def calculate_pay(self, hours_worked: float) -> float:
        """Calculate pay for the pay period (biweekly).
        
        Note: hours_worked is ignored for salaried employees.
        
        Returns:
            Biweekly salary (annual / 26 pay periods).
        """
        return self._annual_salary / self.PAY_PERIODS_PER_YEAR


class CommissionedEmployee(EmployeeRole):
    """Employee with base salary plus commission.
    
    Attributes:
        _base_salary: Base annual salary.
        _commission_rate: Commission percentage (e.g., 0.10 for 10%).
    """
    
    PAY_PERIODS_PER_YEAR = 26
    
    def __init__(self, base_salary: float, commission_rate: float) -> None:
        """Initialize commissioned employee.
        
        Args:
            base_salary: Base annual salary (must be positive).
            commission_rate: Commission percentage (e.g., 0.10 for 10%).
        
        Raises:
            ValueError: If base_salary is not positive or commission_rate is negative.
        """
        if base_salary <= 0:
            raise ValueError("Base salary must be positive")
        if commission_rate < 0:
            raise ValueError("Commission rate cannot be negative")
        self._base_salary = float(base_salary)
        self._commission_rate = float(commission_rate)
    
    @property
    def role_name(self) -> str:
        """Return role name."""
        return "Commissioned"
    
    def calculate_pay(self, hours_worked: float, sales_amount: float = 0.0) -> float:
        """Calculate pay with commission.
        
        Args:
            hours_worked: Hours worked (used for base pay calculation).
            sales_amount: Sales amount for commission calculation.
        
        Returns:
            Base biweekly pay plus commission.
        """
        base_pay = self._base_salary / self.PAY_PERIODS_PER_YEAR
        commission = sales_amount * self._commission_rate
        return base_pay + commission
