from domain_app.models import Manager, Developer, Department
from domain_app.value_objects import Money
from domain_app.repositories import InMemoryRepository
from domain_app.services import PayrollService, DemoPaymentGateway, ConsoleNotifier

def main() -> None:
    it_dept = Department(dept_id=1, name="IT")
    finance_dept = Department(dept_id=2, name="Finance")

    dev1 = Developer(1, "Anna Koval", it_dept, Money(25000), ["Python", "Django"])
    dev2 = Developer(2, "Oleh Melnyk", it_dept, Money(18000), ["Python", "FastAPI"])
    mgr1 = Manager(3, "Iryna Bondar", finance_dept, Money(30000), team_size=5)

    repo = InMemoryRepository()
    for e in [dev1, dev2, mgr1]:
        repo.add(e)
        e.department.add_employee(e)

    service = PayrollService(
        repository=repo,
        gateway=DemoPaymentGateway(),
        notifier=ConsoleNotifier()
    )

    print(f"Average salary: {service.calculate_average_salary():.2f}")
    print(f"Total payroll: {service.calculate_total_payroll()}")

    best = service.find_max_salary_employee()
    if best:
        print(f"Max salary: {best.name} ({best.salary})")

    service.process_salary(dev1, "October")

if __name__ == "__main__":
    main()