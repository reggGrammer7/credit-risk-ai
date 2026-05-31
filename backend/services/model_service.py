import joblib
import shap
import numpy as np
import pandas as pd
from pathlib import Path
from functools import lru_cache

from schemas.schemas import ApplicantFeatures, PredictionResponse


FEATURE_NAMES = [
    "age", "income", "loan_amount", "loan_term",
    "credit_score", "employment_years", "debt_to_income",
    "num_credit_lines", "num_delinquencies", "home_ownership_enc"
]

FEATURE_LABELS = {
    "age": "Age",
    "income": "Annual income",
    "loan_amount": "Loan amount",
    "loan_term": "Loan term",
    "credit_score": "Credit score",
    "employment_years": "Employment years",
    "debt_to_income": "Debt-to-income ratio",
    "num_credit_lines": "Open credit lines",
    "num_delinquencies": "Past delinquencies",
    "home_ownership_enc": "Home ownership",
}


@lru_cache(maxsize=1)
def _load_bundle():
    model_path = Path("models/credit_model.pkl")
    if not model_path.exists():
        raise FileNotFoundError(
            "Model not found. Run: python generate_demo_model.py"
        )
    bundle = joblib.load(model_path)
    explainer = shap.TreeExplainer(bundle["model"])
    return bundle, explainer


def _encode_features(applicant: ApplicantFeatures) -> pd.DataFrame:
    bundle, _ = _load_bundle()
    le = bundle["label_encoder"]
    home_enc = int(le.transform([applicant.home_ownership])[0])

    row = {
        "age": applicant.age,
        "income": applicant.income,
        "loan_amount": applicant.loan_amount,
        "loan_term": applicant.loan_term,
        "credit_score": applicant.credit_score,
        "employment_years": applicant.employment_years,
        "debt_to_income": applicant.debt_to_income,
        "num_credit_lines": applicant.num_credit_lines,
        "num_delinquencies": applicant.num_delinquencies,
        "home_ownership_enc": home_enc,
    }
    return pd.DataFrame([row], columns=FEATURE_NAMES)


def _risk_band(prob: float) -> tuple[str, str]:
    if prob < 0.15:
        return "Low risk", "Approved"
    elif prob < 0.35:
        return "Medium risk", "Review"
    elif prob < 0.60:
        return "High risk", "Declined"
    else:
        return "Very high risk", "Declined"


def predict(applicant: ApplicantFeatures) -> PredictionResponse:
    bundle, explainer = _load_bundle()
    model = bundle["model"]

    X = _encode_features(applicant)
    prob = float(model.predict_proba(X)[0, 1])
    risk_band, decision = _risk_band(prob)

    shap_vals = explainer.shap_values(X)[0]

    shap_dict = {
        FEATURE_LABELS[name]: round(float(val), 4)
        for name, val in zip(FEATURE_NAMES, shap_vals)
    }

    sorted_factors = sorted(
        [{"feature": k, "shap_value": v, "direction": "increases risk" if v > 0 else "reduces risk"}
         for k, v in shap_dict.items()],
        key=lambda x: abs(x["shap_value"]),
        reverse=True,
    )

    return PredictionResponse(
        default_probability=round(prob, 4),
        risk_band=risk_band,
        decision=decision,
        shap_values=shap_dict,
        top_factors=sorted_factors[:5],
    )
