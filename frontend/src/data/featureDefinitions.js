export const FEATURE_DEFINITIONS = {
  age: {
    label: 'Age',
    text: 'Baseline demographic risk factor; vascular resilience naturally decreases over time.',
  },
  hypertension: {
    label: 'Hypertension',
    text: 'Chronic high blood pressure, which strains arterial walls and significantly increases stroke risk.',
  },
  afib: {
    label: 'Atrial fibrillation',
    text: 'An irregular cardiac rhythm that can cause blood pooling and clot formation in the heart.',
  },
  diabetes: {
    label: 'Diabetes',
    text: 'Chronic elevated blood sugar levels that can weaken vascular walls over time.',
  },
  n_conditions: {
    label: 'Prior conditions',
    text: 'Total count of diagnosed medical conditions, measuring overall systemic health burden.',
  },
  n_medications: {
    label: 'Prior medications',
    text: 'Total count of active prescription treatments, indicating disease management complexity.',
  },
}

// Maps the human-readable labels returned by the API's SHAP breakdown back to a
// definition key. The API never returns raw column names, so this is keyed on
// the same display strings FEATURE_LABELS produces server-side.
export const SHAP_LABEL_TO_KEY = {
  Age: 'age',
  Hypertension: 'hypertension',
  'Atrial fibrillation': 'afib',
  Diabetes: 'diabetes',
  'Number of conditions': 'n_conditions',
  'Number of medications': 'n_medications',
}
