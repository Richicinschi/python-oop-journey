"""Tests for Problem 02: Employee with Salary, Benefits, and Department."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day06.problem_02_employee_with_salary_benefits_department import (
    Benefits,
    Department,
    Employee,
    Salary,
)


class TestSalary:
    """Tests for the Salary class."""
    
    def test_salary_init_default_bonus(self) -> None:
        """Test Salary initialization with default bonus."""
        salary = Salary(80000)
        assert salary.base_amount == 80000
        assert salary.bonus_percentage == 10.0
    
    def test_salary_init_custom_bonus(self) -> None:
        """Test Salary initialization with custom bonus."""
        salary = Salary(80000, 15.0)
        assert salary.bonus_percentage == 15.0
    
    def test_salary_give_raise(self) -> None:
        """Test giving a raise."""
        salary = Salary(80000)
        new_amount = salary.give_raise(10.0)
        assert new_amount == 88000.0
        assert salary.base_amount == 88000.0
    
    def test_salary_calculate_bonus(self) -> None:
        """Test bonus calculation."""
        salary = Salary(100000, 10.0)
        assert salary.calculate_bonus() == 10000.0
    
    def test_salary_get_total(self) -> None:
        """Test total compensation calculation."""
        salary = Salary(100000, 10.0)
        assert salary.get_total() == 110000.0
    
    def test_salary_set_bonus_percentage(self) -> None:
        """Test setting bonus percentage."""
        salary = Salary(80000)
        salary.set_bonus_percentage(20.0)
        assert salary.bonus_percentage == 20.0
    
    def test_salary_str(self) -> None:
        """Test string representation."""
        salary = Salary(80000)
        result = str(salary)
        assert "$80,000.00" in result
        assert "10.0%" in result


class TestBenefits:
    """Tests for the Benefits class."""
    
    def test_benefits_init_empty(self) -> None:
        """Test Benefits initialization with no benefits."""
        benefits = Benefits()
        assert benefits.get_benefits() == []
    
    def test_benefits_init_with_list(self) -> None:
        """Test Benefits initialization with benefit list."""
        benefits = Benefits(["Health", "Dental"])
        assert benefits.get_benefits() == ["Health", "Dental"]
    
    def test_benefits_add_benefit(self) -> None:
        """Test adding a benefit."""
        benefits = Benefits()
        benefits.add_benefit("Health")
        assert "Health" in benefits.get_benefits()
    
    def test_benefits_add_duplicate(self) -> None:
        """Test that duplicate benefits are not added."""
        benefits = Benefits(["Health"])
        benefits.add_benefit("Health")
        assert benefits.get_benefits().count("Health") == 1
    
    def test_benefits_remove_benefit(self) -> None:
        """Test removing a benefit."""
        benefits = Benefits(["Health", "Dental"])
        result = benefits.remove_benefit("Health")
        assert result is True
        assert "Health" not in benefits.get_benefits()
    
    def test_benefits_remove_nonexistent(self) -> None:
        """Test removing a benefit that doesn't exist."""
        benefits = Benefits(["Health"])
        result = benefits.remove_benefit("Dental")
        assert result is False
    
    def test_benefits_has_benefit(self) -> None:
        """Test checking for benefit presence."""
        benefits = Benefits(["Health"])
        assert benefits.has_benefit("Health") is True
        assert benefits.has_benefit("Dental") is False
    
    def test_benefits_calculate_value(self) -> None:
        """Test calculating benefit value."""
        benefits = Benefits(["Health", "Dental"])
        # Health: 8000, Dental: 1200
        assert benefits.calculate_value() == 9200.0
    
    def test_benefits_str(self) -> None:
        """Test string representation."""
        benefits = Benefits(["Health", "Dental"])
        result = str(benefits)
        assert "Health" in result
        assert "Dental" in result
    
    def test_benefits_str_empty(self) -> None:
        """Test string representation when empty."""
        benefits = Benefits()
        assert str(benefits) == "None"


