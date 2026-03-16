"""Tests for Problem 03: Employee Role ABC."""

from __future__ import annotations

import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day03.problem_03_employee_role_abc import (
    EmployeeRole,
    HourlyEmployee,
    SalariedEmployee,
    CommissionedEmployee,
)


class TestEmployeeRoleABC:
    """Test suite for EmployeeRole abstract base class."""
    
    def test_employee_role_is_abstract(self) -> None:
        """Test that EmployeeRole cannot be instantiated."""
        assert issubclass(EmployeeRole, ABC)
        with pytest.raises(TypeError, match="abstract"):
            EmployeeRole()
    
    def test_employee_role_has_abstract_role_name(self) -> None:
        """Test that EmployeeRole defines abstract role_name property."""
        assert hasattr(EmployeeRole, 'role_name')
    
    def test_employee_role_has_abstract_calculate_pay(self) -> None:
        """Test that EmployeeRole defines abstract calculate_pay method."""
        assert hasattr(EmployeeRole, 'calculate_pay')


class TestHourlyEmployee:
    """Test suite for HourlyEmployee."""
    
    def test_initialization(self) -> None:
        """Test hourly employee initialization."""
        employee = HourlyEmployee(25.0)
        assert employee._hourly_rate == 25.0
    
    def test_initialization_negative_rate_raises(self) -> None:
        """Test that negative hourly rate raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            HourlyEmployee(-25.0)
    
    def test_initialization_zero_rate_raises(self) -> None:
        """Test that zero hourly rate raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            HourlyEmployee(0.0)
    
    def test_role_name(self) -> None:
        """Test role_name property."""
        employee = HourlyEmployee(25.0)
        assert employee.role_name == "Hourly"
    
    def test_calculate_pay_regular_hours(self) -> None:
        """Test pay calculation for regular hours (<= 40)."""
        employee = HourlyEmployee(25.0)
        # 40 hours at $25/hour = $1000
        assert employee.calculate_pay(40.0) == 1000.0
    
    def test_calculate_pay_under_40_hours(self) -> None:
        """Test pay calculation for under 40 hours."""
        employee = HourlyEmployee(25.0)
        # 30 hours at $25/hour = $750
        assert employee.calculate_pay(30.0) == 750.0
    
    def test_calculate_pay_with_overtime(self) -> None:
        """Test pay calculation with overtime (> 40)."""
        employee = HourlyEmployee(25.0)
        # 40 hours at $25/hour = $1000
        # 5 hours at $37.50/hour = $187.50
        # Total = $1187.50
        assert employee.calculate_pay(45.0) == 1187.5
    
    def test_calculate_pay_overtime_only(self) -> None:
        """Test pay calculation for all overtime."""
        employee = HourlyEmployee(20.0)
        # 50 hours: 40 * 20 + 10 * 30 = 800 + 300 = 1100
        assert employee.calculate_pay(50.0) == 1100.0
    
    def test_calculate_pay_zero_hours(self) -> None:
        """Test pay calculation for zero hours."""
        employee = HourlyEmployee(25.0)
        assert employee.calculate_pay(0.0) == 0.0


class TestSalariedEmployee:
    """Test suite for SalariedEmployee."""
    
    def test_initialization(self) -> None:
        """Test salaried employee initialization."""
        employee = SalariedEmployee(78000.0)
        assert employee._annual_salary == 78000.0
    
    def test_initialization_negative_salary_raises(self) -> None:
        """Test that negative salary raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            SalariedEmployee(-78000.0)
    
    def test_initialization_zero_salary_raises(self) -> None:
        """Test that zero salary raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            SalariedEmployee(0.0)
    
    def test_role_name(self) -> None:
        """Test role_name property."""
        employee = SalariedEmployee(78000.0)
        assert employee.role_name == "Salaried"
    
    def test_calculate_pay(self) -> None:
        """Test biweekly pay calculation."""
        employee = SalariedEmployee(78000.0)
        # 78000 / 26 = 3000 per pay period
        assert employee.calculate_pay(80.0) == 3000.0
    
    def test_calculate_pay_ignores_hours(self) -> None:
        """Test that hours_worked is ignored."""
        employee = SalariedEmployee(52000.0)
        # 52000 / 26 = 2000 per pay period (regardless of hours)
        assert employee.calculate_pay(0.0) == 2000.0
        assert employee.calculate_pay(100.0) == 2000.0
    
    def test_calculate_pay_different_salary(self) -> None:
        """Test biweekly pay with different salary."""
        employee = SalariedEmployee(104000.0)
        # 104000 / 26 = 4000 per pay period
        assert employee.calculate_pay(80.0) == 4000.0


class TestCommissionedEmployee:
    """Test suite for CommissionedEmployee."""
    
    def test_initialization(self) -> None:
        """Test commissioned employee initialization."""
        employee = CommissionedEmployee(52000.0, 0.10)
        assert employee._base_salary == 52000.0
        assert employee._commission_rate == 0.10
    
    def test_initialization_negative_base_raises(self) -> None:
        """Test that negative base salary raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            CommissionedEmployee(-52000.0, 0.10)
    
    def test_initialization_negative_commission_raises(self) -> None:
        """Test that negative commission rate raises ValueError."""
        with pytest.raises(ValueError, match="negative"):
            CommissionedEmployee(52000.0, -0.10)
    
    def test_initialization_zero_commission_allowed(self) -> None:
        """Test that zero commission rate is allowed."""
        employee = CommissionedEmployee(52000.0, 0.0)
        assert employee._commission_rate == 0.0
    
    def test_role_name(self) -> None:
        """Test role_name property."""
        employee = CommissionedEmployee(52000.0, 0.10)
        assert employee.role_name == "Commissioned"
    
    def test_calculate_pay_base_only(self) -> None:
        """Test pay calculation with no sales."""
        employee = CommissionedEmployee(52000.0, 0.10)
        # 52000 / 26 = 2000 base pay, no commission
        assert employee.calculate_pay(80.0, 0.0) == 2000.0
    
    def test_calculate_pay_with_commission(self) -> None:
        """Test pay calculation with sales commission."""
        employee = CommissionedEmployee(52000.0, 0.10)
        # 2000 base + 10000 * 0.10 = 2000 + 1000 = 3000
        assert employee.calculate_pay(80.0, 10000.0) == 3000.0
    
    def test_calculate_pay_different_rates(self) -> None:
        """Test pay with different commission rates."""
        employee = CommissionedEmployee(52000.0, 0.05)
        # 2000 base + 20000 * 0.05 = 2000 + 1000 = 3000
        assert employee.calculate_pay(80.0, 20000.0) == 3000.0
    
    def test_calculate_pay_ignores_hours(self) -> None:
        """Test that hours parameter is not used in calculation."""
        employee = CommissionedEmployee(52000.0, 0.10)
        pay = employee.calculate_pay(80.0, 10000.0)
        assert employee.calculate_pay(40.0, 10000.0) == pay
