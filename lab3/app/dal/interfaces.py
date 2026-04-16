from abc import ABC, abstractmethod
from typing import List, Optional

from app.dal.models import FinancialData, FinancialMetric, Report, User


class IFinancialDataRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[FinancialData]:
        pass

    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[FinancialData]:
        pass

    @abstractmethod
    def add(self, item: FinancialData) -> FinancialData:
        pass

    @abstractmethod
    def update(self, item: FinancialData) -> FinancialData:
        pass

    @abstractmethod
    def delete(self, record_id: int) -> bool:
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
    def get_by_id(self, report_id: str) -> Optional[Report]:
        pass

    @abstractmethod
    def add(self, report: Report) -> Report:
        pass


class IUserRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        pass
