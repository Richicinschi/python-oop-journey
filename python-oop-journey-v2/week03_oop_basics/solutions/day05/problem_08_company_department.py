"""Solution for Problem 08: Company Department.

Company with Departments and Employees - demonstrates composition
(departments owned by company) and aggregation (employees in departments).
"""

from __future__ import annotations
from typing import Optional


class Employee:
    """An employee who can work in a department.
    
    Employees exist independently and can transfer between departments.
    """
    
    def __init__(self, name: str, employee_id: str, role: str, salary: float) -> None:
        """Initialize the employee.
        
        Args:
            name: Employee name.
            employee_id: Unique employee ID.
            role: Job role/title.
            salary: Monthly salary.
        """
        self.name = name
        self.employee_id = employee_id
        self.role = role
        self.salary = salary
        self.department_id: str | None = None
    
    def assign_to_department(self, dept_id: str) -> None:
        """Assign employee to a department.
        
        Args:
            dept_id: Department ID.
        """
        self.department_id = dept_id
    
    def leave_department(self) -> None:
        """Remove employee from their department."""
        self.department_id = None
    
    def get_annual_salary(self) -> float:
        """Calculate annual salary.
        
        Returns:
            Annual salary (monthly * 12).
        """
        return self.salary * 12


class Department:
    """A department in the company (composed by Company).
    
    Departments are part of the company structure and exist
    only while the company maintains them.
    """
    
    def __init__(self, dept_id: str, name: str) -> None:
        """Initialize the department.
        
        Args:
            dept_id: Department ID.
            name: Department name.
        """
        self.dept_id = dept_id
        self.name = name
        self.employees: list[Employee] = []
    
    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the department.
        
        Args:
            employee: Employee to add.
        """
        self.employees.append(employee)
        employee.assign_to_department(self.dept_id)
    
    def remove_employee(self, employee_id: str) -> bool:
        """Remove an employee from the department.
        
        Args:
            employee_id: ID of employee to remove.
            
        Returns:
            True if removed, False if not found.
        """
        for i, emp in enumerate(self.employees):
            if emp.employee_id == employee_id:
                emp.leave_department()
                self.employees.pop(i)
                return True
        return False
    
    def get_employee_count(self) -> int:
        """Get number of employees.
        
        Returns:
            Employee count.
        """
        return len(self.employees)
    
    def get_total_salary(self) -> float:
        """Calculate total monthly salary for department.
        
        Returns:
            Sum of all employee salaries.
        """
        return sum(emp.salary for emp in self.employees)
    
    def find_employee(self, employee_id: str) -> Optional[Employee]:
        """Find an employee by ID.
        
        Args:
            employee_id: Employee ID to find.
            
        Returns:
            Employee if found, None otherwise.
        """
        for emp in self.employees:
            if emp.employee_id == employee_id:
                return emp
        return None


class Company:
    """A company composing departments.
    
    Departments are composed (owned by company) while employees
    are aggregated within departments.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the company.
        
        Args:
            name: Company name.
        """
        self.name = name
        self.departments: dict[str, Department] = {}  # id -> Department
        self.all_employees: dict[str, Employee] = {}  # id -> Employee
    
    def add_department(self, department: Department) -> None:
        """Add a department to the company.
        
        Args:
            department: Department to add (composition).
        """
        self.departments[department.dept_id] = department
    
    def get_department(self, dept_id: str) -> Optional[Department]:
        """Get a department by ID.
        
        Args:
            dept_id: Department ID to find.
            
        Returns:
            Department if found, None otherwise.
        """
        return self.departments.get(dept_id)
    
    def hire_employee(self, employee: Employee, dept_id: str) -> str:
        """Hire an employee into a department.
        
        Args:
            employee: Employee to hire.
            dept_id: Target department ID.
            
        Returns:
            Status message.
        """
        department = self.departments.get(dept_id)
        if department is None:
            return f"Department {dept_id} not found"
        
        self.all_employees[employee.employee_id] = employee
        department.add_employee(employee)
        return f"{employee.name} hired into {department.name}"
    
    def fire_employee(self, employee_id: str) -> str:
        """Fire an employee.
        
        Args:
            employee_id: ID of employee to fire.
            
        Returns:
            Status message.
        """
        employee = self.all_employees.get(employee_id)
        if employee is None:
            return f"Employee {employee_id} not found"
        
        # Remove from department if assigned
        if employee.department_id:
            dept = self.departments.get(employee.department_id)
            if dept:
                dept.remove_employee(employee_id)
        
        del self.all_employees[employee_id]
        return f"{employee.name} has been fired"
    
    def get_department_payroll(self, dept_id: str) -> float:
        """Get annual payroll for a department.
        
        Args:
            dept_id: Department ID.
            
        Returns:
            Annual payroll amount.
        """
        department = self.departments.get(dept_id)
        if department is None:
            return 0.0
        return department.get_total_salary() * 12
    
    def get_total_payroll(self) -> float:
        """Get total annual payroll for company.
        
        Returns:
            Total annual payroll.
        """
        total = 0.0
        for dept in self.departments.values():
            total += dept.get_total_salary() * 12
        return total
    
    def transfer_employee(self, employee_id: str, new_dept_id: str) -> str:
        """Transfer an employee to a different department.
        
        Args:
            employee_id: Employee ID to transfer.
            new_dept_id: Target department ID.
            
        Returns:
            Status message.
        """
        employee = self.all_employees.get(employee_id)
        if employee is None:
            return f"Employee {employee_id} not found"
        
        new_dept = self.departments.get(new_dept_id)
        if new_dept is None:
            return f"Department {new_dept_id} not found"
        
        # Remove from current department
        if employee.department_id:
            old_dept = self.departments.get(employee.department_id)
            if old_dept:
                old_dept.remove_employee(employee_id)
        
        # Add to new department
        new_dept.add_employee(employee)
        return f"{employee.name} transferred to {new_dept.name}"
    
    def get_employee_count(self) -> int:
        """Get total employee count.
        
        Returns:
            Total number of employees.
        """
        return len(self.all_employees)
    
    def get_department_count(self) -> int:
        """Get number of departments.
        
        Returns:
            Department count.
        """
        return len(self.departments)
