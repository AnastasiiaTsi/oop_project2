from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from domain_app.value_objects import Money

class Employee(ABC):
    def __init__(self, emp_id: int, name: str, department: "Department", salary: Money) -> None:
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self._salary = salary

    @property
    def salary(self) -> Money:
        return self._salary

    @salary.setter
    def salary(self, value: Money) -> None:
        if value.amount < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value

    @abstractmethod
    def role(self) -> str:
        ...

    def __str__(self) -> str:
        return f"{self.name} ({self.role()}) - {self.salary}"

class Manager(Employee):
    def __init__(self, emp_id: int, name: str, department: "Department", salary: Money, team_size: int) -> None:
        super().__init__(emp_id, name, department, salary)
        self.team_size = team_size

    def role(self) -> str:
        return "Manager"

class Developer(Employee):
    def __init__(self, emp_id: int, name: str, department: "Department", salary: Money, tech_stack: list[str]) -> None:
        super().__init__(emp_id, name, department, salary)
        self.tech_stack = tech_stack

    def role(self) -> str:
        return "Developer"

@dataclass
class Department:
    dept_id: int
    name: str
    employees: list[Employee] = field(default_factory=list)

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def __len__(self) -> int:
        return len(self.employees)

@dataclass
class PayrollRecord:
    emp_id: int
    amount: Money
    month: str

    def __post_init__(self) -> None:
        if self.amount.amount <= 0:
            raise ValueError("Payroll amount must be positive")