"""Exercise: Employee Role ABC.

Create an abstract base class for employee roles with different pay calculation
strategies.

TODO:
1. Create EmployeeRole ABC with abstract calculate_pay(hours_worked: float) -> float
2. Add abstract property role_name -> str
3. Implement HourlyEmployee with hourly_rate
4. Implement SalariedEmployee with annual_salary
5. Implement CommissionedEmployee with base_salary and commission_rate
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
        # TODO: Define abstract property
        raise NotImplementedError("role_name property must be implemented")
    
    @abstractmethod
    def calculate_pay(self, hours_worked: float) -> float:
        """Calculate pay based on hours worked.
        
        Args:
            hours_worked: Number of hours worked in the pay period.
        
        Returns:
            The calculated pay amount.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("calculate_pay must be implemented")


class HourlyEmployee(EmployeeRole):
    """Employee paid by the hour."""
    
    def __init__(self, hourly_rate: float) -> None:
        """Initialize hourly employee.
        
        Args:
            hourly_rate: Pay rate per hour (must be positive).
        
        Raises:
            ValueError: If hourly_rate is not positive.
        """
        # TODO: Validate and set hourly_rate
        raise NotImplementedError("Initialize hourly employee")
    
    @property
    def role_name(self) -> str:
        """Return role name."""
        # TODO: Return "Hourly"
        raise NotImplementedError("Return role name")
    
    def calculate_pay(self, hours_worked: float) -> float:
        """Calculate pay with overtime (1.5x for hours over 40).
        
        Args:
            hours_worked: Hours worked in the pay period.
        
        Returns:
            Total pay including overtime if applicable.
        """
        # TODO: Calculate regular pay (up to 40 hours)
        # TODO: Add overtime pay (1.5x rate for hours over 40)
        raise NotImplementedError("Calculate pay with overtime")


class SalariedEmployee(EmployeeRole):
    """Employee with fixed annual salary."""
    
    def __init__(self, annual_salary: float) -> None:
        """Initialize salaried employee.
        
        Args:
            annual_salary: Annual salary amount (must be positive).
        
        Raises:
            ValueError: If annual_salary is not positive.
        """
        # TODO: Validate and set annual_salary
        raise NotImplementedError("Initialize salaried employee")
    
    @property
    def role_name(self) -> str:
        """Return role name."""
        # TODO: Return "Salaried"
        raise NotImplementedError("Return role name")
    
    def calculate_pay(self, hours_worked: float) -> float:
        """Calculate pay for the pay period (biweekly).
        
        Note: hours_worked is ignored for salaried employees.
        
        Returns:
            Biweekly salary (annual / 26 pay periods).
        """
        # TODO: Return annual_salary / 26
        raise NotImplementedError("Calculate biweekly pay")


class CommissionedEmployee(EmployeeRole):
    """Employee with base salary plus commission."""
    
    def __init__(self, base_salary: float, commission_rate: float) -> None:
        """Initialize commissioned employee.
        
        Args:
            base_salary: Base annual salary (must be positive).
            commission_rate: Commission percentage (e.g., 0.10 for 10%).
        
        Raises:
            ValueError: If base_salary is not positive or commission_rate is negative.
        """
        # TODO: Validate and set base_salary and commission_rate
        raise NotImplementedError("Initialize commissioned employee")
    
    @property
    def role_name(self) -> str:
        """Return role name."""
        # TODO: Return "Commissioned"
        raise NotImplementedError("Return role name")
    
    def calculate_pay(self, hours_worked: float, sales_amount: float = 0.0) -> float:
        """Calculate pay with commission.
        
        Args:
            hours_worked: Hours worked (used for base pay calculation).
            sales_amount: Sales amount for commission calculation.
        
        Returns:
            Base biweekly pay plus commission.
        """
        # TODO: Calculate base biweekly pay (base_salary / 26)
        # TODO: Add commission (sales_amount * commission_rate)
        raise NotImplementedError("Calculate pay with commission")
