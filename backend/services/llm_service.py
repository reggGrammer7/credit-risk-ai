# import os
# import anthropic
# from schemas.schemas import ApplicantFeatures, PredictionResponse

# _client = None


# def _get_client() -> anthropic.Anthropic:
#     global _client
#     if _client is None:
#         api_key = os.getenv("OPENAI_API_KEY")
#         if not api_key:
#             raise EnvironmentError("ANTHROPIC_API_KEY not set in .env")
#         _client = anthropic.Anthropic(api_key=api_key)
#     return _client


# def _build_system_prompt() -> str:
#     return """You are a credit risk analyst assistant embedded in a loan decision platform.
# You help loan officers and applicants understand credit risk predictions made by a machine learning model.

# Your role:
# - Explain ML predictions in plain, professional language
# - Reference specific SHAP values and applicant data when relevant
# - Be honest about uncertainty — the model is a tool, not a final verdict
# - Suggest concrete, actionable improvements when asked
# - Never guarantee approval or denial outcomes

# Keep answers concise (2–4 sentences unless the question requires more).
# Use plain English — avoid jargon unless the user seems technical."""


# def _build_user_context(
#     applicant: ApplicantFeatures,
#     prediction: PredictionResponse,
#     question: str,
# ) -> str:
#     top = "\n".join(
#         f"  • {f['feature']}: SHAP={f['shap_value']:+.3f} ({f['direction']})"
#         for f in prediction.top_factors
#     )

#     return f"""
# APPLICANT PROFILE:
#   Age: {applicant.age}
#   Annual income: ${applicant.income:,.0f}
#   Loan requested: ${applicant.loan_amount:,.0f} over {applicant.loan_term} months
#   Credit score: {applicant.credit_score}
#   Employment: {applicant.employment_years:.1f} years
#   Debt-to-income: {applicant.debt_to_income:.1%}
#   Open credit lines: {applicant.num_credit_lines}
#   Past delinquencies: {applicant.num_delinquencies}
#   Home ownership: {applicant.home_ownership}

# MODEL PREDICTION:
#   Default probability: {prediction.default_probability:.1%}
#   Risk band: {prediction.risk_band}
#   Decision: {prediction.decision}

# TOP FACTORS (SHAP values — positive = increases default risk):
# {top}

# USER QUESTION: {question}
# """


# def chat(
#     applicant: ApplicantFeatures,
#     prediction: PredictionResponse,
#     question: str,
#     history: list[dict],
# ) -> str:
#     client = _get_client()

#     messages = []
#     for turn in history:
#         messages.append({"role": turn["role"], "content": turn["content"]})

#     context = _build_user_context(applicant, prediction, question)
#     messages.append({"role": "user", "content": context})

#     response = client.messages.create(
#         model="claude-haiku-4-5-20251001",
#         max_tokens=512,
#         system=_build_system_prompt(),
#         messages=messages,
#     )

#     return response.content[0].text






#### OpenAI VERSION
import os
from openai import OpenAI
from dotenv import load_dotenv
from schemas.schemas import ApplicantFeatures, PredictionResponse

load_dotenv()

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"DEBUG: OpenAI key found = {bool(api_key)}")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not set in .env")
        _client = OpenAI(api_key=api_key)
    return _client


def _build_system_prompt() -> str:
    return """You are a credit risk analyst assistant embedded in a loan decision platform.
You help loan officers and applicants understand credit risk predictions made by a machine learning model.

Your role:
- Explain ML predictions in plain, professional language
- Reference specific SHAP values and applicant data when relevant
- Be honest about uncertainty — the model is a tool, not a final verdict
- Suggest concrete, actionable improvements when asked
- Never guarantee approval or denial outcomes

Keep answers concise (2-4 sentences unless the question requires more).
Use plain English — avoid jargon unless the user seems technical."""


