from typing import List, Optional

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

    def get_by_id(self, record_id: int) -> Optional[FinancialData]:
        return self.db.query(FinancialData).filter(FinancialData.id == record_id).first()

    def add(self, item: FinancialData) -> FinancialData:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: FinancialData) -> FinancialData:
        self.db.merge(item)
        self.db.commit()
        return self.get_by_id(item.id)

    def delete(self, record_id: int) -> bool:
        item = self.get_by_id(record_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True


class FinancialMetricRepository(IFinancialMetricRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[FinancialMetric]:
        return self.db.query(FinancialMetric).all()

    def add_many(self, items: List[FinancialMetric]) -> List[FinancialMetric]:
        self.db.add_all(items)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items


class ReportRepository(IReportRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Report]:
        return self.db.query(Report).all()

    def get_by_id(self, report_id: str) -> Optional[Report]:
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

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def add(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: str) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
