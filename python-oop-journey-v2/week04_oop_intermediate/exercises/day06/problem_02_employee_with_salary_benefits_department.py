"""Problem 02: Employee with Salary Benefits Department

Topic: Composition vs Inheritance
Difficulty: Medium

Design an employee system that uses composition to combine
salary calculation, benefits, and department membership
rather than creating deep inheritance hierarchies.

Classes to implement:
- SalaryStrategy (abstract base for salary calculation)
- HourlySalary, SalariedSalary, CommissionSalary
- BenefitsPackage (collection of benefits)
- Department (name, location, budget)
- Employee (composes salary, benefits, and department)

This demonstrates how composition allows flexible combination
of behaviors without combinatorial explosion of subclasses.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SalaryStrategy(ABC):
    """Strategy for calculating salary."""

    @abstractmethod
    def calculate_salary(self) -> float:
        """Calculate gross salary."""
        raise NotImplementedError("Implement calculate_salary")

    @abstractmethod
    def get_details(self) -> dict[str, Any]:
        """Return salary calculation details."""
        raise NotImplementedError("Implement get_details")

    @property
    @abstractmethod
    def strategy_type(self) -> str:
        """Return strategy type identifier."""
        raise NotImplementedError("Implement strategy_type")


class HourlySalary(SalaryStrategy):
    """Hourly wage salary calculation."""

    def __init__(self, hourly_rate: float, hours_worked: float) -> None:
        raise NotImplementedError("Implement __init__")

    def calculate_salary(self) -> float:
        """Calculate: hourly_rate * hours_worked (1.5x for overtime > 40)."""
        raise NotImplementedError("Implement calculate_salary")

    def get_details(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_details")

    @property
    def strategy_type(self) -> str:
        raise NotImplementedError("Implement strategy_type")


class SalariedSalary(SalaryStrategy):
    """Fixed monthly salary."""

    def __init__(self, monthly_salary: float, months_worked: int = 12) -> None:
        raise NotImplementedError("Implement __init__")

    def calculate_salary(self) -> float:
        raise NotImplementedError("Implement calculate_salary")

    def get_details(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_details")

    @property
    def strategy_type(self) -> str:
        raise NotImplementedError("Implement strategy_type")


class CommissionSalary(SalaryStrategy):
    """Base plus commission salary."""

    def __init__(
        self,
        base_salary: float,
        sales_amount: float,
        commission_rate: float,
    ) -> None:
        raise NotImplementedError("Implement __init__")

    def calculate_salary(self) -> float:
        raise NotImplementedError("Implement calculate_salary")

    def get_details(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_details")

    @property
    def strategy_type(self) -> str:
        raise NotImplementedError("Implement strategy_type")


class BenefitsPackage:
    """Collection of employee benefits."""

    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")

    def add_benefit(self, benefit_name: str, value: float) -> None:
        """Add a benefit with its monetary value."""
        raise NotImplementedError("Implement add_benefit")

    def remove_benefit(self, benefit_name: str) -> bool:
        """Remove a benefit, return True if found."""
        raise NotImplementedError("Implement remove_benefit")

    def get_total_value(self) -> float:
        """Return total value of all benefits."""
        raise NotImplementedError("Implement get_total_value")

    def get_benefit_list(self) -> list[str]:
        """Return list of benefit names."""
        raise NotImplementedError("Implement get_benefit_list")

    def has_benefit(self, benefit_name: str) -> bool:
        raise NotImplementedError("Implement has_benefit")


class Department:
    """Department an employee belongs to."""

    def __init__(self, name: str, location: str, budget: float) -> None:
        raise NotImplementedError("Implement __init__")

    def allocate_budget(self, amount: float) -> bool:
        """Allocate budget for a purpose, return True if available."""
        raise NotImplementedError("Implement allocate_budget")

    def get_info(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_info")


class Employee:
    """Employee composed of salary strategy, benefits, and department.
    
    Instead of inheriting from SalariedEmployee, HourlyEmployee, etc.,
    this class uses composition to combine:
    - SalaryStrategy (how pay is calculated)
    - BenefitsPackage (what perks they get)
    - Department (where they work)
    
    Benefits:
    - Can change salary type without changing Employee class
    - Can add/remove benefits without inheritance
    - Can transfer between departments easily
    - Easy to test with mock strategies
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        salary_strategy: SalaryStrategy,
        benefits: BenefitsPackage,
        department: Department,
    ) -> None:
        raise NotImplementedError("Implement __init__")

    def get_total_compensation(self) -> float:
        """Return salary plus benefits value."""
        raise NotImplementedError("Implement get_total_compensation")

    def change_salary_strategy(self, new_strategy: SalaryStrategy) -> None:
        """Change how salary is calculated (composition flexibility)."""
        raise NotImplementedError("Implement change_salary_strategy")

    def transfer_to_department(self, new_department: Department) -> str:
        """Move to a different department."""
        raise NotImplementedError("Implement transfer_to_department")

    def add_benefit(self, name: str, value: float) -> None:
        raise NotImplementedError("Implement add_benefit")

    def get_info(self) -> dict[str, Any]:
        """Return complete employee information."""
        raise NotImplementedError("Implement get_info")
