# 🏠 PredictIQ

### Smart ML-Powered House Price Prediction Web App

An end-to-end machine learning application that trains, compares, and serves
regression models to predict California housing prices — with a full REST
API, a PostgreSQL-backed prediction history, and a live analytics dashboard.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) •
[Tech Stack](#-tech-stack) •
[Getting Started](#-getting-started) •
[API Reference](#-api-reference) •
[Deployment](#-deployment) •
[Roadmap](#-roadmap)

</div>

---

## 📖 Overview

**PredictIQ** demonstrates a complete, production-shaped ML pipeline: real
data → cleaning & EDA → model training & comparison → a served REST API →
an interactive frontend. It predicts **median house value** using the
classic California Housing Prices dataset (~20,640 real records), letting
users enter details about a home/block and get an instant, model-backed
price estimate — with every prediction logged for trend analysis.

## ✨ Features

- 📊 **Real dataset, real cleaning** — missing-value imputation, outlier
  clipping, and categorical encoding on ~20,640 rows of housing data
- 🤖 **Model comparison** — trains and evaluates Linear Regression, Random
  Forest, and Gradient Boosting; automatically selects the best performer
  by R²
- ⚡ **REST API** — FastAPI backend with auto-generated OpenAPI/Swagger docs
- 🗄️ **Persistent logging** — every prediction is stored in PostgreSQL
  (falls back to SQLite automatically for zero-config local development)
- 📈 **Live analytics dashboard** — prediction trend and model accuracy
  charts, built with Recharts
- 🎯 **End-to-end pipeline** — data → model → API → UI, fully wired and
  tested

## 🛠 Tech Stack

| Layer          | Technology                                              |
|----------------|----------------------------------------------------------|
| Frontend       | React 18, Recharts, Axios                                |
| Backend        | FastAPI, Uvicorn, Pydantic                                |
| Machine Learning | scikit-learn, pandas, numpy, matplotlib                |
| Database       | PostgreSQL (SQLAlchemy ORM), SQLite fallback for local dev |
| Tooling        | joblib (model persistence), python-dotenv                 |

## 🗂 Project Structure

```
predictiq/
├── backend/
│   ├── main.py             # FastAPI app — /api/predict, /api/history, /api/metrics
│   ├── train_model.py      # EDA, cleaning, model training & comparison
│   ├── database.py         # SQLAlchemy models (PostgreSQL / SQLite)
│   ├── requirements.txt
│   └── models/              # generated: model.pkl, scaler.pkl, metrics.json
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── api.js
│   │   └── components/
│   │       ├── PredictionForm.js
│   │       ├── PredictionResult.js
│   │       └── Dashboard.js
│   └── package.json
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12
- Node.js 18+
- PostgreSQL 14+ *(optional — SQLite is used automatically if unset)*

### 1. Clone the repository

```bash
git clone https://github.com/alokdwivedi4041/Smart-ML-House-Price-Prediction.git
cd Smart-ML-House-Price-Prediction
```

### 2. Backend setup

```bash
cd backend
python -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**(Optional)** Use PostgreSQL instead of the SQLite default:

```bash
export DATABASE_URL="postgresql://<user>:<password>@localhost:5432/predictiq"   # macOS/Linux
$env:DATABASE_URL="postgresql://<user>:<password>@localhost:5432/predictiq"     # Windows
```

Train the model, then start the API:

```bash
python train_model.py
uvicorn main:app --reload --port 8000
```

The API is now live at `http://localhost:8000` — interactive docs at
`http://localhost:8000/docs`.

### 3. Frontend setup

In a new terminal:

```bash
cd frontend
npm install
npm start
```

The app opens at `http://localhost:3000` and talks to the API automatically.
To point it at a different backend URL, create `frontend/.env`:

```
REACT_APP_API_URL=https://your-deployed-backend-url
```

## 📡 API Reference

| Method | Endpoint         | Description                                  |
|--------|------------------|-----------------------------------------------|
| `GET`  | `/`              | Health check                                  |
| `POST` | `/api/predict`   | Submit house features, get a price prediction |
| `GET`  | `/api/history`   | Returns recent logged predictions             |
| `GET`  | `/api/metrics`   | Returns model comparison metrics (MAE/RMSE/R²)|

<details>
<summary><strong>Example request — <code>POST /api/predict</code></strong></summary>

```json
{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3,
  "ocean_proximity": "NEAR BAY"
}
```

```json
{
  "predicted_value_usd": 452600.00,
  "model_used": "RandomForest"
}
```
</details>

## 🧠 Model Performance

`train_model.py` trains and compares three algorithms; the best model (by
R² on a held-out test set) is automatically saved and served. Typical
results on this dataset:

| Model              | MAE (approx.) | RMSE (approx.) | R²     |
|---------------------|---------------|-----------------|--------|
| Linear Regression    | ~50k          | ~70k            | ~0.65  |
| Random Forest         | ~32k          | ~48k            | ~0.81  |
| Gradient Boosting      | ~35k          | ~51k            | ~0.79  |

*(Exact numbers vary slightly by run — see `backend/models/metrics.json`
after training.)*

## ☁️ Deployment

| Component  | Suggested platform                          | Notes |
|------------|----------------------------------------------|-------|
| Backend    | [Render](https://render.com) / [Railway](https://railway.app) | Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`. Run `train_model.py` as a build step so `model.pkl` exists before boot. |
| Database   | Render / Railway / [Neon](https://neon.tech) | Copy the managed Postgres connection string into `DATABASE_URL`. |
| Frontend   | [Vercel](https://vercel.com) / [Netlify](https://netlify.com) | Build command `npm run build`, output dir `build`. Set `REACT_APP_API_URL` to the deployed backend URL. |

## 🗺 Roadmap

- [ ] Hyperparameter tuning via `GridSearchCV` / `RandomizedSearchCV`
- [ ] `/api/retrain` endpoint to trigger retraining from the UI
- [ ] User accounts for per-user prediction history
- [ ] XGBoost as a fourth candidate model
- [ ] Docker Compose setup for one-command local spin-up

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙋 Author

**Alok Dwivedi**
[GitHub](https://github.com/alokdwivedi4041)

---
