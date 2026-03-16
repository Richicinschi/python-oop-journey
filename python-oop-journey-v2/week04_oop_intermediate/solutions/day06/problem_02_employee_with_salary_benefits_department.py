"""Problem 02: Employee with Salary, Benefits, and Department.

Complex composition example showing how to compose multiple components
to build an employee system without deep inheritance hierarchies.

Classes to implement:
- Salary: Handles salary calculation and raises
- Benefits: Manages employee benefits
- Department: Represents an organizational unit
- Employee: Composes Salary, Benefits, and Department

Example:
    >>> dept = Department("Engineering", "Alice")
    >>> salary = Salary(80000)
    >>> benefits = Benefits(["Health", "Dental"])
    >>> emp = Employee("Bob", salary, benefits, dept)
    >>> emp.get_total_compensation()
    88000.0
"""

from __future__ import annotations

from typing import Any


class Salary:
    """Manages salary information and calculations.
    
    Attributes:
        base_amount: The base salary amount.
        bonus_percentage: Current bonus percentage (default 10%).
    """
    
    DEFAULT_BONUS_PCT = 10.0
    
    def __init__(self, base_amount: float, bonus_percentage: float | None = None) -> None:
        """Initialize a salary.
        
        Args:
            base_amount: The base salary amount.
            bonus_percentage: Optional bonus percentage (defaults to 10%).
        """
        self._base_amount = base_amount
        self._bonus_percentage = bonus_percentage if bonus_percentage is not None else self.DEFAULT_BONUS_PCT
    
    @property
    def base_amount(self) -> float:
        """Get the base salary amount.
        
        Returns:
            The base salary.
        """
        return self._base_amount
    
    @property
    def bonus_percentage(self) -> float:
        """Get the current bonus percentage.
        
        Returns:
            The bonus percentage.
        """
        return self._bonus_percentage
    
    def give_raise(self, percentage: float) -> float:
        """Give a raise by a percentage.
        
        Args:
            percentage: Raise percentage (e.g., 5.0 for 5%).
        
        Returns:
            The new base salary amount.
        """
        self._base_amount *= (1 + percentage / 100)
        return self._base_amount
    
    def set_bonus_percentage(self, percentage: float) -> None:
        """Set the bonus percentage.
        
        Args:
            percentage: New bonus percentage.
        """
        self._bonus_percentage = percentage
    
    def calculate_bonus(self) -> float:
        """Calculate the bonus amount.
        
        Returns:
            The calculated bonus.
        """
        return self._base_amount * (self._bonus_percentage / 100)
    
    def get_total(self) -> float:
        """Get total compensation (base + bonus).
        
        Returns:
            Total compensation amount.
        """
        return self._base_amount + self.calculate_bonus()
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted salary description.
        """
        return f"${self._base_amount:,.2f} + {self._bonus_percentage}% bonus"


class Benefits:
    """Manages employee benefits.
    
    Attributes:
        benefit_types: List of benefit types.
        benefit_value: Estimated monetary value of benefits.
    """
    
    BENEFIT_VALUES: dict[str, float] = {
        "Health": 8000.0,
        "Dental": 1200.0,
        "Vision": 600.0,
        "401k Match": 5000.0,
        "Gym": 600.0,
    }
    
    def __init__(self, benefit_types: list[str] | None = None) -> None:
        """Initialize benefits.
        
        Args:
            benefit_types: List of benefit type names.
        """
        self._benefit_types = benefit_types.copy() if benefit_types else []
    
    def add_benefit(self, benefit_type: str) -> None:
        """Add a benefit.
        
        Args:
            benefit_type: The type of benefit to add.
        """
        if benefit_type not in self._benefit_types:
            self._benefit_types.append(benefit_type)
    
    def remove_benefit(self, benefit_type: str) -> bool:
        """Remove a benefit.
        
        Args:
            benefit_type: The type of benefit to remove.
        
        Returns:
            True if removed, False if not found.
        """
        if benefit_type in self._benefit_types:
            self._benefit_types.remove(benefit_type)
            return True
        return False
    
    def get_benefits(self) -> list[str]:
        """Get list of benefits.
        
        Returns:
            Copy of the benefit types list.
        """
        return self._benefit_types.copy()
    
    def calculate_value(self) -> float:
        """Calculate total monetary value of benefits.
        
        Returns:
            Total value of all benefits.
        """
        return sum(
            self.BENEFIT_VALUES.get(benefit, 0.0)
            for benefit in self._benefit_types
        )
    
    def has_benefit(self, benefit_type: str) -> bool:
        """Check if employee has a specific benefit.
        
        Args:
            benefit_type: The benefit type to check.
        
        Returns:
            True if the benefit is present.
        """
        return benefit_type in self._benefit_types
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Comma-separated list of benefits.
        """
        return ", ".join(self._benefit_types) if self._benefit_types else "None"


