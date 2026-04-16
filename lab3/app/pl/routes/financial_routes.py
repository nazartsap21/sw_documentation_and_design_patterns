from flasgger import swag_from
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database import SessionLocal
from app.dal.repositories import FinancialDataRepository
from app.bll.services import FinancialDataService

financial_bp = Blueprint("financial", __name__, url_prefix="/financial")


def make_service(db) -> FinancialDataService:
    return FinancialDataService(repo=FinancialDataRepository(db))


@financial_bp.get("/")
@swag_from({
    "tags": ["Financial Data"],
    "summary": "List all financial records",
    "responses": {
        200: {"description": "HTML page with a table of all financial records"},
    },
})
def index():
    db = SessionLocal()
    try:
        service = make_service(db)
        records = service.get_all()
        return render_template("financial/index.html", records=records)
    finally:
        db.close()


@financial_bp.get("/create")
@swag_from({
    "tags": ["Financial Data"],
    "summary": "Show create financial record form",
    "responses": {
        200: {"description": "HTML form to create a new financial record"},
    },
})
def create_form():
    return render_template("financial/create.html")


@financial_bp.post("/create")
@swag_from({
    "tags": ["Financial Data"],
    "summary": "Create a new financial record",
    "consumes": ["application/x-www-form-urlencoded"],
    "parameters": [
        {"in": "formData", "name": "period", "type": "string", "required": True,
         "description": "Reporting period, e.g. 2024-Q1"},
        {"in": "formData", "name": "department", "type": "string", "required": True,
         "description": "Department name"},
        {"in": "formData", "name": "revenue", "type": "number", "required": True,
         "description": "Total revenue"},
        {"in": "formData", "name": "expenses", "type": "number", "required": True,
         "description": "Total expenses. Profit is calculated automatically as revenue - expenses"},
    ],
    "responses": {
        302: {"description": "Redirect to financial list on success"},
        400: {"description": "Validation error — missing or non-numeric fields"},
    },
})
def create():
    period = request.form.get("period", "").strip()
    department = request.form.get("department", "").strip()
    revenue_str = request.form.get("revenue", "").strip()
    expenses_str = request.form.get("expenses", "").strip()

    if not period or not department or not revenue_str or not expenses_str:
        flash("All fields are required.", "danger")
        return render_template("financial/create.html")

    try:
        revenue = float(revenue_str)
        expenses = float(expenses_str)
    except ValueError:
        flash("Revenue and Expenses must be numeric.", "danger")
        return render_template("financial/create.html")

    db = SessionLocal()
    try:
        service = make_service(db)
        service.create(period=period, department=department, revenue=revenue, expenses=expenses)
        flash("Record created successfully.", "success")
        return redirect(url_for("financial.index"))
    finally:
        db.close()


@financial_bp.get("/<int:record_id>/edit")
@swag_from({
    "tags": ["Financial Data"],
    "summary": "Show edit form for a financial record",
    "parameters": [
        {"in": "path", "name": "record_id", "type": "integer", "required": True,
         "description": "ID of the financial record"},
    ],
    "responses": {
        200: {"description": "HTML form pre-filled with the record's current values"},
        302: {"description": "Redirect to list if record not found"},
    },
})
def edit_form(record_id: int):
    db = SessionLocal()
    try:
        service = make_service(db)
        record = service.get_by_id(record_id)
        if not record:
            flash("Record not found.", "danger")
            return redirect(url_for("financial.index"))
        return render_template("financial/edit.html", record=record)
    finally:
        db.close()


@financial_bp.post("/<int:record_id>/edit")
@swag_from({
    "tags": ["Financial Data"],
    "summary": "Update a financial record",
    "consumes": ["application/x-www-form-urlencoded"],
    "parameters": [
        {"in": "path", "name": "record_id", "type": "integer", "required": True,
         "description": "ID of the financial record to update"},
        {"in": "formData", "name": "period", "type": "string", "required": True,
         "description": "Reporting period"},
        {"in": "formData", "name": "department", "type": "string", "required": True,
         "description": "Department name"},
        {"in": "formData", "name": "revenue", "type": "number", "required": True,
         "description": "Total revenue"},
        {"in": "formData", "name": "expenses", "type": "number", "required": True,
         "description": "Total expenses. Profit is recalculated automatically"},
    ],
    "responses": {
        302: {"description": "Redirect to financial list after update"},
        400: {"description": "Validation error — missing or non-numeric fields"},
    },
})
def edit(record_id: int):
    period = request.form.get("period", "").strip()
    department = request.form.get("department", "").strip()
    revenue_str = request.form.get("revenue", "").strip()
    expenses_str = request.form.get("expenses", "").strip()

    if not period or not department or not revenue_str or not expenses_str:
        flash("All fields are required.", "danger")
        return redirect(url_for("financial.edit_form", record_id=record_id))

    try:
        revenue = float(revenue_str)
        expenses = float(expenses_str)
    except ValueError:
        flash("Revenue and Expenses must be numeric.", "danger")
        return redirect(url_for("financial.edit_form", record_id=record_id))

    db = SessionLocal()
    try:
        service = make_service(db)
        updated = service.update(record_id, period=period, department=department, revenue=revenue, expenses=expenses)
        if not updated:
            flash("Record not found.", "danger")
        else:
            flash("Record updated successfully.", "success")
        return redirect(url_for("financial.index"))
    finally:
        db.close()


@financial_bp.post("/<int:record_id>/delete")
@swag_from({
    "tags": ["Financial Data"],
    "summary": "Delete a financial record",
    "parameters": [
        {"in": "path", "name": "record_id", "type": "integer", "required": True,
         "description": "ID of the financial record to delete"},
    ],
    "responses": {
        302: {"description": "Redirect to financial list after deletion"},
    },
})
def delete(record_id: int):
    db = SessionLocal()
    try:
        service = make_service(db)
        deleted = service.delete(record_id)
        if deleted:
            flash("Record deleted.", "success")
        else:
            flash("Record not found.", "danger")
        return redirect(url_for("financial.index"))
    finally:
        db.close()
