import pytest
from domain_app.models import Employee, Manager, Developer, Department
from domain_app.value_objects import Money


def test_create_manager(it_department):
    manager = Manager(1, "Iryna Bondar", it_department, Money(30000), team_size=5)
    assert manager.name == "Iryna Bondar"
    assert manager.role() == "Manager"
    assert manager.salary.amount == 30000
    assert manager.team_size == 5


def test_create_developer(it_department):
    dev = Developer(1, "Anna Koval", it_department, Money(25000), tech_stack=["Python"])
    assert dev.name == "Anna Koval"
    assert dev.role() == "Developer"
    assert "Python" in dev.tech_stack


def test_negative_salary_rejected(it_department):
    with pytest.raises(ValueError, match="negative"):
        Money(-1, "UAH")


def test_currency_mismatch():
    with pytest.raises(ValueError, match="Currency mismatch"):
        Money(100, "UAH") + Money(10, "USD")


@pytest.mark.parametrize(
    "salary,expected",
    [
        (0, 0),
        (0.01, 0.01),
        (25000, 25000),
        (999999.99, 999999.99),
    ],
    ids=["zero", "minimum", "normal", "maximum"],
)
def test_valid_salary_amounts(salary, expected, it_department):
    money = Money(salary)
    assert money.amount == pytest.approx(expected)


@pytest.mark.parametrize("salary", [-1, -100, -9999.99])
def test_invalid_salary_amounts(salary):
    with pytest.raises(ValueError, match="negative"):
        Money(salary)


def test_department_len(it_department, developer_anna, developer_oleh):
    it_department.add_employee(developer_anna)
    it_department.add_employee(developer_oleh)
    assert len(it_department) == 2