"""Solution for Problem 06: Employee Bonus Dispatch.

Demonstrates polymorphic bonus calculation in a payroll system.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Employee(ABC):
    """Abstract base class for employees.
    
    Attributes:
        name: Employee name.
        base_salary: Base salary amount.
    """
    
    def __init__(self, name: str, base_salary: float) -> None:
        """Initialize employee.
        
        Args:
            name: Employee name.
            base_salary: Base salary amount.
        """
        self.name = name
        self.base_salary = base_salary
    
    @abstractmethod
    def calculate_bonus(self) -> float:
        """Calculate bonus amount.
        
        Returns:
            Bonus amount as float.
        """
        pass
    
    @abstractmethod
    def get_employee_type(self) -> str:
        """Get employee type name.
        
        Returns:
            String type identifier.
        """
        pass
    
    def get_total_compensation(self) -> float:
        """Calculate total compensation.
        
        Returns:
            Base salary plus bonus.
        """
        return self.base_salary + self.calculate_bonus()


class RegularEmployee(Employee):
    """Regular employee implementation."""
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: 5% of base salary."""
        return self.base_salary * 0.05
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        return "Regular"


class Manager(Employee):
    """Manager implementation with team size bonus.
    
    Attributes:
        team_size: Number of people in team.
    """
    
    def __init__(self, name: str, base_salary: float, team_size: int) -> None:
        """Initialize manager.
        
        Args:
            name: Manager name.
            base_salary: Base salary amount.
            team_size: Number of people in team.
        """
        super().__init__(name, base_salary)
        self.team_size = team_size
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: 10% of base + $100 per team member."""
        return self.base_salary * 0.10 + (self.team_size * 100)
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        return "Manager"


class SalesPerson(Employee):
    """Sales person implementation with sales commission.
    
    Attributes:
        sales_amount: Total sales amount.
    """
    
    def __init__(self, name: str, base_salary: float, sales_amount: float) -> None:
        """Initialize sales person.
        
        Args:
            name: Sales person name.
            base_salary: Base salary amount.
            sales_amount: Total sales amount.
        """
        super().__init__(name, base_salary)
        self.sales_amount = sales_amount
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: 5% of base + 2% of sales."""
        return self.base_salary * 0.05 + (self.sales_amount * 0.02)
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        return "Sales"


class Intern(Employee):
    """Intern implementation with fixed bonus."""
    
    def calculate_bonus(self) -> float:
        """Calculate bonus: fixed $500."""
        return 500.0
    
    def get_employee_type(self) -> str:
        """Return employee type."""
        return "Intern"


def calculate_payroll(employees: list[Employee]) -> dict:
    """Calculate payroll statistics for all employees.
    
    This function demonstrates polymorphism - it works with any
    Employee subclass without knowing the specific type.
    
    Args:
        employees: List of Employee instances.
    
    Returns:
        Dictionary with payroll statistics.
    """
    total_base_salary = 0.0
    total_bonus = 0.0
    total_compensation = 0.0
    by_type: dict[str, int] = {}
    
    for employee in employees:
        bonus = employee.calculate_bonus()
        compensation = employee.get_total_compensation()
        
        total_base_salary += employee.base_salary
        total_bonus += bonus
        total_compensation += compensation
        
        emp_type = employee.get_employee_type()
        by_type[emp_type] = by_type.get(emp_type, 0) + 1
    
    return {
        "total_base_salary": round(total_base_salary, 2),
        "total_bonus": round(total_bonus, 2),
        "total_compensation": round(total_compensation, 2),
        "by_type": by_type,
    }
