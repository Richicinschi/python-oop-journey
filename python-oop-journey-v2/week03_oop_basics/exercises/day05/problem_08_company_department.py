"""Problem 08: Company Department.

Implement a Company with Departments and Employees.
This demonstrates composition (departments owned by company) and aggregation (employees assigned to departments).

Classes to implement:
- Employee: with attributes name, employee_id, role, salary, department_id (optional)
- Department: with attributes id, name, employees (aggregation)
- Company: composes Departments

Methods required:
- Employee.assign_to_department(dept_id: str) -> None
- Employee.get_annual_salary() -> float
- Department.add_employee(employee: Employee) -> None
- Department.remove_employee(employee_id: str) -> bool
- Department.get_total_salary() -> float
- Company.add_department(department: Department) - composition
- Company.hire_employee(employee: Employee, dept_id: str) -> str
- Company.get_department_payroll(dept_id: str) -> float

Hints:
    - Hint 1: Company stores departments in dict: self._departments = {id: Department}
    - Hint 2: Department stores employees in list; track company-wide employees in Company too
    - Hint 3: transfer_employee: find emp in old dept, remove, add to new dept, update dept_id
"""

from __future__ import annotations
from typing import Optional


class Employee:
    """An employee who can work in a department."""
    
    def __init__(self, name: str, employee_id: str, role: str, salary: float) -> None:
        # TODO: Initialize name, employee_id, role, salary (monthly), department_id (None)
        pass
    
    def assign_to_department(self, dept_id: str) -> None:
        # TODO: Set department_id
        pass
    
    def leave_department(self) -> None:
        # TODO: Clear department_id
        pass
    
    def get_annual_salary(self) -> float:
        # TODO: Return annual salary (monthly * 12)
        pass


class Department:
    """A department in the company (composed by Company)."""
    
    def __init__(self, dept_id: str, name: str) -> None:
        # TODO: Initialize id, name, employees (empty list)
        pass
    
    def add_employee(self, employee: Employee) -> None:
        # TODO: Add employee and set their department_id
        pass
    
    def remove_employee(self, employee_id: str) -> bool:
        # TODO: Remove employee by ID, clear their department_id, return True if found
        pass
    
    def get_employee_count(self) -> int:
        # TODO: Return number of employees
        pass
    
    def get_total_salary(self) -> float:
        # TODO: Return sum of monthly salaries
        pass
    
    def find_employee(self, employee_id: str) -> Optional[Employee]:
        # TODO: Return employee by ID or None
        pass


class Company:
    """A company composing departments."""
    
    def __init__(self, name: str) -> None:
        # TODO: Initialize name, departments dict (id -> Department), all_employees dict (id -> Employee)
        pass
    
    def add_department(self, department: Department) -> None:
        # TODO: Add department to company
        pass
    
    def get_department(self, dept_id: str) -> Optional[Department]:
        # TODO: Return department by ID or None
        pass
    
    def hire_employee(self, employee: Employee, dept_id: str) -> str:
        # TODO: Find department, add employee, track employee, return status
        pass
    
    def fire_employee(self, employee_id: str) -> str:
        # TODO: Find employee, remove from department and company, return status
        pass
    
    def get_department_payroll(self, dept_id: str) -> float:
        # TODO: Return annual payroll for department (monthly * 12)
        pass
    
    def get_total_payroll(self) -> float:
        # TODO: Return total annual payroll across all departments
        pass
    
    def transfer_employee(self, employee_id: str, new_dept_id: str) -> str:
        # TODO: Move employee to new department, return status
        pass
