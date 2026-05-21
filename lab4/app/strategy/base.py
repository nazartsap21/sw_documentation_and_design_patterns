from abc import ABC, abstractmethod
from typing import Dict


class IOutputStrategy(ABC):
    """Abstract base for all output strategies (Strategy pattern)."""

    @abstractmethod
    def output(self, row: Dict[str, str]) -> None:
        """Send a single data row to the target storage."""
        pass

    def close(self) -> None:
        """Release any resources held by this strategy (optional override)."""
        pass
