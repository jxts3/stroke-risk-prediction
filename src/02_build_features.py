"""
Step 2: Feature Engineering (YOUR TURN)
=========================================
Goal: turn each patient's PRE-CUTOFF history into one row of numeric features.

Input you already have:
- data/processed/cohort.csv  -> patient_id, cutoff_date, label, BIRTHDATE, GENDER
- data/raw/conditions.csv    -> PATIENT, START, CODE, DESCRIPTION
- data/raw/medications.csv   -> PATIENT, START, CODE, DESCRIPTION
- data/raw/observations.csv  -> PATIENT, DATE, CODE, DESCRIPTION, VALUE, UNITS

KEY CODES (SNOMED unless noted):
    Hypertension       = 59621000
    Atrial Fibrillation = 49436004
    Diabetes (type 2)  = 44054006

RULE: for every feature, only count events where event_date < cutoff_date
for that patient. This is the leakage rule from before - do not skip this.

Fill in the function below. Suggested features to start with (add more once
this works):
    age_at_cutoff          -> (cutoff_date - BIRTHDATE) in years
    has_hypertension        -> 1 if hypertension condition appears before cutoff, else 0
    has_afib                -> 1 if afib condition appears before cutoff, else 0
    has_diabetes             -> 1 if diabetes condition appears before cutoff, else 0
    n_conditions_total       -> count of all condition records before cutoff
    n_medications_total      -> count of all medication records before cutoff
    n_encounters_last_2yrs   -> count of encounters in the 2 years before cutoff
                                 (hint: you'll need encounters.csv too - load it)

HINTS:
- Merge cohort with conditions on PATIENT, this gives every patient's
  cutoff_date sitting next to every one of their condition rows.
- Filter to rows where START < cutoff_date BEFORE you do any counting/grouping.
- groupby('patient_id') + .agg(...) or .apply(...) is your friend for turning
  many rows per patient into one row per patient.
- Start small: get age + has_hypertension working and printing correctly
  before adding the rest. Print intermediate dataframes to sanity check.
"""

import pandas as pd

HYPERTENSION_CODE = 59621000
AFIB_CODE = 49436004
DIABETES_CODE = 44054006

cohort = pd.read_csv("data/processed/cohort.csv", parse_dates=["cutoff_date", "BIRTHDATE"])
conditions = pd.read_csv("data/raw/conditions.csv", parse_dates=["START"])
medications = pd.read_csv("data/raw/medications.csv", parse_dates=["START"])
# encounters.csv has a timezone in its dates (remember the bug from step 1!)
# you'll need to strip tz info the same way we did before if you load it here.


def build_features(cohort, conditions, medications):
    """
    Returns a dataframe with one row per patient_id and the engineered
    feature columns described above, ready to merge with cohort['label'].
    """
    # TODO: your code here
    pass


if __name__ == "__main__":
    features = build_features(cohort, conditions, medications)
    print(features.head())
    print(f"\nShape: {features.shape}")
    # once it looks right, save it:
    # features.to_csv("data/processed/features.csv", index=False)
