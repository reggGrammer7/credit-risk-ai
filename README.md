# CreditAI — Full-Stack Risk Assessment Platform

A production-style AI web app combining:
- **React + Vite** frontend with Tailwind CSS
- **FastAPI** backend with Pydantic validation
- **Gradient Boosting** ML model with SHAP explainability
- **Claude (Anthropic API)** for natural language explanations

---

## Project structure

```
credit-risk-ai/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── generate_demo_model.py   # Run once to create the ML model
│   ├── requirements.txt
│   ├── .env.example             # Copy to .env and add your API key
│   ├── routers/
│   │   ├── predict.py
│   │   ├── chat.py
│   │   └── health.py
│   ├── services/
│   │   ├── model_service.py     # ML model + SHAP
│   │   └── llm_service.py       # Claude API calls
│   ├── schemas/
│   │   └── schemas.py           # Pydantic models
│   └── models/                  # .pkl file lives here (generated)
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── services/
        │   └── api.js           # All API calls
        └── components/
            ├── InputForm.jsx    # Applicant input fields
            ├── ResultsCard.jsx  # Score + risk band + gauge
            ├── ShapChart.jsx    # SHAP bar chart (Recharts)
            └── ChatPanel.jsx    # LLM chat interface
```

---

## Setup — step by step

### 1. Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate the demo ML model (only need to run once)
python generate_demo_model.py

# Create your .env file
cp .env.example .env
# → Open .env and paste your Anthropic API key
#   Get one at: https://console.anthropic.com/

# Start the API server
uvicorn main:app --reload --port 8000
```

API docs are auto-generated at: http://localhost:8000/docs

---

### 2. Frontend

Open a **new terminal** (keep the backend running):

```bash
cd frontend

npm install

npm run dev
```

Open: http://localhost:5173

---

## Getting an Anthropic API key

1. Go to https://console.anthropic.com/
2. Sign up / log in
3. Go to API Keys → Create Key
4. Paste it into `backend/.env` as `ANTHROPIC_API_KEY=sk-ant-...`

---

## How it works

1. User fills in applicant details in the React form
2. React calls `POST /predict` on the FastAPI backend
3. FastAPI loads the sklearn model, runs prediction, computes SHAP values
4. Results (probability, risk band, SHAP) are returned and visualised
5. User asks a question in the chat panel
6. React calls `POST /chat` with the applicant data + prediction + question
7. FastAPI builds a structured prompt and calls the Claude API
8. Claude explains the prediction in plain English

---

## Using your own model

Replace `models/credit_model.pkl` with your own trained model.

In `services/model_service.py`, update:
- `FEATURE_NAMES` — your feature column names
- `_encode_features()` — how you preprocess `ApplicantFeatures` into a dataframe
- `_risk_band()` — your threshold logic

The rest of the app picks it up automatically.
