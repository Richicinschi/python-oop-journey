"""Reference solution for Problem 02: Employee Hierarchy."""

from __future__ import annotations


class Employee:
    """Base class for all employees."""
    
    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        self.name = name
        self.employee_id = employee_id
        self.base_salary = base_salary
    
    def get_details(self) -> str:
        return f"Name: {self.name}, ID: {self.employee_id}"
    
    def calculate_salary(self) -> float:
        return self.base_salary
    
    def get_role(self) -> str:
        return "Employee"


class Manager(Employee):
    """A manager is an employee with a bonus and reports."""
    
    def __init__(self, name: str, employee_id: str, base_salary: float, 
                 bonus_rate: float, department: str) -> None:
        super().__init__(name, employee_id, base_salary)
        self.bonus_rate = bonus_rate
        self.department = department
        self._reports: list[Employee] = []
    
    def get_details(self) -> str:
        base = super().get_details()
        return f"{base}, Dept: {self.department}, Reports: {len(self._reports)}"
    
    def calculate_salary(self) -> float:
        return self.base_salary + (self.base_salary * self.bonus_rate)
    
    def get_role(self) -> str:
        return "Manager"
    
    def add_report(self, employee: Employee) -> None:
        self._reports.append(employee)
    
    def get_report_count(self) -> int:
        return len(self._reports)


class Engineer(Employee):
    """An engineer is an employee with a specialization."""
    
    def __init__(self, name: str, employee_id: str, base_salary: float,
                 specialization: str, years_experience: int) -> None:
        super().__init__(name, employee_id, base_salary)
        self.specialization = specialization
        self.years_experience = years_experience
        self._certifications: list[str] = []
    
    def get_details(self) -> str:
        base = super().get_details()
        return f"{base}, Spec: {self.specialization}, Exp: {self.years_experience} years"
    
    def get_role(self) -> str:
        return "Engineer"
    
    def add_certification(self, certification: str) -> None:
        self._certifications.append(certification)
    
    def calculate_salary(self) -> float:
        return self.base_salary + (self.years_experience * 2000)


class Salesperson(Employee):
    """A salesperson is an employee with commission."""
    
    def __init__(self, name: str, employee_id: str, base_salary: float,
                 commission_rate: float, territory: str) -> None:
        super().__init__(name, employee_id, base_salary)
        self.commission_rate = commission_rate
        self.territory = territory
        self._sales_made: float = 0.0
    
    def get_details(self) -> str:
        base = super().get_details()
        return f"{base}, Territory: {self.territory}"
    
    def get_role(self) -> str:
        return "Salesperson"
    
    def make_sale(self, amount: float) -> None:
        self._sales_made += amount
    
    def calculate_salary(self) -> float:
        return self.base_salary + (self._sales_made * self.commission_rate)
