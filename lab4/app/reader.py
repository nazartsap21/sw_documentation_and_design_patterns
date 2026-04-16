import csv
from typing import Dict, Iterator, Optional


def read_csv(file_path: str, max_rows: Optional[int] = None) -> Iterator[Dict[str, str]]:
    with open(file_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for count, row in enumerate(reader, start=1):
            yield dict(row)
            if max_rows is not None and count >= max_rows:
                break
