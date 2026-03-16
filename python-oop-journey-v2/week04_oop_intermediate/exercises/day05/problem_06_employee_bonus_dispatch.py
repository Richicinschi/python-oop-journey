"""Problem 06: Employee Bonus Dispatch.

Topic: Polymorphism
Difficulty: Medium

Create employee types with different bonus calculation strategies.
Demonstrate polymorphic bonus calculation in a payroll system.

TODO:
1. Create Employee ABC with:
   - __init__(self, name: str, base_salary: float)
   - calculate_bonus(self) -> float (abstract)
   - get_employee_type(self) -> str (abstract)
   - get_total_compensation(self) -> float (base_salary + bonus)

2. Create RegularEmployee class:
   - calculate_bonus returns base_salary * 0.05 (5% bonus)
   - get_employee_type returns "Regular"

3. Create Manager class:
   - __init__(self, name: str, base_salary: float, team_size: int)
   - calculate_bonus returns base_salary * 0.10 + (team_size * 100)
   - get_employee_type returns "Manager"

4. Create SalesPerson class:
   - __init__(self, name: str, base_salary: float, sales_amount: float)
   - calculate_bonus returns base_salary * 0.05 + (sales_amount * 0.02)
   - get_employee_type returns "Sales"

5. Create Intern class:
   - calculate_bonus returns 500.0 (fixed bonus)
   - get_employee_type returns "Intern"

6. Implement calculate_payroll(employees: list) -> dict
   that returns dict with:
   - 'total_base_salary': sum of all base salaries
   - 'total_bonus': sum of all bonuses
   - 'total_compensation': sum of all compensation
   - 'by_type': dict mapping employee types to count
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Employee(ABC):
    """Abstract base class for employees."""
    
    def __init__(self, name: str, base_salary: float) -> None:
        """Initialize employee.
        
        Args:
            name: Employee name.
            base_salary: Base salary amount.
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize employee")
    
    @abstractmethod
    def calculate_bonus(self) -> float:
        """Calculate bonus amount.
        
        Returns:
            Bonus amount as float.
        """
        raise NotImplementedError("calculate_bonus must be implemented")
    
    @abstractmethod
    def get_employee_type(self) -> str:
        """Get employee type name.
        
        Returns:
            String type identifier.
        """
        raise NotImplementedError("get_employee_type must be implemented")
    
    def get_total_compensation(self) -> float:
        """Calculate total compensation.
        
        Returns:
            Base salary plus bonus.
        """
        # TODO: Return base_salary + calculate_bonus()
        raise NotImplementedError("Implement get_total_compensation")


class RegularEmployee(Employee):
    """Regular employee implementation."""
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: 5% of base salary."""
        # TODO: Return base_salary * 0.05
        raise NotImplementedError("Implement calculate_bonus")
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        # TODO: Return "Regular"
        raise NotImplementedError("Implement get_employee_type")


class Manager(Employee):
    """Manager implementation with team size bonus."""
    
    def __init__(self, name: str, base_salary: float, team_size: int) -> None:
        """Initialize manager.
        
        Args:
            name: Manager name.
            base_salary: Base salary amount.
            team_size: Number of people in team.
        """
        # TODO: Call parent __init__ and set team_size
        raise NotImplementedError("Initialize manager")
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: 10% of base + $100 per team member."""
        # TODO: Return base_salary * 0.10 + (team_size * 100)
        raise NotImplementedError("Implement calculate_bonus")
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        # TODO: Return "Manager"
        raise NotImplementedError("Implement get_employee_type")


class SalesPerson(Employee):
    """Sales person implementation with sales commission."""
    
    def __init__(self, name: str, base_salary: float, sales_amount: float) -> None:
        """Initialize sales person.
        
        Args:
            name: Sales person name.
            base_salary: Base salary amount.
            sales_amount: Total sales amount.
        """
        # TODO: Call parent __init__ and set sales_amount
        raise NotImplementedError("Initialize sales person")
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: 5% of base + 2% of sales."""
        # TODO: Return base_salary * 0.05 + (sales_amount * 0.02)
        raise NotImplementedError("Implement calculate_bonus")
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        # TODO: Return "Sales"
        raise NotImplementedError("Implement get_employee_type")


class Intern(Employee):
    """Intern implementation with fixed bonus."""
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: fixed $500."""
        # TODO: Return 500.0
        raise NotImplementedError("Implement calculate_bonus")
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        # TODO: Return "Intern"
        raise NotImplementedError("Implement get_employee_type")


def calculate_payroll(employees: list[Employee]) -> dict:
    """Calculate payroll statistics for all employees.
    
    Args:
        employees: List of Employee instances.
    
    Returns:
        Dictionary with:
        - 'total_base_salary': sum of all base salaries
        - 'total_bonus': sum of all bonuses
        - 'total_compensation': sum of all compensation
        - 'by_type': dict mapping employee types to count
    """
    # TODO: Calculate and return payroll statistics
    raise NotImplementedError("Implement calculate_payroll")
