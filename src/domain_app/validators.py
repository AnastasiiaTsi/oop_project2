from domain_app.exceptions import RecordValidationError
from domain_app.models import Developer, Department
from domain_app.value_objects import Money

def parse_employee(
    row: dict[str, str],
    *,
    line_number: int,
    allowed_departments: set[str],
) -> Developer:
    """Parses and validates a single CSV row into a Developer domain object."""
    try:
        employee_id = int(row["employee_id"])
    except (KeyError, ValueError) as error:
        raise RecordValidationError(
            "Invalid employee ID", line_number=line_number, field="employee_id"
        ) from error

    name = row.get("name", "").strip()
    if not name:
        raise RecordValidationError(
            "Employee name is empty", line_number=line_number, field="name"
        )

    department = row.get("department", "").strip()
    if department not in allowed_departments:
        raise RecordValidationError(
            f"Department '{department}' is not allowed",
            line_number=line_number,
            field="department",
        )

    try:
        salary = float(row["salary"])
    except (KeyError, ValueError) as error:
        raise RecordValidationError(
            "Invalid salary", line_number=line_number, field="salary"
        ) from error

    # Створюємо тимчасовий Department для доменного об'єкта
    dept = Department(dept_id=1, name=department)
    return Developer(employee_id, name, dept, Money(salary), [])