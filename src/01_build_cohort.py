"""
Step 1: Cohort + Label Definition
==================================
Goal: produce a table with one row per patient:
    patient_id, label (1=stroke, 0=control), cutoff_date

cutoff_date is the "hand covering the page" boundary.
- For stroke patients: cutoff_date = date of their FIRST stroke diagnosis.
  We will only build features from events strictly BEFORE this date.
- For control patients (never had a stroke): cutoff_date = a randomly chosen
  date from their own encounter history. This stops the model from learning
  "more history = more likely to have had a stroke" as a cheap shortcut.

SNOMED-CT code for stroke in Synthea: 230690007
"""

import pandas as pd
import numpy as np

np.random.seed(42)  # reproducibility - same random cutoffs every run

STROKE_CODE = 230690007

# ---- Load only the columns we need (these files get big at full scale) ----
conditions = pd.read_csv(
    "data/raw/conditions.csv",
    usecols=["START", "PATIENT", "CODE", "DESCRIPTION"],
    parse_dates=["START"],
)
encounters = pd.read_csv(
    "data/raw/encounters.csv",
    usecols=["START", "PATIENT"],
    parse_dates=["START"],
)
patients = pd.read_csv(
    "data/raw/patients.csv",
    usecols=["Id", "BIRTHDATE", "DEATHDATE", "GENDER"],
    parse_dates=["BIRTHDATE", "DEATHDATE"],
)

print(f"Loaded {len(patients)} patients, {len(conditions)} condition records, "
      f"{len(encounters)} encounter records")

# ---- Data quality fix: Synthea is inconsistent about timezones across files.
# conditions.START is a plain date (tz-naive), encounters.START includes "Z"
# (tz-aware). Pandas refuses to compare tz-naive vs tz-aware timestamps, and
# tz_localize(None) errors if a column is ALREADY naive - so we check dtype
# per column rather than applying it blindly everywhere.
def make_tz_naive(series):
    series = pd.to_datetime(series)
    if getattr(series.dt, "tz", None) is not None:
        series = series.dt.tz_localize(None)
    return series

conditions["START"] = make_tz_naive(conditions["START"])
encounters["START"] = make_tz_naive(encounters["START"])
patients["BIRTHDATE"] = make_tz_naive(patients["BIRTHDATE"])
patients["DEATHDATE"] = make_tz_naive(patients["DEATHDATE"])

# ---- Step A: find every stroke diagnosis, keep the FIRST one per patient ----
stroke_dx = conditions[conditions["CODE"] == STROKE_CODE].copy()
first_stroke = (
    stroke_dx.sort_values("START")
    .groupby("PATIENT", as_index=False)
    .first()[["PATIENT", "START"]]
    .rename(columns={"PATIENT": "patient_id", "START": "cutoff_date"})
)
first_stroke["label"] = 1

print(f"\nFound {len(first_stroke)} patients with a stroke diagnosis (cases)")

# ---- Step B: everyone else is a candidate control ----
case_ids = set(first_stroke["patient_id"])
control_ids = patients[~patients["Id"].isin(case_ids)]["Id"]

print(f"{len(control_ids)} patients with no stroke diagnosis (control candidates)")

# For each control, pick ONE random encounter date from their own history
# to act as their cutoff. This is the "covering point" for healthy patients.
enc_by_patient = encounters.groupby("PATIENT")["START"]

control_rows = []
for pid in control_ids:
    if pid not in enc_by_patient.groups:
        continue  # patient has no encounters at all, can't build features anyway
    dates = enc_by_patient.get_group(pid)
    chosen = dates.sample(1, random_state=hash(pid) % (2**32)).iloc[0]
    control_rows.append({"patient_id": pid, "cutoff_date": chosen, "label": 0})

controls = pd.DataFrame(control_rows)

print(f"Assigned a random cutoff date to {len(controls)} controls "
      f"(dropped {len(control_ids) - len(controls)} with zero encounters)")

# ---- Step C: combine into one cohort table ----
cohort = pd.concat([first_stroke, controls], ignore_index=True)
cohort = cohort.merge(patients[["Id", "BIRTHDATE", "DEATHDATE", "GENDER"]],
                       left_on="patient_id", right_on="Id", how="left").drop(columns="Id")

# Sanity filter: cutoff_date must be AFTER birth (obviously) - cheap data quality check
cohort = cohort[cohort["cutoff_date"] > cohort["BIRTHDATE"]]

print(f"\nFinal cohort: {len(cohort)} patients "
      f"({cohort['label'].sum()} cases, {(cohort['label']==0).sum()} controls)")
print(f"Class balance: {cohort['label'].mean():.1%} positive")

cohort.to_csv("data/processed/cohort.csv", index=False)
print("\nSaved -> data/processed/cohort.csv")
print(cohort.head())
