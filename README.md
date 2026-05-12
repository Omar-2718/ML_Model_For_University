# Salary Prediction Project (Express + Python ML)

This project has two parts:

1. Python ML scripts in `ml/` (train + predict)
2. Node/Express API in `api/` that calls Python using subprocess

## Current Structure

```text
ML Uni/
  api/
    src/
      app.ts
      server.ts
      controllers/predict.controller.ts
      routes/predict.ts
      utils/subprocess.ts
      utils/validation.ts
  ml/
    data/Salary_Data[1].csv
    model_artifacts/
    train.py
    predict.py
    requirements.txt
  README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## 1) Setup Python Environment

From project root:

```powershell
cd "D:\Back_End\Projects\ML Uni"
python -m venv ml/.venv
```

Activate venv (PowerShell):

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& "D:\Back_End\Projects\ML Uni\ml\.venv\Scripts\Activate.ps1")
```

Install Python dependencies:

```powershell
pip install -r ml/requirements.txt
```

## 2) Train the Model

This reads data from `ml/data/Salary_Data[1].csv` and writes artifacts to `ml/model_artifacts/`.

```powershell
python ml/train.py
```

Artifacts created:

- `salary_model.joblib`
- `robust_scaler.joblib`
- `category_mappings.json`
- `feature_schema.json`

## 3) Test Python Prediction Directly

Get feature names:

```powershell
python ml/predict.py --features
```

Example prediction:

```powershell
python ml/predict.py 29 Male "Bachelor's" "Data Analyst" 4
```

Expected output shape:

```json
{"salary": 113456.7}
```

## 4) Setup and Run API

Install Node dependencies:

```powershell
cd api
npm install
```

If `npm run dev` fails because `tsx` is missing, install it once:

```powershell
npm install -D tsx
```

Run API:

```powershell
npm run dev
```

Server default port is `3000`.

Important:
- Run API from the `api/` folder.
- `subprocess.ts` resolves Python script with `../ml/predict.py` relative to the API working directory.

## 5) API Endpoints

### POST /predict

Request body:

```json
{
  "age": 29,
  "gender": "Male",
  "educationLevel": "Bachelor's",
  "jobTitle": "Data Analyst",
  "yearsOfExperience": 4
}
```

Response:

```json
{
  "salary": 113456.7
}
```

### GET /predict/features

Response:

```json
{
  "features": [
    "Age",
    "Gender",
    "Education Level",
    "Job Title",
    "Years of Experience"
  ]
}
```

## 6) Quick End-to-End Run (PowerShell)

From project root:

```powershell
# Python setup
python -m venv ml/.venv
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& "D:\Back_End\Projects\ML Uni\ml\.venv\Scripts\Activate.ps1")
pip install -r ml/requirements.txt

# Train model
python ml/train.py

# Run API
cd api
npm install
npm run dev
```

In another terminal:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:3000/predict" -ContentType "application/json" -Body '{"age":29,"gender":"Male","educationLevel":"Bachelor''s","jobTitle":"Data Analyst","yearsOfExperience":4}'
```

