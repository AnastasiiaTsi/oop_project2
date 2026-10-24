import csv
from collections.abc import Iterator
from pathlib import Path

def read_csv_rows(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    """Streams CSV rows as tuples of (line_number, row_dict)."""
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=2):
            yield line_number, row