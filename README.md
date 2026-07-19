# Stroke Risk Predictor



An interpretable machine learning pipeline for predicting stroke risk from synthetic electronic health record (EHR) data, with a leakage-free cohort design, model comparison, clinical benchmark validation, and an interactive Streamlit application.



**Live app:** *(add your Streamlit Cloud link here once deployed, or note "run locally" below)*

**Live Tableau dashboard:** https://public.tableau.com/app/profile/oghenemaro.igbide/viz/StrokeRiskCohortAnalysis/Dashboard1



## Overview



This project builds a stroke risk model from raw synthetic patient records, generated using Synthea (https://synthea.mitre.org), an open-source synthetic patient generator. Rather than starting from a pre-built ML-ready dataset, the full pipeline - cohort definition, feature engineering, model training, interpretability, and clinical validation - was built from raw EHR-style data (conditions, medications, encounters).



## Key methodology



- Leakage-free labeling: each patient is assigned a cutoff date - the date of first stroke diagnosis for cases, or a randomly selected visit date for controls - and only events occurring before that date are used as features. This prevents the model from seeing post-outcome information (e.g. stroke recovery medications).

- Feature engineering: age at cutoff, presence of hypertension/atrial fibrillation/diabetes prior to cutoff, and total condition/medication counts, all computed directly from raw SNOMED/RxNorm-coded records.

- Model comparison: logistic regression vs. XGBoost, evaluated via 5-fold stratified cross-validation (ROC-AUC and PR-AUC) due to severe class imbalance (\~0.7% positive rate at full scale). Logistic regression outperformed XGBoost, likely due to the limited number of positive cases relative to XGBoost's capacity to overfit.

- Interpretability: SHAP used to explain individual predictions, with features standardized first so SHAP magnitudes are comparable across features of different scales.

- Clinical validation: model performance compared against a simplified version of CHA2DS2-VASc, a real clinical stroke risk score, as a sanity-check benchmark.

- Population-level analysis: a Tableau dashboard covering age distribution, comorbidity prevalence by outcome group, model comparison, and a condition/medication scatter - complementing the patient-level Streamlit tool with cohort-wide patterns.



## Results



| Model | ROC-AUC | PR-AUC |

|---|---|---|

| Logistic Regression | 0.858 +/- 0.026 | 0.093 +/- 0.073 |

| XGBoost | 0.819 +/- 0.027 | 0.037 +/- 0.013 |

| Simplified CHA2DS2-VASc (benchmark) | 0.754 | 0.024 |



(Cross-validated on \~5,700 synthetic patients, \~40 stroke cases)



## Running locally



pip install streamlit pandas scikit-learn xgboost shap plotly joblib

streamlit run app.py



Note: raw Synthea-generated data is excluded from this repo (see .gitignore). To regenerate, use Synthea (https://github.com/synthetichealth/synthea) with exporter.csv.export = true in config/synthea.properties, then run the notebook top to bottom to rebuild the cohort, features, and trained model artifacts.



## Limitations



- Built on synthetic data - not validated on real patient records, and not a clinical decision tool.

- Small absolute number of positive cases (\~40) even at full generation scale, meaning PR-AUC estimates carry meaningful variance across cross-validation folds.

- Feature set is limited to condition/medication history; does not include lab values, imaging, or family history, which would likely improve performance.

