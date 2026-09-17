"""
PredictIQ - FastAPI backend
============================
Serves the trained house-price prediction model via a REST API,
logs every prediction to PostgreSQL (or SQLite in local dev), and
exposes endpoints for the React analytics dashboard.

Run (after training the model once with train_model.py):
    uvicorn main:app --reload --port 8000
"""
import json
import os

import joblib
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import PredictionLog, get_db, init_db

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

app = FastAPI(title="PredictIQ API", version="1.0.0")

# Allow the React dev server (and any origin in simple local/demo setups)
# to call this API. Tighten this list before deploying publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
scaler = None
metrics = None


@app.on_event("startup")
def startup():
    global model, scaler, metrics
    init_db()

    model_path = os.path.join(MODELS_DIR, "model.pkl")
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")

    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        raise RuntimeError(
            "No trained model found. Run `python train_model.py` first "
            "to generate models/model.pkl and models/scaler.pkl."
        )

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    with open(metrics_path) as f:
        metrics = json.load(f)


class HouseFeatures(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float = Field(..., description="Median age of houses in the block")
    total_rooms: float = Field(..., description="Total rooms in the block")
    total_bedrooms: float = Field(..., description="Total bedrooms in the block")
    population: float = Field(..., description="Block population")
    households: float = Field(..., description="Number of households in the block")
    median_income: float = Field(..., description="Median income in block (10k USD)")
    ocean_proximity: str = Field(..., description="One of: <1H OCEAN, INLAND, ISLAND, NEAR BAY, NEAR OCEAN")


class PredictionResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    predicted_value_usd: float
    model_used: str


def build_input_row(features: HouseFeatures) -> pd.DataFrame:
    """Builds a single-row DataFrame that exactly matches the column
    layout (numeric + one-hot ocean_proximity) the model was trained on."""
    row = {f: getattr(features, f) for f in metrics["numeric_features"]}

    if features.ocean_proximity not in metrics["categories"]:
        raise HTTPException(
            status_code=400,
            detail=f"ocean_proximity must be one of {metrics['categories']}",
        )

    for cat in metrics["categories"]:
        row[f"ocean_{cat}"] = 1 if features.ocean_proximity == cat else 0

    df = pd.DataFrame([row])
    # Ensure exact column order the scaler/model expect
    return df[metrics["feature_columns"]]


@app.get("/")
def root():
    return {"status": "ok", "service": "PredictIQ API"}


@app.get("/api/metrics")
def get_metrics():
    if metrics is None:
        raise HTTPException(status_code=503, detail="Model metrics not loaded yet")
    return metrics


@app.post("/api/predict", response_model=PredictionResponse)
def predict(features: HouseFeatures, db: Session = Depends(get_db)):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    input_row = build_input_row(features)
    scaled = scaler.transform(input_row)
    prediction_usd = round(float(model.predict(scaled)[0]), 2)

    log = PredictionLog(
        input_features=json.dumps(features.dict()),
        predicted_value=prediction_usd,
        model_used=metrics["best_model"],
    )
    db.add(log)
    db.commit()

    return PredictionResponse(predicted_value_usd=prediction_usd, model_used=metrics["best_model"])


@app.get("/api/history")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    rows = (
        db.query(PredictionLog)
        .order_by(PredictionLog.id.desc())
        .limit(limit)
        .all()
    )
    return [r.to_dict() for r in reversed(rows)]
