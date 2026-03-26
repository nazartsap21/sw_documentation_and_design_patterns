from flask import Blueprint, jsonify, request

from app.database import SessionLocal
from app.dal.repositories import (
    FinancialDataRepository,
    FinancialMetricRepository,
    ReportRepository,
    UserRepository,
)
from app.bll.services import FinancialService, UserService

api = Blueprint("api", __name__)

CSV_FILE_PATH = "financial_data.csv"


def make_financial_service(db) -> FinancialService:
    return FinancialService(
        financial_data_repo=FinancialDataRepository(db),
        metric_repo=FinancialMetricRepository(db),
        report_repo=ReportRepository(db),
    )

def make_user_service(db) -> UserService:
    return UserService(user_repo=UserRepository(db))


@api.post("/load-data")
def load_data():
    db = SessionLocal()
    try:
        service = make_financial_service(db)
        result = service.load_from_csv(CSV_FILE_PATH)
        return jsonify({"status": "ok", **result}), 200
    except FileNotFoundError:
        return jsonify({"error": f"File '{CSV_FILE_PATH}' not found. Please run generate_csv.py first."}), 404
    finally:
        db.close()


@api.get("/financial-data")
def get_financial_data():
    db = SessionLocal()
    try:
        service = make_financial_service(db)
        records = service.get_all_financial_data()
        return jsonify([
            {
                "id": r.id,
                "period": r.period,
                "department": r.department,
                "revenue": r.revenue,
                "expenses": r.expenses,
                "profit": r.profit,
            }
            for r in records
        ]), 200
    finally:
        db.close()


@api.get("/reports")
def get_reports():
    db = SessionLocal()
    try:
        service = make_financial_service(db)
        reports = service.get_all_reports()
        return jsonify([
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "tables_count": len(r.tables),
                "charts_count": len(r.charts),
                "metrics_count": len(r.metrics),
            }
            for r in reports
        ]), 200
    finally:
        db.close()


@api.get("/reports/<report_id>")
def get_report(report_id: str):
    db = SessionLocal()
    try:
        service = make_financial_service(db)
        report = service.get_report_by_id(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404
        return jsonify({
            "id": report.id,
            "created_at": report.created_at.isoformat(),
            "tables": [{"rows": t.rows, "columns": t.columns} for t in report.tables],
            "charts": [{"type": c.type} for c in report.charts],
            "metrics": [{"name": m.name, "value": m.value} for m in report.metrics],
        }), 200
    finally:
        db.close()


@api.get("/users")
def get_users():
    db = SessionLocal()
    try:
        service = make_user_service(db)
        users = service.get_all()
        return jsonify([
            {"id": u.id, "name": u.name, "role": u.role}
            for u in users
        ]), 200
    finally:
        db.close()


@api.post("/users")
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "role" not in data:
        return jsonify({"error": "Required fields: name, role"}), 400

    db = SessionLocal()
    try:
        service = make_user_service(db)
        user = service.create_user(name=data["name"], role=data["role"])
        return jsonify({"id": user.id, "name": user.name, "role": user.role}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
