from flask import Flask, redirect, url_for
from flasgger import Swagger

from app.database import Base, engine
from app.dal import models  # noqa: F401 — ensures models are registered with Base
from app.pl.routes.financial_routes import financial_bp
from app.pl.routes.report_routes import report_bp
from app.pl.routes.user_routes import user_bp

Base.metadata.create_all(bind=engine)

app = Flask(__name__, template_folder="app/pl/templates", static_folder="app/static")
app.secret_key = "workday-lab3-secret"

app.config["SWAGGER"] = {
    "title": "Workday Financial Management",
    "description": "MVC web application for managing financial data, reports, and users.",
    "version": "1.0.0",
    "uiversion": 3,
}
Swagger(app)

app.register_blueprint(financial_bp)
app.register_blueprint(report_bp)
app.register_blueprint(user_bp)


@app.get("/")
def index():
    return redirect(url_for("financial.index"))


if __name__ == "__main__":
    app.run(debug=True)
