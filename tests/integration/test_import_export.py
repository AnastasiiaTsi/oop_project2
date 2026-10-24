import json
import pytest
from domain_app.exporters import export_employees_json
from domain_app.readers import read_csv_rows
from domain_app.validators import parse_employee


@pytest.mark.integration
def test_csv_import_and_json_export(tmp_path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "employee_id,name,position,department,salary\n"
        "1,Anna Koval,Developer,IT,25000\n"
        "2,Oleh Melnyk,QA Engineer,IT,18000\n",
        encoding="utf-8",
    )
    
    employees = []
    for line_num, row in read_csv_rows(csv_file):
        employees.append(
            parse_employee(row, line_number=line_num, allowed_departments={"IT"})
        )
    
    assert len(employees) == 2
    
    output_file = tmp_path / "output" / "employees.json"
    count = export_employees_json(employees, output_file)
    
    assert count == 2
    assert output_file.exists()
    
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["name"] == "Anna Koval"
    assert data[1]["salary"] == pytest.approx(18000.0)