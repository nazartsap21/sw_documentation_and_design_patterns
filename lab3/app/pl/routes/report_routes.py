from flasgger import swag_from
from flask import Blueprint, render_template, flash, redirect, url_for

from app.database import SessionLocal
from app.dal.repositories import FinancialDataRepository, ReportRepository, FinancialMetricRepository
from app.bll.services import ReportService

report_bp = Blueprint("reports", __name__, url_prefix="/reports")


def make_service(db) -> ReportService:
    return ReportService(
        report_repo=ReportRepository(db),
        metric_repo=FinancialMetricRepository(db),
        financial_repo=FinancialDataRepository(db),
    )


@report_bp.get("/")
@swag_from({
    "tags": ["Reports"],
    "summary": "List all reports",
    "responses": {
        200: {"description": "HTML page with a table of all generated reports"},
    },
})
def index():
    db = SessionLocal()
    try:
        service = make_service(db)
        reports = service.get_all()
        return render_template("reports/index.html", reports=reports)
    finally:
        db.close()


@report_bp.post("/generate")
@swag_from({
    "tags": ["Reports"],
    "summary": "Generate a new report from current financial data",
    "description": (
        "Reads all FinancialData records, computes ROI (profit/revenue×100) per record as "
        "FinancialMetrics, and creates a Report with one ReportTable (dataset dimensions), "
        "two ReportCharts (bar, line), and all computed metrics."
    ),
    "responses": {
        302: {"description": "Redirect to the new report's detail page on success"},
        400: {"description": "No financial data found — add records before generating"},
    },
})
def generate():
    db = SessionLocal()
    try:
        service = make_service(db)
        report = service.generate()
        flash(f"Report {report.id[:8]}… generated successfully.", "success")
        return redirect(url_for("reports.detail", report_id=report.id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("reports.index"))
    finally:
        db.close()


@report_bp.get("/<report_id>")
@swag_from({
    "tags": ["Reports"],
    "summary": "Show report detail",
    "parameters": [
        {"in": "path", "name": "report_id", "type": "string", "required": True,
         "description": "UUID of the report"},
    ],
    "responses": {
        200: {"description": "HTML detail page showing tables, charts, and ROI metrics"},
        302: {"description": "Redirect to reports list if report not found"},
    },
})
def detail(report_id: str):
    db = SessionLocal()
    try:
        service = make_service(db)
        report = service.get_by_id(report_id)
        if not report:
            flash("Report not found.", "danger")
            return redirect(url_for("reports.index"))
        return render_template("reports/detail.html", report=report)
    finally:
        db.close()
