from typing import Dict

from app.strategy.base import IOutputStrategy

_DISPLAY_FIELDS = (
    "BEGIN_YEARMONTH", "STATE", "EVENT_TYPE",
    "BEGIN_DATE_TIME", "END_DATE_TIME",
    "INJURIES_DIRECT", "DEATHS_DIRECT",
    "DAMAGE_PROPERTY", "DAMAGE_CROPS",
    "BEGIN_LOCATION", "END_LOCATION",
)


class ConsoleOutputStrategy(IOutputStrategy):
    """Prints each row as a formatted line to stdout."""

    def output(self, row: Dict[str, str]) -> None:
        fields = {k: row[k] for k in _DISPLAY_FIELDS if k in row} or row
        line = " | ".join(f"{k}: {v}" for k, v in fields.items())
        print(line)
