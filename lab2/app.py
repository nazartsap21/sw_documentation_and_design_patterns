from flask import Flask

from app.database import Base, engine
from app.dal import models
from app.pl.routes import api

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")


@app.get("/")
def index():
    return {
        "message": "Server is running",
        "endpoints": [
            "POST /api/load-data         — load CSV into DB",
            "GET  /api/financial-data    — all financial records",
            "GET  /api/reports           — all reports",
            "GET  /api/reports/<id>      — report by ID",
            "GET  /api/users             — all users",
            "POST /api/users             — create user",
        ],
    }


if __name__ == "__main__":
    app.run(debug=True)
