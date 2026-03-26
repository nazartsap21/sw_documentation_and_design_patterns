import csv
from typing import List

from sqlalchemy.orm import Session

from app.dal.interfaces import (
    IFinancialDataRepository,
    IFinancialMetricRepository,
    IReportRepository,
    IUserRepository,
)
from app.dal.models import FinancialData, FinancialMetric, Report, User


class FinancialDataRepository(IFinancialDataRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[FinancialData]:
        return self.db.query(FinancialData).all()

    def add_many(self, items: List[FinancialData]) -> None:
        self.db.bulk_save_objects(items)
        self.db.commit()

    def read_from_csv(self, file_path: str) -> List[dict]:
        rows = []
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows


class FinancialMetricRepository(IFinancialMetricRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[FinancialMetric]:
        return self.db.query(FinancialMetric).all()

    def add_many(self, items: List[FinancialMetric]) -> List[FinancialMetric]:
        for item in items:
            self.db.add(item)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items


class ReportRepository(IReportRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Report]:
        return self.db.query(Report).all()

    def get_by_id(self, report_id: str) -> Report | None:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def add(self, report: Report) -> Report:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report


class UserRepository(IUserRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def add(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
