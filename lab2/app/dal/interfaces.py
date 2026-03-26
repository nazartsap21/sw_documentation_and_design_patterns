from abc import ABC, abstractmethod
from typing import List

from app.dal.models import FinancialData, FinancialMetric, Report, User


class IFinancialDataRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[FinancialData]:
        pass

    @abstractmethod
    def add_many(self, items: List[FinancialData]) -> None:
        pass

    @abstractmethod
    def read_from_csv(self, file_path: str) -> List[dict]:
        pass


class IFinancialMetricRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[FinancialMetric]:
        pass

    @abstractmethod
    def add_many(self, items: List[FinancialMetric]) -> List[FinancialMetric]:
        pass


class IReportRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Report]:
        pass

    @abstractmethod
    def get_by_id(self, report_id: str) -> Report | None:
        pass

    @abstractmethod
    def add(self, report: Report) -> Report:
        pass


class IUserRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> User:
        pass
