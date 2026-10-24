import pytest
from domain_app.models import Department, Developer, Manager
from domain_app.value_objects import Money


@pytest.fixture
def it_department() -> Department:
    return Department(dept_id=1, name="IT")


@pytest.fixture
def developer_anna(it_department) -> Developer:
    return Developer(1, "Anna Koval", it_department, Money(25000), ["Python", "Django"])


@pytest.fixture
def developer_oleh(it_department) -> Developer:
    return Developer(2, "Oleh Melnyk", it_department, Money(18000), ["Python", "FastAPI"])


@pytest.fixture
def manager_iryna(it_department) -> Manager:
    return Manager(3, "Iryna Bondar", it_department, Money(30000), team_size=5)


@pytest.fixture
def sample_employees(developer_anna, developer_oleh, manager_iryna) -> list:
    return [developer_anna, developer_oleh, manager_iryna]