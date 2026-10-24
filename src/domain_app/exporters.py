import json
from collections.abc import Iterable
from pathlib import Path
from domain_app.models import Employee

def export_employees_json(employees: Iterable[Employee], path: Path) -> int:
    """Exports employees to a JSON file atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    count = 0
    try:
        with temporary.open("w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for employee in employees:
                if not first:
                    file.write(",\n")
                json.dump(
                    {
                        "employee_id": employee.emp_id,
                        "name": employee.name,
                        "position": employee.role(),
                        "department": employee.department.name,
                        "salary": employee.salary.amount,
                    },
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
                first = False
                count += 1
            file.write("\n]\n")
        temporary.replace(path)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise
    return count