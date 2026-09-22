"""
Stroke Risk Predictor - API
============================
Run with: uvicorn main:app --reload
Requires: data/processed/stroke_model.pkl, feature_scaler.pkl, shap_background.csv
"""

import joblib
import pandas as pd
import shap
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

FEATURE_ORDER = ['age_at_cutoff', 'has_hypertension', 'has_afib',
                  'has_diabetes', 'n_conditions_total', 'n_medications_total']

FEATURE_LABELS = {
    'age_at_cutoff': 'Age',
    'has_hypertension': 'Hypertension',
    'has_afib': 'Atrial fibrillation',
    'has_diabetes': 'Diabetes',
    'n_conditions_total': 'Number of conditions',
    'n_medications_total': 'Number of medications',
}

model = joblib.load("data/processed/stroke_model.pkl")
scaler = joblib.load("data/processed/feature_scaler.pkl")
background = pd.read_csv("data/processed/shap_background.csv")
masker = shap.maskers.Independent(background, max_samples=200)
explainer = shap.LinearExplainer(model, masker)

app = FastAPI(title="Stroke Risk Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    age: float
    hypertension: int
    afib: int
    diabetes: int
    n_conditions: int
    n_medications: int


class ShapEntry(BaseModel):
    feature: str
    value: float


class PredictResponse(BaseModel):
    risk_percentage: float
    risk_label: str
    shap_values: list[ShapEntry]


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    patient = pd.DataFrame([{
        'age_at_cutoff': request.age,
        'has_hypertension': request.hypertension,
        'has_afib': request.afib,
        'has_diabetes': request.diabetes,
        'n_conditions_total': request.n_conditions,
        'n_medications_total': request.n_medications,
    }])[FEATURE_ORDER]

    patient_scaled = pd.DataFrame(scaler.transform(patient), columns=FEATURE_ORDER)
    risk_pct = float(model.predict_proba(patient_scaled)[0, 1] * 100)

    if risk_pct >= 60:
        risk_label = "High"
    elif risk_pct >= 30:
        risk_label = "Moderate"
    else:
        risk_label = "Low"

    shap_values = explainer(patient_scaled)
    shap_df = pd.DataFrame({
        'feature': FEATURE_ORDER,
        'value': shap_values.values[0],
    }).sort_values('value', key=abs, ascending=False)

    return PredictResponse(
        risk_percentage=risk_pct,
        risk_label=risk_label,
        shap_values=[
            ShapEntry(feature=FEATURE_LABELS[row['feature']], value=float(row['value']))
            for _, row in shap_df.iterrows()
        ],
    )
