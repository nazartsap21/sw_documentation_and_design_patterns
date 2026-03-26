# Lab 2

## Project structure

```
lab2/
├── app.py                            ← Entry point (starting Flask)
├── config/
│   └── app.yml                       ← URL for connecting to MySQL
├── generate_csv.py                   ← CSV Generator (run from command line)
├── financial_data.csv                ← Data file (generated)
├── requirements.txt
└── app/
    ├── database.py                   ← SQLAlchemy connection
    ├── dal/
    │   ├── interfaces.py             ← Interfaces (ABC) — DAL
    │   ├── models.py                 ← ORM models (class diagram)
    │   └── repositories.py           ← Repository implementations + CSV reading
    ├── bll/
    │   └── services.py               ← Business logic (IoC / DI)
    └── pl/
        ├── interfaces.py             ← Presentation layer interfaces
        └── routes.py                 ← Flask Blueprint (routes)
```

## 1. Configure database connection

Open `config/app.yml` and set your MySQL connection string:

```yaml
db:
  uri: "mysql+pymysql://user:password@localhost:3306/lab2_db"
```

Format: `mysql+pymysql://<user>:<password>@<host>:<port>/<database>`

## 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Generate CSV data

```bash
python generate_csv.py
```

With parameters:
```bash
python generate_csv.py --rows 1500 --output financial_data.csv
```

## 5. Run the application

```bash
python app.py
```

The server starts on `http://127.0.0.1:5000`

## 6. Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | List all endpoints |
| POST | `/api/load-data` | Load CSV data into the database |
| GET | `/api/financial-data` | All financial records |
| GET | `/api/reports` | All reports |
| GET | `/api/reports/<id>` | Report by ID |
| GET | `/api/users` | All users |
| POST | `/api/users` | Create a user |
