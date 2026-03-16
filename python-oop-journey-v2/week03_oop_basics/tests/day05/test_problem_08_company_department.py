"""Tests for Problem 08: Company Department."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_08_company_department import (
    Employee,
    Department,
    Company,
)


class TestEmployee:
    """Tests for Employee class."""
    
    def test_employee_init(self) -> None:
        """Test employee initialization."""
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        assert emp.name == "John Doe"
        assert emp.employee_id == "E001"
        assert emp.role == "Developer"
        assert emp.salary == 5000.0
        assert emp.department_id is None
    
    def test_assign_to_department(self) -> None:
        """Test assigning to department."""
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        emp.assign_to_department("DEV")
        assert emp.department_id == "DEV"
    
    def test_leave_department(self) -> None:
        """Test leaving department."""
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        emp.assign_to_department("DEV")
        emp.leave_department()
        assert emp.department_id is None
    
    def test_get_annual_salary(self) -> None:
        """Test calculating annual salary."""
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        assert emp.get_annual_salary() == 60000.0


class TestDepartment:
    """Tests for Department class."""
    
    def test_department_init(self) -> None:
        """Test department initialization."""
        dept = Department("DEV", "Development")
        assert dept.dept_id == "DEV"
        assert dept.name == "Development"
        assert dept.employees == []
    
    def test_add_employee(self) -> None:
        """Test adding employee."""
        dept = Department("DEV", "Development")
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        dept.add_employee(emp)
        assert len(dept.employees) == 1
        assert emp.department_id == "DEV"
    
    def test_remove_employee(self) -> None:
        """Test removing employee."""
        dept = Department("DEV", "Development")
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        dept.add_employee(emp)
        result = dept.remove_employee("E001")
        assert result is True
        assert len(dept.employees) == 0
        assert emp.department_id is None
    
    def test_remove_employee_not_found(self) -> None:
        """Test removing non-existent employee."""
        dept = Department("DEV", "Development")
        result = dept.remove_employee("INVALID")
        assert result is False
    
    def test_get_employee_count(self) -> None:
        """Test getting employee count."""
        dept = Department("DEV", "Development")
        assert dept.get_employee_count() == 0
        dept.add_employee(Employee("John", "E001", "Dev", 5000.0))
        assert dept.get_employee_count() == 1
    
    def test_get_total_salary(self) -> None:
        """Test calculating total salary."""
        dept = Department("DEV", "Development")
        dept.add_employee(Employee("John", "E001", "Dev", 5000.0))
        dept.add_employee(Employee("Jane", "E002", "Dev", 6000.0))
        assert dept.get_total_salary() == 11000.0
    
    def test_find_employee(self) -> None:
        """Test finding employee."""
        dept = Department("DEV", "Development")
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        dept.add_employee(emp)
        found = dept.find_employee("E001")
        assert found is emp
    
    def test_find_employee_not_found(self) -> None:
        """Test finding non-existent employee."""
        dept = Department("DEV", "Development")
        found = dept.find_employee("INVALID")
        assert found is None


class TestCompany:
    """Tests for Company class."""
    
    def test_company_init(self) -> None:
        """Test company initialization."""
        company = Company("TechCorp")
        assert company.name == "TechCorp"
        assert company.departments == {}
        assert company.all_employees == {}
    
    def test_add_department(self) -> None:
        """Test adding department."""
        company = Company("TechCorp")
        dept = Department("DEV", "Development")
        company.add_department(dept)
        assert "DEV" in company.departments
    
    def test_get_department(self) -> None:
        """Test getting department."""
        company = Company("TechCorp")
        dept = Department("DEV", "Development")
        company.add_department(dept)
        found = company.get_department("DEV")
        assert found is dept
    
    def test_get_department_not_found(self) -> None:
        """Test getting non-existent department."""
        company = Company("TechCorp")
        found = company.get_department("UNKNOWN")
        assert found is None
    
    def test_hire_employee(self) -> None:
        """Test hiring employee."""
        company = Company("TechCorp")
        dept = Department("DEV", "Development")
        company.add_department(dept)
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        result = company.hire_employee(emp, "DEV")
        assert "hired" in result.lower()
        assert "E001" in company.all_employees
        assert emp in dept.employees
    
    def test_hire_employee_dept_not_found(self) -> None:
        """Test hiring into non-existent department."""
        company = Company("TechCorp")
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        result = company.hire_employee(emp, "UNKNOWN")
        assert "not found" in result.lower()
    
    def test_fire_employee(self) -> None:
        """Test firing employee."""
        company = Company("TechCorp")
        dept = Department("DEV", "Development")
        company.add_department(dept)
        emp = Employee("John Doe", "E001", "Developer", 5000.0)
        company.hire_employee(emp, "DEV")
        result = company.fire_employee("E001")
        assert "fired" in result.lower()
        assert "E001" not in company.all_employees
        assert emp not in dept.employees
    
    def test_fire_employee_not_found(self) -> None:
        """Test firing non-existent employee."""
        company = Company("TechCorp")
        result = company.fire_employee("INVALID")
        assert "not found" in result.lower()
    
    def test_get_department_payroll(self) -> None:
        """Test getting department payroll."""
        company = Company("TechCorp")
        dept = Department("DEV", "Development")
        company.add_department(dept)
        company.hire_employee(Employee("John", "E001", "Dev", 5000.0), "DEV")
        payroll = company.get_department_payroll("DEV")
        assert payroll == 60000.0  # 5000 * 12
    
    def test_get_department_payroll_not_found(self) -> None:
        """Test payroll for non-existent department."""
        company = Company("TechCorp")
        payroll = company.get_department_payroll("UNKNOWN")
        assert payroll == 0.0
    
    def test_get_total_payroll(self) -> None:
        """Test getting total payroll."""
        company = Company("TechCorp")
        company.add_department(Department("DEV", "Development"))
        company.add_department(Department("HR", "Human Resources"))
        company.hire_employee(Employee("John", "E001", "Dev", 5000.0), "DEV")
        company.hire_employee(Employee("Jane", "E002", "HR", 4000.0), "HR")
        # (5000 + 4000) * 12 = 108000
        assert company.get_total_payroll() == 108000.0
    
    def test_transfer_employee(self) -> None:
        """Test transferring employee."""
        company = Company("TechCorp")
        company.add_department(Department("DEV", "Development"))
        company.add_department(Department("HR", "Human Resources"))
        emp = Employee("John", "E001", "Dev", 5000.0)
        company.hire_employee(emp, "DEV")
        result = company.transfer_employee("E001", "HR")
        assert "transferred" in result.lower()
        assert emp.department_id == "HR"
    
    def test_transfer_employee_not_found(self) -> None:
        """Test transferring non-existent employee."""
        company = Company("TechCorp")
        company.add_department(Department("HR", "Human Resources"))
        result = company.transfer_employee("INVALID", "HR")
        assert "not found" in result.lower()
    
    def test_get_employee_count(self) -> None:
        """Test getting employee count."""
        company = Company("TechCorp")
        company.add_department(Department("DEV", "Development"))
        assert company.get_employee_count() == 0
        company.hire_employee(Employee("John", "E001", "Dev", 5000.0), "DEV")
        assert company.get_employee_count() == 1
    
    def test_get_department_count(self) -> None:
        """Test getting department count."""
        company = Company("TechCorp")
        assert company.get_department_count() == 0
        company.add_department(Department("DEV", "Development"))
        assert company.get_department_count() == 1
