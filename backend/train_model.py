"""
PredictIQ - Model Training Script
==================================
Loads the classic California Housing Prices dataset (real Kaggle/StatLib
data, ~20,640 rows), runs a quick EDA, cleans missing values, one-hot
encodes the categorical feature, trains and compares three algorithms,
and saves the best-performing model + scaler + metrics + column layout
to the `models/` folder for the API to serve.

Run:
    python train_model.py
"""
import json
import os

import joblib
import matplotlib
matplotlib.use("Agg")  # headless plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

DATA_URL = (
    "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
    "datasets/housing/housing.csv"
)

NUMERIC_FEATURES = [
    "longitude", "latitude", "housing_median_age", "total_rooms",
    "total_bedrooms", "population", "households", "median_income",
]
CATEGORICAL_FEATURE = "ocean_proximity"
CATEGORIES = ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
TARGET_NAME = "median_house_value"


def load_and_clean_data():
    print(f"Loading dataset from {DATA_URL} ...")
    df = pd.read_csv(DATA_URL)
    print(f"Raw shape: {df.shape}")
    print("Missing values per column:\n", df.isnull().sum())

    df = df.drop_duplicates()

    # total_bedrooms has ~200 missing values in the real dataset -> impute
    # with the median, a standard, defensible cleaning step.
    df["total_bedrooms"] = df["total_bedrooms"].fillna(df["total_bedrooms"].median())

    # Clip 1st/99th percentile outliers on the target so a few extreme
    # values don't skew training.
    lower, upper = df[TARGET_NAME].quantile([0.01, 0.99])
    df[TARGET_NAME] = df[TARGET_NAME].clip(lower, upper)

    return df


def run_eda(df: pd.DataFrame):
    print("\n--- EDA summary ---")
    print(df.describe())

    corr = df[NUMERIC_FEATURES + [TARGET_NAME]].corr()
    plt.figure(figsize=(8, 6))
    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Feature correlation matrix")
    plt.tight_layout()
    eda_path = os.path.join(MODELS_DIR, "eda_correlation.png")
    plt.savefig(eda_path)
    plt.close()
    print(f"Saved correlation heatmap to {eda_path}")


def build_feature_matrix(df: pd.DataFrame):
    """One-hot encode ocean_proximity with a fixed, known category list so
    the API can always build the exact same columns at inference time."""
    cat = pd.Categorical(df[CATEGORICAL_FEATURE], categories=CATEGORIES)
    dummies = pd.get_dummies(cat, prefix="ocean")
    X = pd.concat([df[NUMERIC_FEATURES].reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
    return X


def train_and_compare(df: pd.DataFrame):
    X = build_feature_matrix(df)
    y = df[TARGET_NAME].reset_index(drop=True)
    feature_columns = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    candidates = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(
            n_estimators=200, max_depth=14, random_state=42, n_jobs=-1
        ),
        "GradientBoosting": GradientBoostingRegressor(
            n_estimators=200, max_depth=3, learning_rate=0.1, random_state=42
        ),
    }

    results = {}
    best_name, best_model, best_r2 = None, None, -np.inf

    for name, model in candidates.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)

        mae = mean_absolute_error(y_test, preds)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        r2 = r2_score(y_test, preds)

        results[name] = {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "R2": round(r2, 4)}
        print(f"{name}: MAE={mae:.2f}  RMSE={rmse:.2f}  R2={r2:.4f}")

        if r2 > best_r2:
            best_name, best_model, best_r2 = name, model, r2

    print(f"\nBest model: {best_name} (R2={best_r2:.4f})")
    return best_name, best_model, scaler, results, feature_columns


def main():
    df = load_and_clean_data()
    run_eda(df)
    best_name, best_model, scaler, results, feature_columns = train_and_compare(df)

    joblib.dump(best_model, os.path.join(MODELS_DIR, "model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))

    metrics_payload = {
        "best_model": best_name,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_feature": CATEGORICAL_FEATURE,
        "categories": CATEGORIES,
        "feature_columns": feature_columns,
        "target": TARGET_NAME,
        "comparison": results,
    }
    with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"\nSaved model.pkl, scaler.pkl and metrics.json to {MODELS_DIR}")


if __name__ == "__main__":
    main()
