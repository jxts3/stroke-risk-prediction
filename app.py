"""
Stroke Risk Predictor - Clinical Calm UI
===========================================
Run with: streamlit run app.py
Requires: data/processed/stroke_model.pkl, feature_scaler.pkl,
          feature_stats.csv, shap_background.csv
"""

import streamlit as st
import pandas as pd
import joblib
import shap
import plotly.graph_objects as go

st.set_page_config(page_title="Stroke Risk Predictor", page_icon=":material/monitor_heart:", layout="centered")

# ============================================================
# GLOBAL STYLE: Clinical Calm dark theme (charcoal background,
# teal/blue accents, rounded cards) + Plus Jakarta Sans font +
# Material icons + entrance animations
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..500,0,0&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background-color: #0F1517;
    }
    h1, h2, h3 { color: #E8EDF0 !important; }
    p, li, label, .stMarkdown { color: #B4BFC7 !important; }

    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined';
        font-weight: normal;
        font-style: normal;
        vertical-align: middle;
        line-height: 1;
    }

    /* Native bordered containers become soft rounded cards, distinguishable from the page */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        background-color: #172123 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        margin-bottom: 20px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] {
        padding: 14px 10px;
        gap: 0.9rem;
    }

    /* Subheaders read as calm section titles, not shouty headings */
    h3 {
        font-size: 19px !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px;
    }
    h3 .material-symbols-outlined {
        color: #45C4B0;
        margin-right: 6px;
        font-size: 22px;
    }

    /* Muted, calm caption/disclaimer styling */
    [data-testid="stCaptionContainer"] {
        color: #8896A1 !important;
    }

    /* Landing intro: the single title moment at the top of the page */
    .landing-intro {
        text-align: center;
        max-width: 620px;
        margin: 4px auto 0 auto;
        padding: 8px 12px 22px 12px;
        animation: fadeInUp 0.55s ease-out both;
    }
    .landing-intro .eyebrow {
        text-transform: uppercase;
        letter-spacing: 1.6px;
        font-size: 12.5px;
        font-weight: 700;
        color: #45C4B0 !important;
        margin: 0 0 10px 0;
    }
    .landing-intro h1 {
        font-size: 38px;
        font-weight: 800;
        margin: 0 0 14px 0;
        letter-spacing: -0.3px;
    }
    .landing-intro p.lead {
        font-size: 15.5px;
        color: #B4BFC7 !important;
        line-height: 1.65;
        margin: 0;
    }
    .landing-divider {
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin: 4px 0 24px 0;
    }

    /* Subtle hover feedback on interactive elements */
    div[data-testid="stSlider"] [role="slider"] {
        transition: box-shadow 0.15s ease;
    }
    div[data-testid="stSlider"] [role="slider"]:hover,
    div[data-testid="stSlider"] [role="slider"]:focus {
        box-shadow: 0 0 0 8px rgba(69, 196, 176, 0.18);
    }
    div[data-testid="stCheckbox"] {
        border-radius: 8px;
        padding: 2px 6px;
        margin-left: -6px;
        transition: background-color 0.15s ease;
    }
    div[data-testid="stCheckbox"]:hover {
        background-color: rgba(69, 196, 176, 0.08);
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 26px 12px 10px 12px;
        margin-top: 4px;
    }
    .app-footer a {
        color: #8896A1 !important;
        text-decoration: none;
        font-size: 13px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: color 0.15s ease;
    }
    .app-footer a:hover {
        color: #45C4B0 !important;
    }

    /* Section entrance animation: fade + slight upward slide, staggered per section */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) {
        animation: fadeInUp 0.55s ease-out 0.13s both;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2) {
        animation: fadeInUp 0.55s ease-out 0.26s both;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(3) {
        animation: fadeInUp 0.55s ease-out 0.39s both;
    }

    /* Narrow-screen tightening */
    @media (max-width: 480px) {
        .landing-intro h1 { font-size: 28px; }
        .landing-intro p.lead { font-size: 14px; }
        .landing-intro { padding: 4px 8px 16px 8px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LANDING INTRO: the single title/"what is this" moment for the
# whole page
# ============================================================
st.markdown("""
<div class="landing-intro">
    <p class="eyebrow">by Jesse Igbide</p>
    <h1>Stroke Risk Predictor</h1>
    <p class="lead">An interpretable machine learning tool that estimates a patient's stroke risk
    from a handful of clinical factors, and shows exactly what's driving that estimate.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# METHODOLOGY: shown up front so visitors get context before
# they reach the interactive tool below
# ============================================================
with st.expander(":material/info: About this model"):
    st.markdown("""
    - **Data**: synthetic EHR records generated by Synthea, with a leakage-free
      cohort design (cutoff dates = first stroke diagnosis for cases, a randomly
      chosen visit date for controls).
    - **Model**: logistic regression, chosen over XGBoost after cross-validated
      comparison showed better performance given the small positive class size.
    - **Validation**: ROC-AUC 0.858 ± 0.026 (5-fold stratified cross-validation),
      outperforming a simplified CHA2DS2-VASc-style clinical benchmark (ROC-AUC 0.754).
    - **Limitations**: synthetic data, small absolute number of positive cases,
      simplified feature set (no lab values, imaging, or family history).
    """)

st.markdown('<hr class="landing-divider">', unsafe_allow_html=True)

st.caption(":material/warning: Built on synthetic data for educational/portfolio purposes only. Not a real clinical tool.")

# ============================================================
# LOAD MODEL ARTIFACTS
# ============================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load("data/processed/stroke_model.pkl")
    scaler = joblib.load("data/processed/feature_scaler.pkl")
    background = pd.read_csv("data/processed/shap_background.csv")
    return model, scaler, background

model, scaler, background = load_artifacts()

FEATURE_ORDER = ['age_at_cutoff', 'has_hypertension', 'has_afib',
                  'has_diabetes', 'n_conditions_total', 'n_medications_total']

# ============================================================
# PATIENT PROFILE CARD
# ============================================================
with st.container(border=True):
    st.subheader(":material/person: Patient Profile")

    col1, col2 = st.columns(2)
    with col1:
        age = st.slider(":material/cake: Age", 18, 100, 55)
        n_conditions = st.slider(":material/clinical_notes: Total prior conditions on record", 0, 150, 20)
    with col2:
        n_medications = st.slider(":material/medication: Total prior medications on record", 0, 150, 25)

    st.write("**Conditions:**")
    c1, c2, c3 = st.columns(3)
    with c1:
        has_hypertension = st.checkbox(":material/favorite: Hypertension")
    with c2:
        has_afib = st.checkbox(":material/cardiology: Atrial Fibrillation")
    with c3:
        has_diabetes = st.checkbox(":material/bloodtype: Diabetes")

# ============================================================
# PREDICTION
# ============================================================
patient = pd.DataFrame([{
    'age_at_cutoff': age,
    'has_hypertension': int(has_hypertension),
    'has_afib': int(has_afib),
    'has_diabetes': int(has_diabetes),
    'n_conditions_total': n_conditions,
    'n_medications_total': n_medications
}])[FEATURE_ORDER]

patient_scaled = pd.DataFrame(scaler.transform(patient), columns=FEATURE_ORDER)
risk_proba = model.predict_proba(patient_scaled)[0, 1]

risk_label = "Low" if risk_proba < 0.33 else ("Moderate" if risk_proba < 0.66 else "Elevated")
risk_color = "#48BB78" if risk_proba < 0.33 else ("#ECC94B" if risk_proba < 0.66 else "#F56565")

# ============================================================
# PREDICTED RISK CARD
# ============================================================
with st.container(border=True):
    st.subheader(":material/monitoring: Predicted Risk")

    fig_donut = go.Figure(data=[go.Pie(
        values=[risk_proba, 1 - risk_proba],
        hole=0.75,
        marker=dict(colors=[risk_color, "#26343A"]),
        textinfo='none',
        sort=False,
        direction='clockwise',
        rotation=0,
        showlegend=False
    )])
    fig_donut.update_layout(
        annotations=[dict(
            text=f"<b>{risk_proba:.1%}</b><br><span style='font-size:16px;color:{risk_color}'>{risk_label}</span>",
            x=0.5, y=0.5, font=dict(size=32, family="Plus Jakarta Sans", color="#E8EDF0"),
            showarrow=False
        )],
        height=280,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

# ============================================================
# EXPLANATION CARD
# ============================================================
with st.container(border=True):
    st.subheader(":material/insights: Why this prediction?")
    st.caption("How much each factor pushed this patient's risk up or down, "
               "compared to a reference population of 200 patients.")

    explainer = shap.LinearExplainer(model, background)
    shap_values = explainer(patient_scaled)

    shap_df = pd.DataFrame({
        'feature': FEATURE_ORDER,
        'shap_value': shap_values.values[0]
    }).sort_values('shap_value', key=abs, ascending=True)

    bar_colors = ['#F56565' if v > 0 else '#63B3ED' for v in shap_df['shap_value']]
    fig_shap = go.Figure(go.Bar(
        x=shap_df['shap_value'],
        y=shap_df['feature'],
        orientation='h',
        marker_color=bar_colors
    ))
    fig_shap.update_layout(
        height=320,
        margin=dict(t=20, b=20, l=10, r=20),
        plot_bgcolor='#172123',
        paper_bgcolor='#172123',
        font=dict(family="Plus Jakarta Sans", color="#E8EDF0"),
        xaxis_title="Impact on risk (SHAP value)",
        xaxis=dict(gridcolor='#2A363A', zerolinecolor='#3A4850'),
        yaxis=dict(gridcolor='#2A363A')
    )
    st.plotly_chart(fig_shap, use_container_width=True, config={'displayModeBar': False})

    shap_df_display = shap_df.sort_values('shap_value', key=abs, ascending=False)
    st.dataframe(shap_df_display, hide_index=True, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="app-footer">
    <a href="#" target="_blank">
        <span class="material-symbols-outlined" style="font-size:16px;">code</span>
        View on GitHub
    </a>
</div>
""", unsafe_allow_html=True)
