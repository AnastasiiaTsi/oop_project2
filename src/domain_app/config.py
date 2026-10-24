import os

def get_payroll_mode() -> str:
    """Returns the payroll mode from env variables."""
    return os.getenv("PAYROLL_MODE", "sandbox")