class TestDepartment:
    """Tests for the Department class."""
    
    def test_department_init(self) -> None:
        """Test Department initialization."""
        dept = Department("Engineering", "Alice")
        assert dept.name == "Engineering"
        assert dept.manager == "Alice"
    
    def test_department_change_manager(self) -> None:
        """Test changing department manager."""
        dept = Department("Engineering", "Alice")
        dept.change_manager("Bob")
        assert dept.manager == "Bob"
    
    def test_department_add_employee(self) -> None:
        """Test adding an employee."""
        dept = Department("Engineering", "Alice")
        dept.add_employee("Charlie")
        assert dept.get_employee_count() == 1
    
    def test_department_add_duplicate_employee(self) -> None:
        """Test that duplicate employees are not added."""
        dept = Department("Engineering", "Alice")
        dept.add_employee("Charlie")
        dept.add_employee("Charlie")
        assert dept.get_employee_count() == 1
    
    def test_department_remove_employee(self) -> None:
        """Test removing an employee."""
        dept = Department("Engineering", "Alice")
        dept.add_employee("Charlie")
        result = dept.remove_employee("Charlie")
        assert result is True
        assert dept.get_employee_count() == 0
    
    def test_department_remove_nonexistent(self) -> None:
        """Test removing an employee that doesn't exist."""
        dept = Department("Engineering", "Alice")
        result = dept.remove_employee("Charlie")
        assert result is False
    
    def test_department_str(self) -> None:
        """Test string representation."""
        dept = Department("Engineering", "Alice")
        result = str(dept)
        assert "Engineering" in result
        assert "Alice" in result


class TestEmployee:
    """Tests for the Employee class."""
    
    def test_employee_init(self) -> None:
        """Test Employee initialization."""
        dept = Department("Engineering", "Alice")
        salary = Salary(80000)
        benefits = Benefits(["Health"])
        emp = Employee("Bob", salary, benefits, dept)
        
        assert emp.name == "Bob"
        assert emp.salary == salary
        assert emp.benefits == benefits
        assert emp.department == dept
    
    def test_employee_added_to_department(self) -> None:
        """Test that employee is added to department on init."""
        dept = Department("Engineering", "Alice")
        salary = Salary(80000)
        benefits = Benefits(["Health"])
        emp = Employee("Bob", salary, benefits, dept)
        
        assert dept.get_employee_count() == 1
    
    def test_employee_transfer_to(self) -> None:
        """Test transferring to a new department."""
        dept1 = Department("Engineering", "Alice")
        dept2 = Department("Sales", "Carol")
        salary = Salary(80000)
        benefits = Benefits(["Health"])
        emp = Employee("Bob", salary, benefits, dept1)
        
        result = emp.transfer_to(dept2)
        
        assert "Bob" in result
        assert "Engineering" in result
        assert "Sales" in result
        assert emp.department == dept2
        assert dept1.get_employee_count() == 0
        assert dept2.get_employee_count() == 1
    
    def test_employee_get_total_compensation(self) -> None:
        """Test total compensation calculation."""
        dept = Department("Engineering", "Alice")
        salary = Salary(80000, 10.0)  # 80k + 8k bonus = 88k
        benefits = Benefits(["Health"])  # 8k value
        emp = Employee("Bob", salary, benefits, dept)
        
        # 80k + 8k bonus + 8k benefits = 96k
        assert emp.get_total_compensation() == 96000.0
    
    def test_employee_get_summary(self) -> None:
        """Test getting employee summary."""
        dept = Department("Engineering", "Alice")
        salary = Salary(80000)
        benefits = Benefits(["Health"])
        emp = Employee("Bob", salary, benefits, dept)
        
        summary = emp.get_summary()
        assert summary["name"] == "Bob"
        assert summary["department"] == "Engineering"
        assert summary["manager"] == "Alice"
        assert summary["base_salary"] == 80000
        assert "Health" in summary["benefits"]
    
    def test_employee_str(self) -> None:
        """Test string representation."""
        dept = Department("Engineering", "Alice")
        salary = Salary(80000)
        benefits = Benefits(["Health"])
        emp = Employee("Bob", salary, benefits, dept)
        
        result = str(emp)
        assert "Bob" in result
        assert "Engineering" in result
    
    def test_employee_uses_composition(self) -> None:
        """Test that Employee uses composition."""
        assert not issubclass(Employee, Salary)
        assert not issubclass(Employee, Benefits)
        assert not issubclass(Employee, Department)
