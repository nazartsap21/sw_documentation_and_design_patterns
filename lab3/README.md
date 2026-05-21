# Lab 3 — MVC Web Application

MVC web application for Workday Financial Management built with Flask + Jinja2 + SQLAlchemy.

## Project structure

```
lab3/
├── app.py                              ← Entry point (Flask app)
├── config/
│   └── app.yml                         ← MySQL connection string
├── requirements.txt
└── app/
    ├── database.py                     ← SQLAlchemy engine + session
    ├── dal/
    │   ├── interfaces.py               ← Abstract interfaces (DAL)
    │   ├── models.py                   ← ORM models (FinancialData, Report, User, …)
    │   └── repositories.py             ← Concrete repository implementations
    ├── bll/
    │   └── services.py                 ← Business logic (CRUD via interfaces)
    ├── pl/
    │   ├── routes/
    │   │   ├── financial_routes.py     ← /financial  (list, create, edit, delete)
    │   │   ├── report_routes.py        ← /reports    (list, detail)
    │   │   └── user_routes.py          ← /users      (list, create, delete)
    │   └── templates/
    │       ├── base.html
    │       ├── financial/
    │       │   ├── index.html
    │       │   ├── create.html
    │       │   └── edit.html
    │       ├── reports/
    │       │   ├── index.html
    │       │   └── detail.html
    │       └── users/
    │           ├── index.html
    │           └── create.html
    └── static/
        └── style.css
```

## Setup

### 1. Configure database

Edit `config/app.yml`:

```yaml
db:
  uri: "mysql+pymysql://user:password@localhost:3306/lab3_db"
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`

## Pages

| URL | Description |
|-----|-------------|
| `GET /` | Redirects to Financial Data list |
| `GET /financial/` | List all financial records |
| `GET /financial/create` | Create record form |
| `POST /financial/create` | Save new record |
| `GET /financial/<id>/edit` | Edit record form |
| `POST /financial/<id>/edit` | Update record |
| `POST /financial/<id>/delete` | Delete record |
| `GET /reports/` | List all reports |
| `GET /reports/<id>` | Report detail |
| `GET /users/` | List all users |
| `GET /users/create` | Create user form |
| `POST /users/create` | Save new user |
| `POST /users/<id>/delete` | Delete user |
