# PredictIQ — Smart ML Prediction Web App

An end-to-end ML web app that predicts California median house prices,
using the real ~20,640-row California Housing Prices dataset (the
classic StatLib/Kaggle dataset, loaded straight from a public CSV).
Users fill in a form, a Python API runs the input through a trained
scikit-learn model, and a React dashboard shows prediction history and
model accuracy.

**Stack**
- Frontend: React + Recharts
- Backend: FastAPI (Python)
- ML: scikit-learn, pandas, numpy (Linear Regression, Random Forest, Gradient Boosting)
- Database: PostgreSQL (via SQLAlchemy — falls back to SQLite automatically if `DATABASE_URL` isn't set, so it also runs with zero setup)

```
predictiq/
├── backend/
│   ├── main.py           # FastAPI app: /api/predict, /api/history, /api/metrics
│   ├── train_model.py    # EDA + trains & compares 3 models, saves the best one
│   ├── database.py       # SQLAlchemy models (PostgreSQL / SQLite)
│   ├── requirements.txt
│   └── models/           # generated: model.pkl, scaler.pkl, metrics.json
└── frontend/
    ├── src/
    │   ├── App.js
    │   ├── api.js
    │   └── components/   # PredictionForm, PredictionResult, Dashboard
    └── package.json
```

---

## 1. Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- (Optional, for production-grade logging) PostgreSQL 14+

---

## 2. Backend setup

```bash
cd predictiq/backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2a. (Optional) Point at PostgreSQL

By default the app uses a local SQLite file (`predictiq.db`) so you can
run everything immediately. To use PostgreSQL instead:

```bash
# Create a database first, e.g.:
#   createdb predictiq

export DATABASE_URL="postgresql://<user>:<password>@localhost:5432/predictiq"
```

(On Windows PowerShell: `$env:DATABASE_URL="postgresql://user:pass@localhost:5432/predictiq"`)

### 2b. Train the model

This loads the dataset, runs EDA, trains & compares 3 algorithms, and
saves the best model to `backend/models/`:

```bash
python train_model.py
```

You should see MAE/RMSE/R² printed for each model and a final
"Best model: ..." line.

### 2c. Run the API

```bash
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive Swagger docs.

---

## 3. Frontend setup

In a **new terminal**:

```bash
cd predictiq/frontend
npm install
npm start
```

This opens `http://localhost:3000`. It talks to the API at
`http://localhost:8000` by default (see `src/api.js`). To point it at a
different backend URL (e.g. after deploying), create `frontend/.env`:

```
REACT_APP_API_URL=https://your-deployed-backend-url
```

---

## 4. Using the app

1. Fill in the house details form (median income, rooms, location, etc.)
2. Click **Predict Price** — the API scales your input, runs it through
   the trained model, and returns a predicted value.
3. Every prediction is logged to the database and immediately shows up
   in the **Prediction Trend** chart below.
4. The **Model Accuracy Comparison** chart shows R² for all three
   algorithms trained during `train_model.py`.

---

## 5. Deploying to GitHub

From the `predictiq/` root folder:

```bash
git init
git add .
git commit -m "Initial commit: PredictIQ ML prediction app"

# Create a new empty repo on GitHub first (via github.com/new), then:
git branch -M main
git remote add origin https://github.com/<your-username>/predictiq.git
git push -u origin main
```

> Note: `models/*.pkl`, `metrics.json`, and `predictiq.db` are in
> `.gitignore` since they're generated artifacts — anyone cloning the
> repo just runs `python train_model.py` once to regenerate them.

### Pushing changes later

```bash
git add .
git commit -m "Describe your change"
git push
```

---


