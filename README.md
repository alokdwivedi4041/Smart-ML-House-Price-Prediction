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

## 6. (Optional) Hosting it live

- **Backend (FastAPI)**: Render, Railway, or Fly.io all support Python
  web services directly from a GitHub repo. Set the start command to
  `uvicorn main:app --host 0.0.0.0 --port $PORT`, add a `DATABASE_URL`
  environment variable pointing at a managed Postgres instance (Render
  and Railway both offer one-click Postgres add-ons), and make sure
  `train_model.py` runs once (e.g. as a build/release step) so
  `models/model.pkl` exists before the API starts.
- **Frontend (React)**: Vercel or Netlify — connect the GitHub repo,
  set the build command to `npm run build` and the output directory to
  `build`, and set `REACT_APP_API_URL` to your deployed backend URL in
  the project's environment variables.
- **Database**: Render/Railway/Supabase/Neon all offer free-tier managed
  PostgreSQL — copy the connection string they give you into
  `DATABASE_URL` on the backend service.

---

## 7. Extending it (matches the 8-week plan)

- Add hyperparameter tuning / cross-validation in `train_model.py`
  (`GridSearchCV` or `RandomizedSearchCV`) — Week 6.
- Add a `/api/retrain` endpoint to trigger retraining from the UI.
- Add user accounts/sessions to the `database.py` models if you want
  per-user prediction history instead of a global log.
- Swap in XGBoost by adding `xgboost` to `requirements.txt` and a
  third candidate model in `train_and_compare()`.
