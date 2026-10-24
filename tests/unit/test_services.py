from unittest.mock import Mock, AsyncMock
import pytest
from domain_app.protocols import PaymentGateway, Notifier
from domain_app.services import PayrollService, AsyncPayrollProvider
from domain_app.repositories import InMemoryRepository


def _make_service(sample_employees):
    repo = InMemoryRepository()
    for e in sample_employees:
        repo.add(e)
    gateway = Mock(spec=PaymentGateway)
    notifier = Mock(spec=Notifier)
    return PayrollService(repository=repo, gateway=gateway, notifier=notifier)


def test_payroll_average_salary(sample_employees):
    service = _make_service(sample_employees)
    assert service.calculate_average_salary() == pytest.approx(24333.33, rel=1e-3)


def test_payroll_max_salary(sample_employees):
    service = _make_service(sample_employees)
    best = service.find_max_salary_employee()
    assert best is not None
    assert best.name == "Iryna Bondar"
    assert best.salary.amount == 30000


def test_payroll_empty_repository():
    repo = InMemoryRepository()
    gateway = Mock(spec=PaymentGateway)
    notifier = Mock(spec=Notifier)
    service = PayrollService(repository=repo, gateway=gateway, notifier=notifier)
    assert service.calculate_average_salary() == 0.0
    assert service.find_max_salary_employee() is None


def test_payroll_total(sample_employees):
    service = _make_service(sample_employees)
    total = service.calculate_total_payroll()
    assert total.amount == pytest.approx(73000)


def test_process_salary_interaction(developer_anna):
    repo = InMemoryRepository()
    repo.add(developer_anna)
    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = "PAY-001"
    notifier = Mock(spec=Notifier)
    service = PayrollService(repository=repo, gateway=gateway, notifier=notifier)
    
    record = service.process_salary(developer_anna, "October")
    
    assert record.emp_id == 1
    assert record.amount.amount == 25000
    gateway.process_payment.assert_called_once_with(developer_anna.salary)
    notifier.send.assert_called_once_with(
        "Anna Koval",
        "Salary paid for October. Payment: PAY-001",
    )


def test_process_salary_payment_failure(developer_anna):
    repo = InMemoryRepository()
    repo.add(developer_anna)
    
    class PaymentError(Exception):
        pass
    
    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.side_effect = PaymentError("Gateway unavailable")
    notifier = Mock(spec=Notifier)
    service = PayrollService(repository=repo, gateway=gateway, notifier=notifier)
    
    with pytest.raises(PaymentError, match="Gateway unavailable"):
        service.process_salary(developer_anna, "October")
    
    notifier.send.assert_not_called()


@pytest.mark.asyncio
async def test_async_payroll_provider():
    client = AsyncMock()
    client.fetch_status.return_value = {"status": "paid"}
    provider = AsyncPayrollProvider(client)
    status = await provider.get_status("PAY-001")
    assert status == "paid"
    client.fetch_status.assert_awaited_once_with("PAY-001")


@pytest.mark.asyncio
async def test_async_payroll_provider_failure():
    client = AsyncMock()
    client.fetch_status.side_effect = ConnectionError("Network error")
    provider = AsyncPayrollProvider(client)
    with pytest.raises(ConnectionError):
        await provider.get_status("PAY-001")