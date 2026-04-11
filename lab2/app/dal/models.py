from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database import Base


report_metric = Table(
    "report_metrics",
    Base.metadata,
    Column("report_id", String(36), ForeignKey("reports.id")),
    Column("metric_id", Integer, ForeignKey("financial_metrics.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(20), nullable=False)
    department = Column(String(100), nullable=False)
    revenue = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)


class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)

    reports = relationship("Report", secondary=report_metric, back_populates="metrics")


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tables = relationship("ReportTable", back_populates="report", cascade="all, delete-orphan")
    charts = relationship("ReportChart", back_populates="report", cascade="all, delete-orphan")

    metrics = relationship("FinancialMetric", secondary=report_metric, back_populates="reports")


class ReportTable(Base):
    __tablename__ = "report_tables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(String(36), ForeignKey("reports.id"), nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)

    report = relationship("Report", back_populates="tables")


class ReportChart(Base):
    __tablename__ = "report_charts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(String(36), ForeignKey("reports.id"), nullable=False)
    type = Column(String(20), nullable=False)

    report = relationship("Report", back_populates="charts")
