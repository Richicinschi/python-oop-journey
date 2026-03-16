"""Problem 02: Employee Hierarchy

Topic: Inheritance with super()
Difficulty: Easy

Create an Employee base class and three derived classes demonstrating
proper use of super() and extending parent functionality.
"""

from __future__ import annotations


class Employee:
    """Base class for all employees.
    
    Attributes:
        name: Employee's full name
        employee_id: Unique employee identifier
        base_salary: Base annual salary
    """
    
    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        """Initialize an Employee.
        
        Args:
            name: Employee's full name
            employee_id: Unique identifier
            base_salary: Annual base salary
        """
        raise NotImplementedError("Implement Employee.__init__")
    
    def get_details(self) -> str:
        """Return basic employee details.
        
        Returns:
            String in format: "Name: X, ID: Y"
        """
        raise NotImplementedError("Implement Employee.get_details")
    
    def calculate_salary(self) -> float:
        """Calculate total salary (base by default).
        
        Returns:
            Base salary amount
        """
        raise NotImplementedError("Implement Employee.calculate_salary")
    
    def get_role(self) -> str:
        """Return the employee role.
        
        Returns:
            "Employee"
        """
        raise NotImplementedError("Implement Employee.get_role")


class Manager(Employee):
    """A manager is an employee with a bonus and reports.
    
    Additional Attributes:
        bonus_rate: Percentage bonus on base salary (e.g., 0.20 for 20%)
        department: Manager's department
        reports: List of employees managed
    """
    
    def __init__(self, name: str, employee_id: str, base_salary: float, 
                 bonus_rate: float, department: str) -> None:
        """Initialize a Manager.
        
        Args:
            name: Manager's full name
            employee_id: Unique identifier
            base_salary: Annual base salary
            bonus_rate: Bonus as decimal (e.g., 0.20)
            department: Department name
        """
        raise NotImplementedError("Implement Manager.__init__")
    
    def get_details(self) -> str:
        """Override: Include department and report count.
        
        Returns:
            Base details + ", Dept: X, Reports: Y"
        """
        raise NotImplementedError("Implement Manager.get_details")
    
    def calculate_salary(self) -> float:
        """Override: Include bonus in salary calculation.
        
        Returns:
            Base salary + (base_salary * bonus_rate)
        """
        raise NotImplementedError("Implement Manager.calculate_salary")
    
    def get_role(self) -> str:
        """Override: Return Manager role.
        
        Returns:
            "Manager"
        """
        raise NotImplementedError("Implement Manager.get_role")
    
    def add_report(self, employee: Employee) -> None:
        """Add an employee to this manager's reports.
        
        Args:
            employee: Employee to add as a report
        """
        raise NotImplementedError("Implement Manager.add_report")
    
    def get_report_count(self) -> int:
        """Return the number of direct reports.
        
        Returns:
            Count of employees in reports list
        """
        raise NotImplementedError("Implement Manager.get_report_count")


class Engineer(Employee):
    """An engineer is an employee with a specialization.
    
    Additional Attributes:
        specialization: Engineering field (e.g., "Backend", "Frontend")
        years_experience: Years of engineering experience
        certifications: List of certifications
    """
    
    def __init__(self, name: str, employee_id: str, base_salary: float,
                 specialization: str, years_experience: int) -> None:
        """Initialize an Engineer.
        
        Args:
            name: Engineer's full name
            employee_id: Unique identifier
            base_salary: Annual base salary
            specialization: Engineering specialization
            years_experience: Years of experience
        """
        raise NotImplementedError("Implement Engineer.__init__")
    
    def get_details(self) -> str:
        """Override: Include specialization and experience.
        
        Returns:
            Base details + ", Spec: X, Exp: Y years"
        """
        raise NotImplementedError("Implement Engineer.get_details")
    
    def get_role(self) -> str:
        """Override: Return Engineer role.
        
        Returns:
            "Engineer"
        """
        raise NotImplementedError("Implement Engineer.get_role")
    
    def add_certification(self, certification: str) -> None:
        """Add a certification to the engineer's list.
        
        Args:
            certification: Certification name to add
        """
        raise NotImplementedError("Implement Engineer.add_certification")
    
    def calculate_salary(self) -> float:
        """Override: Add $2000 per year of experience.
        
        Returns:
            Base salary + (years_experience * 2000)
        """
        raise NotImplementedError("Implement Engineer.calculate_salary")


class Salesperson(Employee):
    """A salesperson is an employee with commission.
    
    Additional Attributes:
        commission_rate: Commission percentage as decimal
        sales_made: Total sales amount
        territory: Sales territory/region
    """
    
    def __init__(self, name: str, employee_id: str, base_salary: float,
                 commission_rate: float, territory: str) -> None:
        """Initialize a Salesperson.
        
        Args:
            name: Salesperson's full name
            employee_id: Unique identifier
            base_salary: Annual base salary
            commission_rate: Commission as decimal (e.g., 0.05)
            territory: Sales territory
        """
        raise NotImplementedError("Implement Salesperson.__init__")
    
    def get_details(self) -> str:
        """Override: Include territory.
        
        Returns:
            Base details + ", Territory: X"
        """
        raise NotImplementedError("Implement Salesperson.get_details")
    
    def get_role(self) -> str:
        """Override: Return Salesperson role.
        
        Returns:
            "Salesperson"
        """
        raise NotImplementedError("Implement Salesperson.get_role")
    
    def make_sale(self, amount: float) -> None:
        """Record a sale.
        
        Args:
            amount: Sale amount to add to sales_made
        """
        raise NotImplementedError("Implement Salesperson.make_sale")
    
    def calculate_salary(self) -> float:
        """Override: Include commission on sales.
        
        Returns:
            Base salary + (sales_made * commission_rate)
        """
        raise NotImplementedError("Implement Salesperson.calculate_salary")
