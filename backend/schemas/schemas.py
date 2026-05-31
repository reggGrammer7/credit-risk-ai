from pydantic import BaseModel, Field
from typing import Optional


class ApplicantFeatures(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    income: float = Field(..., ge=0, description="Annual income in USD")
    loan_amount: float = Field(..., ge=0, description="Requested loan amount")
    loan_term: int = Field(..., ge=1, le=360, description="Loan term in months")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score")
    employment_years: float = Field(..., ge=0, description="Years at current employer")
    debt_to_income: float = Field(..., ge=0, le=1, description="Debt-to-income ratio (0–1)")
    num_credit_lines: int = Field(..., ge=0, description="Number of open credit lines")
    num_delinquencies: int = Field(..., ge=0, description="Number of past delinquencies")
    home_ownership: str = Field(..., description="RENT, OWN, or MORTGAGE")


class PredictionResponse(BaseModel):
    default_probability: float
    risk_band: str
    decision: str
    shap_values: dict[str, float]
    top_factors: list[dict]


class ChatRequest(BaseModel):
    applicant: ApplicantFeatures
    prediction: PredictionResponse
    question: str
    history: Optional[list[dict]] = []


class ChatResponse(BaseModel):
    answer: str
