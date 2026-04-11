from abc import ABC, abstractmethod


class IFinancialController(ABC):

    @abstractmethod
    def load_data(self) -> tuple:
        pass

    @abstractmethod
    def get_all_financial_data(self) -> tuple:
        pass


class IReportController(ABC):

    @abstractmethod
    def get_all_reports(self) -> tuple:
        pass

    @abstractmethod
    def get_report(self, report_id: str) -> tuple:
        pass


class IUserController(ABC):

    @abstractmethod
    def get_all_users(self) -> tuple:
        pass

    @abstractmethod
    def create_user(self) -> tuple:
        pass
