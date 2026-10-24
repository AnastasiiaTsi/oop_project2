import pytest
from domain_app.config import get_payroll_mode


def test_payroll_mode_from_env(monkeypatch):
    monkeypatch.setenv("PAYROLL_MODE", "production")
    assert get_payroll_mode() == "production"


def test_default_payroll_mode(monkeypatch):
    monkeypatch.delenv("PAYROLL_MODE", raising=False)
    assert get_payroll_mode() == "sandbox"