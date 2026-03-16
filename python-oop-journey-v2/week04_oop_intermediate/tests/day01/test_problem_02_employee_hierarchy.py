"""Tests for Problem 02: Employee Hierarchy."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_02_employee_hierarchy import (
    Employee, Manager, Engineer, Salesperson
)


class TestEmployee:
    """Tests for the base Employee class."""
    
    def test_employee_init(self) -> None:
        emp = Employee("John Doe", "E001", 50000.0)
        assert emp.name == "John Doe"
        assert emp.employee_id == "E001"
        assert emp.base_salary == 50000.0
    
    def test_employee_get_details(self) -> None:
        emp = Employee("John Doe", "E001", 50000.0)
        assert emp.get_details() == "Name: John Doe, ID: E001"
    
    def test_employee_calculate_salary(self) -> None:
        emp = Employee("John Doe", "E001", 50000.0)
        assert emp.calculate_salary() == 50000.0
    
    def test_employee_get_role(self) -> None:
        emp = Employee("John Doe", "E001", 50000.0)
        assert emp.get_role() == "Employee"


class TestManager:
    """Tests for the Manager class."""
    
    def test_manager_inheritance(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        assert isinstance(manager, Employee)
    
    def test_manager_init(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        assert manager.name == "Jane Smith"
        assert manager.bonus_rate == 0.20
        assert manager.department == "Engineering"
    
    def test_manager_get_details(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        details = manager.get_details()
        assert "Jane Smith" in details
        assert "Engineering" in details
        assert "Reports: 0" in details
    
    def test_manager_calculate_salary(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        expected = 80000.0 + (80000.0 * 0.20)
        assert manager.calculate_salary() == expected
    
    def test_manager_get_role(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        assert manager.get_role() == "Manager"
    
    def test_manager_add_report(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        emp = Employee("John Doe", "E001", 50000.0)
        manager.add_report(emp)
        assert manager.get_report_count() == 1
    
    def test_manager_add_multiple_reports(self) -> None:
        manager = Manager("Jane Smith", "M001", 80000.0, 0.20, "Engineering")
        manager.add_report(Employee("E1", "E001", 50000.0))
        manager.add_report(Employee("E2", "E002", 55000.0))
        assert manager.get_report_count() == 2


class TestEngineer:
    """Tests for the Engineer class."""
    
    def test_engineer_inheritance(self) -> None:
        eng = Engineer("Bob Dev", "ENG001", 70000.0, "Backend", 5)
        assert isinstance(eng, Employee)
    
    def test_engineer_init(self) -> None:
        eng = Engineer("Bob Dev", "ENG001", 70000.0, "Backend", 5)
        assert eng.name == "Bob Dev"
        assert eng.specialization == "Backend"
        assert eng.years_experience == 5
    
    def test_engineer_get_details(self) -> None:
        eng = Engineer("Bob Dev", "ENG001", 70000.0, "Backend", 5)
        details = eng.get_details()
        assert "Bob Dev" in details
        assert "Backend" in details
        assert "5 years" in details
    
    def test_engineer_calculate_salary(self) -> None:
        eng = Engineer("Bob Dev", "ENG001", 70000.0, "Backend", 5)
        expected = 70000.0 + (5 * 2000)
        assert eng.calculate_salary() == expected
    
    def test_engineer_get_role(self) -> None:
        eng = Engineer("Bob Dev", "ENG001", 70000.0, "Backend", 5)
        assert eng.get_role() == "Engineer"
    
    def test_engineer_add_certification(self) -> None:
        eng = Engineer("Bob Dev", "ENG001", 70000.0, "Backend", 5)
        eng.add_certification("AWS Certified")
        eng.add_certification("Kubernetes")


class TestSalesperson:
    """Tests for the Salesperson class."""
    
    def test_salesperson_inheritance(self) -> None:
        sales = Salesperson("Alice Sell", "S001", 40000.0, 0.05, "Northeast")
        assert isinstance(sales, Employee)
    
    def test_salesperson_init(self) -> None:
        sales = Salesperson("Alice Sell", "S001", 40000.0, 0.05, "Northeast")
        assert sales.name == "Alice Sell"
        assert sales.commission_rate == 0.05
        assert sales.territory == "Northeast"
    
    def test_salesperson_get_details(self) -> None:
        sales = Salesperson("Alice Sell", "S001", 40000.0, 0.05, "Northeast")
        details = sales.get_details()
        assert "Alice Sell" in details
        assert "Northeast" in details
    
    def test_salesperson_calculate_salary_no_sales(self) -> None:
        sales = Salesperson("Alice Sell", "S001", 40000.0, 0.05, "Northeast")
        assert sales.calculate_salary() == 40000.0
    
    def test_salesperson_calculate_salary_with_sales(self) -> None:
        sales = Salesperson("Alice Sell", "S001", 40000.0, 0.05, "Northeast")
        sales.make_sale(100000.0)
        expected = 40000.0 + (100000.0 * 0.05)
        assert sales.calculate_salary() == expected
    
    def test_salesperson_multiple_sales(self) -> None:
        sales = Salesperson("Alice Sell", "S001", 40000.0, 0.10, "Northeast")
        sales.make_sale(50000.0)
        sales.make_sale(75000.0)
        expected = 40000.0 + (125000.0 * 0.10)
        assert sales.calculate_salary() == expected


class TestSuperUsage:
    """Tests verifying proper super() usage."""
    
    def test_manager_uses_super_for_details(self) -> None:
        manager = Manager("Test", "M001", 80000.0, 0.20, "IT")
        details = manager.get_details()
        assert "Name: Test" in details  # From parent via super()
    
    def test_engineer_uses_super_for_details(self) -> None:
        eng = Engineer("Test", "ENG001", 70000.0, "Backend", 5)
        details = eng.get_details()
        assert "Name: Test" in details  # From parent via super()


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_roles(self) -> None:
        employees: list[Employee] = [
            Employee("Base", "E001", 50000.0),
            Manager("Mgr", "M001", 80000.0, 0.20, "IT"),
            Engineer("Eng", "ENG001", 70000.0, "Backend", 5),
            Salesperson("Sales", "S001", 40000.0, 0.05, "East")
        ]
        
        roles = [e.get_role() for e in employees]
        assert roles == ["Employee", "Manager", "Engineer", "Salesperson"]
