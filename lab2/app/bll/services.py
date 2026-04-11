import uuid
from datetime import datetime
from typing import List

from app.dal.interfaces import (
    IFinancialDataRepository,
    IFinancialMetricRepository,
    IReportRepository,
    IUserRepository,
)
from app.dal.models import (
    FinancialData,
    FinancialMetric,
    Report,
    ReportChart,
    ReportTable,
    User,
)


class FinancialService:

    def __init__(
        self,
        financial_data_repo: IFinancialDataRepository,
        metric_repo: IFinancialMetricRepository,
        report_repo: IReportRepository,
    ):
        self.financial_data_repo = financial_data_repo
        self.metric_repo = metric_repo
        self.report_repo = report_repo

    def load_from_csv(self, file_path: str) -> dict:

        raw_rows = self.financial_data_repo.read_from_csv(file_path)

        financial_records = []
        metrics = []

        for row in raw_rows:
            revenue = float(row["revenue"])
            expenses = float(row["expenses"])
            profit = revenue - expenses

            financial_records.append(FinancialData(
                period=row["period"],
                department=row["department"],
                revenue=revenue,
                expenses=expenses,
                profit=profit,
            ))

            roi = round((profit / revenue * 100) if revenue != 0 else 0.0, 4)
            metrics.append(FinancialMetric(
                name=f"ROI {row['period']} / {row['department']}",
                value=roi,
            ))

        self.financial_data_repo.add_many(financial_records)
        saved_metrics = self.metric_repo.add_many(metrics)

        report = Report(
            id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            tables=[ReportTable(rows=len(financial_records), columns=5)],
            charts=[ReportChart(type="bar"), ReportChart(type="line")],
            metrics=saved_metrics,
        )
        self.report_repo.add(report)

        return {
            "loaded_rows": len(financial_records),
            "metrics_created": len(saved_metrics),
            "report_id": report.id,
        }

    def get_all_financial_data(self) -> List[FinancialData]:
        return self.financial_data_repo.get_all()

    def get_all_reports(self) -> List[Report]:
        return self.report_repo.get_all()

    def get_report_by_id(self, report_id: str) -> Report | None:
        return self.report_repo.get_by_id(report_id)


class UserService:

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_all(self) -> List[User]:
        return self.user_repo.get_all()

    def create_user(self, name: str, role: str) -> User:
        if role not in ("analyst", "manager"):
            raise ValueError(f"Невідома роль '{role}'. Допустимі: analyst, manager")
        user = User(id=str(uuid.uuid4()), name=name, role=role)
        return self.user_repo.add(user)