def _build_user_context(
    applicant: ApplicantFeatures,
    prediction: PredictionResponse,
    question: str,
) -> str:
    top = "\n".join(
        f"  • {f['feature']}: SHAP={f['shap_value']:+.3f} ({f['direction']})"
        for f in prediction.top_factors
    )
    return f"""
APPLICANT PROFILE:
  Age: {applicant.age}
  Annual income: ${applicant.income:,.0f}
  Loan requested: ${applicant.loan_amount:,.0f} over {applicant.loan_term} months
  Credit score: {applicant.credit_score}
  Employment: {applicant.employment_years:.1f} years
  Debt-to-income: {applicant.debt_to_income:.1%}
  Open credit lines: {applicant.num_credit_lines}
  Past delinquencies: {applicant.num_delinquencies}
  Home ownership: {applicant.home_ownership}

MODEL PREDICTION:
  Default probability: {prediction.default_probability:.1%}
  Risk band: {prediction.risk_band}
  Decision: {prediction.decision}

TOP FACTORS (SHAP values — positive = increases default risk):
{top}

USER QUESTION: {question}
"""


def chat(
    applicant: ApplicantFeatures,
    prediction: PredictionResponse,
    question: str,
    history: list[dict],
) -> str:
    client = _get_client()

    messages = [{"role": "system", "content": _build_system_prompt()}]

    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})

    context = _build_user_context(applicant, prediction, question)
    messages.append({"role": "user", "content": context})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=512,
        messages=messages,
    )

    return response.choices[0].message.content









































# import os
# import anthropic
# from dotenv import load_dotenv
# from schemas.schemas import ApplicantFeatures, PredictionResponse

# load_dotenv()

# _client = None


# def _get_client() -> anthropic.Anthropic:
#     global _client
#     if _client is None:
#         api_key = os.getenv("ANTHROPIC_API_KEY")
#         print(f"DEBUG: API key found = {bool(api_key)}, starts with = {api_key[:10] if api_key else 'NONE'}")
#         if not api_key:
#             raise EnvironmentError("ANTHROPIC_API_KEY not set in .env")
#         _client = anthropic.Anthropic(api_key=api_key)
#     return _client


# def _build_system_prompt() -> str:
#     return """You are a credit risk analyst assistant embedded in a loan decision platform.
# You help loan officers and applicants understand credit risk predictions made by a machine learning model.

# Your role:
# - Explain ML predictions in plain, professional language
# - Reference specific SHAP values and applicant data when relevant
# - Be honest about uncertainty — the model is a tool, not a final verdict
# - Suggest concrete, actionable improvements when asked
# - Never guarantee approval or denial outcomes

# Keep answers concise (2-4 sentences unless the question requires more).
# Use plain English — avoid jargon unless the user seems technical."""


# def _build_user_context(applicant, prediction, question) -> str:
#     top = "\n".join(
#         f"  • {f['feature']}: SHAP={f['shap_value']:+.3f} ({f['direction']})"
#         for f in prediction.top_factors
#     )
#     return f"""
# APPLICANT PROFILE:
#   Age: {applicant.age}
#   Annual income: ${applicant.income:,.0f}
#   Loan requested: ${applicant.loan_amount:,.0f} over {applicant.loan_term} months
#   Credit score: {applicant.credit_score}
#   Employment: {applicant.employment_years:.1f} years
#   Debt-to-income: {applicant.debt_to_income:.1%}
#   Open credit lines: {applicant.num_credit_lines}
#   Past delinquencies: {applicant.num_delinquencies}
#   Home ownership: {applicant.home_ownership}

# MODEL PREDICTION:
#   Default probability: {prediction.default_probability:.1%}
#   Risk band: {prediction.risk_band}
#   Decision: {prediction.decision}

# TOP FACTORS (SHAP values — positive = increases default risk):
# {top}

# USER QUESTION: {question}
# """


# def chat(applicant, prediction, question, history) -> str:
#     try:
#         client = _get_client()
#         messages = []
#         for turn in history:
#             messages.append({"role": turn["role"], "content": turn["content"]})
#         context = _build_user_context(applicant, prediction, question)
#         messages.append({"role": "user", "content": context})
#         response = client.messages.create(
#             model="claude-haiku-4-5-20251001",
#             max_tokens=512,
#             system=_build_system_prompt(),
#             messages=messages,
#         )
#         return response.content[0].text
#     except Exception as e:
#         print(f"LLM ERROR: {type(e).__name__}: {e}")
#         raise