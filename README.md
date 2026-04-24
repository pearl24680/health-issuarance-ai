# AI-Powered Health Insurance Assistant

Full-stack starter project for predicting insurance premiums, assessing health risk, recommending plan tiers, and answering simple premium-related questions.

## Stack

- Backend: FastAPI
- ML: scikit-learn Random Forest regressor and classifier
- Frontend: React + Tailwind CSS + Vite
- Data: Synthetic CSV generated locally

## Project Structure

```text
backend/
  app/
    main.py
    schemas.py
    services.py
  ml/
    data_gen.py
    train_model.py
data/
models/
frontend/
requirements.txt
```

## Backend Setup

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe backend\ml\data_gen.py
.venv\Scripts\python.exe backend\ml\train_model.py
.venv\Scripts\uvicorn.exe backend.app.main:app --reload
```

Optional root environment:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

If `GEMINI_API_KEY` is set, the `/chat` endpoint will use Gemini. If it is not set, chat falls back to the local rule-based assistant.

Backend URLs:

- `GET /health`
- `GET /meta`
- `POST /predict`
- `POST /chat`

## Frontend Setup

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Optional frontend environment:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Deploy To Render

This repo is set up for a single-service Docker deployment on Render using [render.yaml](c:\Users\vivek\Desktop\Pearl\render.yaml#L1) and [Dockerfile](c:\Users\vivek\Desktop\Pearl\Dockerfile#L1).

Steps:

1. Push this project to GitHub.
2. Sign in to Render and choose `New +` -> `Blueprint`.
3. Connect the GitHub repo.
4. Render will detect `render.yaml` and create the `pearl-health-assistant` web service.
5. Click deploy. During build, it will install Python dependencies, install frontend packages, build the React app, generate the synthetic dataset, and train the models inside the container.
6. When the deploy finishes, Render will give you a public URL you can share.

Notes:

- The app serves the React frontend and FastAPI backend from the same URL.
- The root URL loads the dashboard, while `/predict`, `/chat`, and `/health` remain available on the same host.
- Free-tier cold starts may make the first request slow.

## Sample Prediction Payload

```json
{
  "age": 34,
  "bmi": 25.8,
  "smoking_status": "Non-Smoker",
  "chronic_diseases": 1,
  "exercise_frequency": "3-4 times/week",
  "region": "West",
  "annual_income": 78000
}
```
