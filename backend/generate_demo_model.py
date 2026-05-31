# """
# Run this once to create the demo model:
#     python generate_demo_model.py

# This trains a realistic credit risk model on synthetic data
# and saves it to models/credit_model.pkl
# """
# import os
# import numpy as np
# import pandas as pd
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import roc_auc_score
# import joblib

# os.makedirs("models", exist_ok=True)

# np.random.seed(42)
# n = 5000

# credit_score   = np.random.randint(300, 850, n)
# income         = np.random.lognormal(10.8, 0.6, n)
# loan_amount    = np.random.lognormal(10.2, 0.7, n)
# loan_term      = np.random.choice([12, 24, 36, 48, 60, 120, 180, 240, 360], n)
# age            = np.random.randint(18, 75, n)
# employment_yrs = np.abs(np.random.normal(5, 4, n))
# dti            = np.random.beta(2, 5, n)
# num_lines      = np.random.randint(0, 20, n)
# num_delinq     = np.random.poisson(0.5, n)
# home_ownership = np.random.choice(["RENT", "OWN", "MORTGAGE"], n, p=[0.4, 0.2, 0.4])

# le = LabelEncoder()
# home_enc = le.fit_transform(home_ownership)

# log_odds = (
#     -3.0
#     - 0.005 * (credit_score - 600)
#     + 0.3  * dti
#     - 0.2  * np.log1p(income / 10000)
#     + 0.15 * np.log1p(loan_amount / income)
#     + 0.1  * num_delinq
#     - 0.05 * employment_yrs
#     + 0.2  * (home_enc == le.transform(["RENT"])[0]).astype(float)
# )
# prob = 1 / (1 + np.exp(-log_odds))
# y = (np.random.uniform(size=n) < prob).astype(int)

# feature_names = [
#     "age", "income", "loan_amount", "loan_term",
#     "credit_score", "employment_years", "debt_to_income",
#     "num_credit_lines", "num_delinquencies", "home_ownership_enc"
# ]

# X = np.column_stack([
#     age, income, loan_amount, loan_term,
#     credit_score, employment_yrs, dti,
#     num_lines, num_delinq, home_enc
# ])
# df = pd.DataFrame(X, columns=feature_names)

# X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)

# model = GradientBoostingClassifier(n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42)
# model.fit(X_train, y_train)

# auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
# print(f"Model AUC: {auc:.4f}")

# bundle = {
#     "model": model,
#     "label_encoder": le,
#     "feature_names": feature_names,
# }
# joblib.dump(bundle, "models/credit_model.pkl")
# print("Saved → models/credit_model.pkl")


"""
Run once to generate all three models:
    python generate_demo_model.py
"""
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
import joblib

os.makedirs("models", exist_ok=True)

np.random.seed(42)
n = 5000

credit_score   = np.random.randint(300, 850, n)
income         = np.random.lognormal(10.8, 0.6, n)
loan_amount    = np.random.lognormal(10.2, 0.7, n)
loan_term      = np.random.choice([12, 24, 36, 48, 60, 120, 180, 240, 360], n)
age            = np.random.randint(18, 75, n)
employment_yrs = np.abs(np.random.normal(5, 4, n))
dti            = np.random.beta(2, 5, n)
num_lines      = np.random.randint(0, 20, n)
num_delinq     = np.random.poisson(0.5, n)
home_ownership = np.random.choice(["RENT", "OWN", "MORTGAGE"], n, p=[0.4, 0.2, 0.4])

le = LabelEncoder()
home_enc = le.fit_transform(home_ownership)

log_odds = (
    -3.0
    - 0.005 * (credit_score - 600)
    + 0.3   * dti
    - 0.2   * np.log1p(income / 10000)
    + 0.15  * np.log1p(loan_amount / income)
    + 0.1   * num_delinq
    - 0.05  * employment_yrs
    + 0.2   * (home_enc == le.transform(["RENT"])[0]).astype(float)
)
prob = 1 / (1 + np.exp(-log_odds))
y = (np.random.uniform(size=n) < prob).astype(int)

feature_names = [
    "age", "income", "loan_amount", "loan_term",
    "credit_score", "employment_years", "debt_to_income",
    "num_credit_lines", "num_delinquencies", "home_ownership_enc"
]

X = np.column_stack([
    age, income, loan_amount, loan_term,
    credit_score, employment_yrs, dti,
    num_lines, num_delinq, home_enc
])
df = pd.DataFrame(X, columns=feature_names)

X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

models = {
    "xgboost": XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.05,
                              use_label_encoder=False, eval_metric="logloss", random_state=42),
    "random_forest": RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42),
    "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
}

for name, model in models.items():
    if name == "logistic_regression":
        model.fit(X_train_scaled, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test_scaled)[:, 1])
    else:
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"{name} AUC: {auc:.4f}")

    bundle = {
        "model": model,
        "label_encoder": le,
        "feature_names": feature_names,
        "scaler": scaler if name == "logistic_regression" else None,
        "model_type": name,
    }
    joblib.dump(bundle, f"models/{name}.pkl")
    print(f"Saved → models/{name}.pkl")

print("\nAll three models saved successfully.")