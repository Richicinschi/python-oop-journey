"""Tests for Problem 06: Employee Bonus Dispatch."""

from __future__ import annotations

import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day05.problem_06_employee_bonus_dispatch import (
    Employee,
    RegularEmployee,
    Manager,
    SalesPerson,
    Intern,
    calculate_payroll,
)


class TestEmployeeABC:
    """Test suite for Employee abstract base class."""
    
    def test_employee_is_abstract(self) -> None:
        """Test that Employee cannot be instantiated."""
        assert issubclass(Employee, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Employee("Test", 50000.0)


class TestRegularEmployee:
    """Test suite for RegularEmployee."""
    
    def test_initialization(self) -> None:
        """Test regular employee initialization."""
        emp = RegularEmployee("John Doe", 50000.0)
        assert emp.name == "John Doe"
        assert emp.base_salary == 50000.0
    
    def test_calculate_bonus(self) -> None:
        """Test bonus calculation: 5% of base."""
        emp = RegularEmployee("John", 50000.0)
        assert emp.calculate_bonus() == 2500.0  # 5% of 50000
    
    def test_get_employee_type(self) -> None:
        """Test employee type."""
        emp = RegularEmployee("John", 50000.0)
        assert emp.get_employee_type() == "Regular"
    
    def test_get_total_compensation(self) -> None:
        """Test total compensation."""
        emp = RegularEmployee("John", 50000.0)
        # 50000 + (50000 * 0.05) = 52500
        assert emp.get_total_compensation() == 52500.0


class TestManager:
    """Test suite for Manager."""
    
    def test_initialization(self) -> None:
        """Test manager initialization."""
        mgr = Manager("Jane Smith", 80000.0, 5)
        assert mgr.name == "Jane Smith"
        assert mgr.base_salary == 80000.0
        assert mgr.team_size == 5
    
    def test_calculate_bonus(self) -> None:
        """Test bonus: 10% of base + $100 per team member."""
        mgr = Manager("Jane", 80000.0, 5)
        # 80000 * 0.10 + 5 * 100 = 8000 + 500 = 8500
        assert mgr.calculate_bonus() == 8500.0
    
    def test_calculate_bonus_zero_team(self) -> None:
        """Test bonus with zero team size."""
        mgr = Manager("Jane", 80000.0, 0)
        assert mgr.calculate_bonus() == 8000.0  # Just 10% of base
    
    def test_get_employee_type(self) -> None:
        """Test employee type."""
        mgr = Manager("Jane", 80000.0, 5)
        assert mgr.get_employee_type() == "Manager"
    
    def test_get_total_compensation(self) -> None:
        """Test total compensation."""
        mgr = Manager("Jane", 80000.0, 5)
        # 80000 + 8500 = 88500
        assert mgr.get_total_compensation() == 88500.0


class TestSalesPerson:
    """Test suite for SalesPerson."""
    
    def test_initialization(self) -> None:
        """Test sales person initialization."""
        sales = SalesPerson("Bob Wilson", 40000.0, 100000.0)
        assert sales.name == "Bob Wilson"
        assert sales.base_salary == 40000.0
        assert sales.sales_amount == 100000.0
    
    def test_calculate_bonus(self) -> None:
        """Test bonus: 5% of base + 2% of sales."""
        sales = SalesPerson("Bob", 40000.0, 100000.0)
        # 40000 * 0.05 + 100000 * 0.02 = 2000 + 2000 = 4000
        assert sales.calculate_bonus() == 4000.0
    
    def test_calculate_bonus_zero_sales(self) -> None:
        """Test bonus with zero sales."""
        sales = SalesPerson("Bob", 40000.0, 0.0)
        assert sales.calculate_bonus() == 2000.0  # Just 5% of base
    
    def test_get_employee_type(self) -> None:
        """Test employee type."""
        sales = SalesPerson("Bob", 40000.0, 100000.0)
        assert sales.get_employee_type() == "Sales"


class TestIntern:
    """Test suite for Intern."""
    
    def test_initialization(self) -> None:
        """Test intern initialization."""
        intern = Intern("Alice Brown", 30000.0)
        assert intern.name == "Alice Brown"
        assert intern.base_salary == 30000.0
    
    def test_calculate_bonus(self) -> None:
        """Test bonus: fixed $500."""
        intern = Intern("Alice", 30000.0)
        assert intern.calculate_bonus() == 500.0
    
    def test_get_employee_type(self) -> None:
        """Test employee type."""
        intern = Intern("Alice", 30000.0)
        assert intern.get_employee_type() == "Intern"
    
    def test_get_total_compensation(self) -> None:
        """Test total compensation."""
        intern = Intern("Alice", 30000.0)
        assert intern.get_total_compensation() == 30500.0


class TestCalculatePayroll:
    """Test suite for calculate_payroll function."""
    
    def test_empty_list(self) -> None:
        """Test with empty list."""
        result = calculate_payroll([])
        
        assert result["total_base_salary"] == 0.0
        assert result["total_bonus"] == 0.0
        assert result["total_compensation"] == 0.0
        assert result["by_type"] == {}
    
    def test_single_employee(self) -> None:
        """Test with single employee."""
        employees = [RegularEmployee("John", 50000.0)]
        result = calculate_payroll(employees)
        
        assert result["total_base_salary"] == 50000.0
        assert result["total_bonus"] == 2500.0
        assert result["total_compensation"] == 52500.0
        assert result["by_type"] == {"Regular": 1}
    
    def test_mixed_employees(self) -> None:
        """Test polymorphic payroll with mixed employee types."""
        employees = [
            RegularEmployee("John", 50000.0),  # Bonus: 2500
            Manager("Jane", 80000.0, 5),  # Bonus: 8500
            SalesPerson("Bob", 40000.0, 100000.0),  # Bonus: 4000
            Intern("Alice", 30000.0),  # Bonus: 500
        ]
        result = calculate_payroll(employees)
        
        assert result["total_base_salary"] == 200000.0
        assert result["total_bonus"] == 15500.0  # 2500 + 8500 + 4000 + 500
        assert result["total_compensation"] == 215500.0
        assert result["by_type"] == {
            "Regular": 1,
            "Manager": 1,
            "Sales": 1,
            "Intern": 1,
        }
    
    def test_multiple_same_type(self) -> None:
        """Test with multiple employees of same type."""
        employees = [
            RegularEmployee("John", 50000.0),
            RegularEmployee("Jane", 60000.0),
            Intern("Alice", 25000.0),
            Intern("Bob", 28000.0),
        ]
        result = calculate_payroll(employees)
        
        assert result["by_type"] == {"Regular": 2, "Intern": 2}
        assert result["total_base_salary"] == 163000.0
