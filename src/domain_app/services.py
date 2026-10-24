from domain_app.models import Employee, PayrollRecord
from domain_app.protocols import PaymentGateway, Notifier
from domain_app.repositories import InMemoryRepository
from domain_app.value_objects import Money

class DemoPaymentGateway:
    def process_payment(self, amount: Money) -> str:
        print(f"Processed payment: {amount}")
        return "PAY-001"

class ConsoleNotifier:
    def send(self, recipient: str, message: str) -> None:
        print(f"Notification to {recipient}: {message}")

class PayrollService:
    def __init__(
        self,
        repository: InMemoryRepository[Employee],
        gateway: PaymentGateway,
        notifier: Notifier,
    ) -> None:
        self._repository = repository
        self._gateway = gateway
        self._notifier = notifier

    def calculate_average_salary(self) -> float:
        employees = self._repository.all()
        if not employees:
            return 0.0
        total = sum(e.salary.amount for e in employees)
        return total / len(employees)

    def calculate_total_payroll(self) -> Money:
        employees = self._repository.all()
        total_amount = sum(e.salary.amount for e in employees)
        return Money(total_amount, "UAH")

    def find_max_salary_employee(self) -> Employee | None:
        employees = self._repository.all()
        if not employees:
            return None
        return max(employees, key=lambda e: e.salary.amount)

    def process_salary(self, employee: Employee, month: str) -> PayrollRecord:
        payment_id = self._gateway.process_payment(employee.salary)
        self._notifier.send(employee.name, f"Salary paid for {month}. Payment: {payment_id}")
        return PayrollRecord(emp_id=employee.emp_id, amount=employee.salary, month=month)

class AsyncPayrollProvider:
    def __init__(self, client) -> None:
        self._client = client

    async def get_status(self, payment_id: str) -> str:
        data = await self._client.fetch_status(payment_id)
        return data["status"]