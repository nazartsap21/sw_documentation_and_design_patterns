from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import yaml, os

with open(os.path.join(os.path.dirname(__file__), "../config/app.yml"), "r") as f:
    config = yaml.safe_load(f)
    DATABASE_URL = config["db"]["uri"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
