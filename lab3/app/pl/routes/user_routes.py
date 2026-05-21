from flasgger import swag_from
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database import SessionLocal
from app.dal.repositories import UserRepository
from app.bll.services import UserService

user_bp = Blueprint("users", __name__, url_prefix="/users")


def make_service(db) -> UserService:
    return UserService(repo=UserRepository(db))


@user_bp.get("/")
@swag_from({
    "tags": ["Users"],
    "summary": "List all users",
    "responses": {
        200: {"description": "HTML page with a table of all users"},
    },
})
def index():
    db = SessionLocal()
    try:
        service = make_service(db)
        users = service.get_all()
        return render_template("users/index.html", users=users)
    finally:
        db.close()


@user_bp.get("/create")
@swag_from({
    "tags": ["Users"],
    "summary": "Show create user form",
    "responses": {
        200: {"description": "HTML form to create a new user"},
    },
})
def create_form():
    return render_template("users/create.html")


@user_bp.post("/create")
@swag_from({
    "tags": ["Users"],
    "summary": "Create a new user",
    "consumes": ["application/x-www-form-urlencoded"],
    "parameters": [
        {"in": "formData", "name": "name", "type": "string", "required": True,
         "description": "Full name of the user"},
        {"in": "formData", "name": "role", "type": "string", "required": True,
         "enum": ["analyst", "manager"],
         "description": "User role — must be 'analyst' or 'manager'"},
    ],
    "responses": {
        302: {"description": "Redirect to users list on success"},
        400: {"description": "Validation error — missing fields or unknown role"},
    },
})
def create():
    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip()

    if not name or not role:
        flash("Name and role are required.", "danger")
        return render_template("users/create.html")

    db = SessionLocal()
    try:
        service = make_service(db)
        service.create(name=name, role=role)
        flash("User created successfully.", "success")
        return redirect(url_for("users.index"))
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("users/create.html")
    finally:
        db.close()


@user_bp.post("/<user_id>/delete")
@swag_from({
    "tags": ["Users"],
    "summary": "Delete a user",
    "parameters": [
        {"in": "path", "name": "user_id", "type": "string", "required": True,
         "description": "UUID of the user to delete"},
    ],
    "responses": {
        302: {"description": "Redirect to users list after deletion"},
    },
})
def delete(user_id: str):
    db = SessionLocal()
    try:
        service = make_service(db)
        deleted = service.delete(user_id)
        if deleted:
            flash("User deleted.", "success")
        else:
            flash("User not found.", "danger")
        return redirect(url_for("users.index"))
    finally:
        db.close()
