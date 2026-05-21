import uuid
from datetime import datetime
from typing import List, Optional

from app.dal.interfaces import (
    IFinancialDataRepository,
    IFinancialMetricRepository,
    IReportRepository,
    IUserRepository,
)
from app.dal.models import FinancialData, FinancialMetric, Report, ReportChart, ReportTable, User


class FinancialDataService:

    def __init__(self, repo: IFinancialDataRepository):
        self.repo = repo

    def get_all(self) -> List[FinancialData]:
        return self.repo.get_all()

    def get_by_id(self, record_id: int) -> Optional[FinancialData]:
        return self.repo.get_by_id(record_id)

    def create(self, period: str, department: str, revenue: float, expenses: float) -> FinancialData:
        profit = round(revenue - expenses, 2)
        record = FinancialData(
            period=period,
            department=department,
            revenue=revenue,
            expenses=expenses,
            profit=profit,
        )
        return self.repo.add(record)

    def update(self, record_id: int, period: str, department: str, revenue: float, expenses: float) -> Optional[FinancialData]:
        record = self.repo.get_by_id(record_id)
        if not record:
            return None
        record.period = period
        record.department = department
        record.revenue = revenue
        record.expenses = expenses
        record.profit = round(revenue - expenses, 2)
        return self.repo.update(record)

    def delete(self, record_id: int) -> bool:
        return self.repo.delete(record_id)


class ReportService:

    def __init__(self, report_repo: IReportRepository, metric_repo: IFinancialMetricRepository,
                 financial_repo: IFinancialDataRepository):
        self.report_repo = report_repo
        self.metric_repo = metric_repo
        self.financial_repo = financial_repo

    def get_all(self) -> List[Report]:
        return self.report_repo.get_all()

    def get_by_id(self, report_id: str) -> Optional[Report]:
        return self.report_repo.get_by_id(report_id)

    def generate(self) -> Report:
        records = self.financial_repo.get_all()
        if not records:
            raise ValueError("No financial data found. Add records before generating a report.")

        metrics = []
        for r in records:
            roi = round((r.profit / r.revenue * 100) if r.revenue != 0 else 0.0, 4)
            metric = FinancialMetric(
                name=f"ROI {r.period} / {r.department}",
                value=roi,
            )
            metrics.append(metric)

        saved_metrics = self.metric_repo.add_many(metrics)

        report = Report(
            id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            tables=[ReportTable(rows=len(records), columns=5)],
            charts=[ReportChart(type="bar"), ReportChart(type="line")],
            metrics=saved_metrics,
        )
        return self.report_repo.add(report)


class UserService:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def get_all(self) -> List[User]:
        return self.repo.get_all()

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def create(self, name: str, role: str) -> User:
        if role not in ("analyst", "manager"):
            raise ValueError(f"Unknown role '{role}'. Allowed: analyst, manager")
        user = User(id=str(uuid.uuid4()), name=name, role=role)
        return self.repo.add(user)

    def delete(self, user_id: str) -> bool:
        return self.repo.delete(user_id)