class Department:
    """Represents an organizational department.
    
    Attributes:
        name: Department name.
        manager: Name of the department manager.
    """
    
    def __init__(self, name: str, manager: str) -> None:
        """Initialize a department.
        
        Args:
            name: Department name.
            manager: Name of the department manager.
        """
        self._name = name
        self._manager = manager
        self._employees: list[str] = []
    
    @property
    def name(self) -> str:
        """Get department name.
        
        Returns:
            The department name.
        """
        return self._name
    
    @property
    def manager(self) -> str:
        """Get department manager name.
        
        Returns:
            The manager's name.
        """
        return self._manager
    
    def change_manager(self, new_manager: str) -> None:
        """Change the department manager.
        
        Args:
            new_manager: Name of the new manager.
        """
        self._manager = new_manager
    
    def add_employee(self, employee_name: str) -> None:
        """Add an employee to the department.
        
        Args:
            employee_name: Name of the employee.
        """
        if employee_name not in self._employees:
            self._employees.append(employee_name)
    
    def remove_employee(self, employee_name: str) -> bool:
        """Remove an employee from the department.
        
        Args:
            employee_name: Name of the employee to remove.
        
        Returns:
            True if removed, False if not found.
        """
        if employee_name in self._employees:
            self._employees.remove(employee_name)
            return True
        return False
    
    def get_employee_count(self) -> int:
        """Get number of employees in department.
        
        Returns:
            Count of employees.
        """
        return len(self._employees)
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted department description.
        """
        return f"{self._name} (Manager: {self._manager})"


class Employee:
    """An employee composed of Salary, Benefits, and Department.
    
    This demonstrates complex composition - an employee is not a salary,
    nor a benefits package, nor a department. An employee HAS these things.
    
    Attributes:
        name: Employee name.
        salary: Salary object.
        benefits: Benefits object.
        department: Department object.
    """
    
    def __init__(
        self,
        name: str,
        salary: Salary,
        benefits: Benefits,
        department: Department
    ) -> None:
        """Initialize an employee.
        
        Args:
            name: Employee name.
            salary: Salary object.
            benefits: Benefits object.
            department: Department object.
        """
        self._name = name
        self._salary = salary
        self._benefits = benefits
        self._department = department
        department.add_employee(name)
    
    @property
    def name(self) -> str:
        """Get employee name.
        
        Returns:
            The employee's name.
        """
        return self._name
    
    @property
    def salary(self) -> Salary:
        """Get salary component.
        
        Returns:
            The Salary object.
        """
        return self._salary
    
    @property
    def benefits(self) -> Benefits:
        """Get benefits component.
        
        Returns:
            The Benefits object.
        """
        return self._benefits
    
    @property
    def department(self) -> Department:
        """Get department component.
        
        Returns:
            The Department object.
        """
        return self._department
    
    def transfer_to(self, new_department: Department) -> str:
        """Transfer employee to a new department.
        
        Args:
            new_department: The department to transfer to.
        
        Returns:
            Transfer confirmation message.
        """
        old_dept = self._department.name
        self._department.remove_employee(self._name)
        self._department = new_department
        new_department.add_employee(self._name)
        return f"{self._name} transferred from {old_dept} to {new_department.name}"
    
    def get_total_compensation(self) -> float:
        """Calculate total compensation including benefits.
        
        Returns:
            Total monetary value of salary + bonus + benefits.
        """
        return self._salary.get_total() + self._benefits.calculate_value()
    
    def get_summary(self) -> dict[str, Any]:
        """Get a summary of employee information.
        
        Returns:
            Dictionary with employee details.
        """
        return {
            "name": self._name,
            "department": self._department.name,
            "manager": self._department.manager,
            "base_salary": self._salary.base_amount,
            "total_compensation": self.get_total_compensation(),
            "benefits": self._benefits.get_benefits(),
        }
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted employee description.
        """
        return f"{self._name} - {self._department.name}"
