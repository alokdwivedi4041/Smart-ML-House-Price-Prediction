"""
Database layer for PredictIQ.

Uses PostgreSQL in production via SQLAlchemy. If no DATABASE_URL is set,
it falls back to a local SQLite file so the app can be run with zero
external setup while developing.

Set the environment variable DATABASE_URL to something like:
    postgresql://<user>:<password>@<host>:5432/predictiq
"""
import os
import json
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./predictiq.db")

# SQLite needs a special connect arg; Postgres does not.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    input_features = Column(Text)          # JSON-encoded dict of the input
    predicted_value = Column(Float)
    model_used = Column(String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "input_features": json.loads(self.input_features),
            "predicted_value": self.predicted_value,
            "model_used": self.model_used,
        }


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
