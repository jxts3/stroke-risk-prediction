"""
Stroke Risk Predictor - Control Room UI
===========================================
Run with: streamlit run app.py
Requires: data/processed/stroke_model.pkl, feature_scaler.pkl,
          feature_stats.csv, shap_background.csv
"""

import math
import uuid

import streamlit as st
import pandas as pd
import joblib
import shap

st.set_page_config(page_title="Stroke Risk Predictor", page_icon=":material/monitor_heart:", layout="centered")

# ============================================================
# Control Room palette - one hue (oxblood), three intensities.
# ox-bright = primary emphasis (main gauge, elevated readings)
# ox-mid    = secondary emphasis (dial fills, moderate readings)
# ox-dim    = low emphasis (declining / protective indicators)
# ============================================================
OX_BRIGHT = "#7A1F2B"
OX_MID = "#A8434C"
OX_DIM = "#8A5257"

# ============================================================
# GLOBAL STYLE: light, restrained instrument-panel theme.
# Instrument Serif italic is reserved for the hero headline only;
# Archivo carries every label/body line; Space Mono carries every
# number on the page.
# ============================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Instrument+Serif:ital@1&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..500,0,0&display=swap" rel="stylesheet">
<style>
    /* Streamlit's own theme CSS ships highly-specific selectors for
       every text element (stMarkdownContainer p, stCaptionContainer,
       stWidgetLabel, etc.) that otherwise beat a plain `body` rule,
       silently falling back to its default UI font. Force Archivo
       everywhere with !important, then win back Instrument Serif /
       Space Mono / Material Symbols for their specific classes with
       rules placed after (equal specificity, source order decides). */
    html, body, [class*="css"], p, div, li, label, a,
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p,
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label,
    .stMarkdown, .stMarkdown p, h1, h2, h4, h5, h6, h3 {
        font-family: 'Archivo', sans-serif !important;
    }
    .stApp {
        background-color: #FAF9F7;
    }
    h1, h2, h3 { color: #221A1A !important; }
    p, li, label, .stMarkdown { color: #746360 !important; }

    .num, .num * { font-family: 'Space Mono', monospace !important; }

    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined' !important;
        font-weight: normal;
        font-style: normal;
        vertical-align: middle;
        line-height: 1;
    }

    h3 {
        font-size: 19px !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px;
    }
    h3 .material-symbols-outlined {
        color: #7A1F2B;
        margin-right: 6px;
        font-size: 22px;
    }

    [data-testid="stCaptionContainer"] {
        color: #746360 !important;
    }

    /* ---- Hero: centered, oversized italic headline ----
       Streamlit sets its own text-align on stMarkdownContainer p,
       which (being an explicit rule) beats the inherited center from
       .hero-wrap regardless of specificity, so it's forced here too. */
    .hero-wrap { text-align: center !important; padding: 24px 24px 8px; }
    .hero-wrap p { text-align: center !important; }
    .eyebrow {
        font-size: 16px;
        color: #746360 !important;
        margin: 6px 0 20px 0;
        text-align: center !important;
    }
    .hero-title {
        font-family: 'Instrument Serif', serif !important;
        font-style: italic;
        font-weight: 400 !important;
        font-size: 156px !important;
        line-height: 0.92 !important;
        color: #221A1A;
        margin: 0 !important;
        text-align: center !important;
    }
    .title-underline {
        width: 0;
        height: 3px;
        background: #7A1F2B;
        margin: 20px auto 0;
        animation: drawLine 0.9s cubic-bezier(.2,.8,.2,1) 0.5s forwards;
    }
    @keyframes drawLine { to { width: 120px; } }
    .hero-sub {
        font-size: 14px;
        color: #746360;
        line-height: 1.6;
        margin: 20px auto 0;
        max-width: 360px;
        text-align: center !important;
    }
    .gauge-hero { position: relative; display: flex; justify-content: center; margin-top: 36px; }
    .ring-track { fill: none; stroke: #E3DBD9; }
    .ring-fill { fill: none; stroke-linecap: round; }
    .gauge-readout {
        position: absolute; inset: 0;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .gauge-readout .pct { font-size: 44px; font-weight: 700; }
    .gauge-readout .label { font-size: 14.5px; color: #746360; margin-top: 4px; }

    /* ---- Instrument panel (dials) - each is its own card, matching
       the reference's individually-bordered dial-card treatment ---- */
    .dial-card {
        display: flex; flex-direction: column; align-items: center;
        background: #FFFFFF; border: 1px solid #E3DBD9; border-radius: 14px;
        padding: 22px 12px;
    }
    .dial-track { stroke: #E3DBD9; fill: none; }
    .dial-fill { fill: none; stroke-linecap: round; }

    /* ---- Signal readout ---- */
    .readout-row {
        display: grid; grid-template-columns: 150px 1fr 64px;
        align-items: center; gap: 12px; margin-bottom: 14px;
    }
    .readout-row .name { color: #746360; font-size: 15px; }
    .bar-track { position: relative; height: 6px; background: #E3DBD9; border-radius: 3px; }
    .bar-fill { position: absolute; top: 0; height: 100%; border-radius: 3px; }
    .bar-fill.up { left: 50%; background: #7A1F2B; }
    .bar-fill.down { right: 50%; background: #8A5257; }
    .readout-row .amt { text-align: right; font-size: 14px; }

    /* Subtle hover feedback on interactive elements, tinted oxblood */
    div[data-testid="stSlider"] [role="slider"] {
        transition: box-shadow 0.15s ease;
    }
    div[data-testid="stSlider"] [role="slider"]:hover,
    div[data-testid="stSlider"] [role="slider"]:focus {
        box-shadow: 0 0 0 8px rgba(122, 31, 43, 0.14);
    }
    div[data-testid="stSlider"] { font-family: 'Space Mono', monospace; }

    /* Footer */
    .app-footer { text-align: center; padding: 26px 12px 10px 12px; margin-top: 4px; }
    .app-footer a {
        color: #746360 !important; text-decoration: none; font-size: 13px;
        display: inline-flex; align-items: center; gap: 6px; transition: color 0.15s ease;
    }
    .app-footer a:hover { color: #7A1F2B !important; }

    /* Scroll-triggered reveal state, toggled by the script below.
       (Streamlit renames its internal container testids across
       versions, so the hide/reveal styles are applied inline by the
       script instead of keyed to a testid here.) Slide-up + fade,
       not a clip-path wipe - a transform doesn't zero out the
       element's own paintable area the way clip-path does, so it
       doesn't fight the IntersectionObserver watching it. */
    .sr-hidden { opacity: 0; transform: translateY(28px); transition: opacity 0.7s ease, transform 0.7s cubic-bezier(.2,.8,.2,1); }
    .sr-hidden.sr-in-view { opacity: 1 !important; transform: translateY(0) !important; }

    /* These need !important too: the base .hero-title/.hero-sub rules
       above are !important (to beat Streamlit's own h1/p sizing), and
       a plain override can't win against that even inside a media
       query - only a later, equally-!important rule can. Streamlit's
       "centered" layout caps out well under a full-bleed page's width,
       so this breakpoint also fires well before a phone-sized screen. */
    @media (max-width: 700px) {
        .hero-title { font-size: 72px !important; }
        .hero-sub { font-size: 14px !important; max-width: 320px !important; }
        .gauge-readout .pct { font-size: 38px !important; }
    }
    @media (max-width: 420px) {
        .hero-title { font-size: 52px !important; }
        .hero-sub { font-size: 13px !important; }
        .gauge-readout .pct { font-size: 32px !important; }
    }

    /* Respect the OS-level "reduce motion" setting: skip the draw-in
       and slide-up animations, jump straight to their end state. The
       gauge/dial rings need no extra rule - their SVG stroke-dashoffset
       attribute already holds the final value, the keyframe is what
       was animating away from it, so disabling the animation alone
       reveals the correct final ring for free. */
    @media (prefers-reduced-motion: reduce) {
        .ring-fill, .dial-fill { animation: none !important; }
        .title-underline { animation: none !important; width: 120px !important; }
        .sr-hidden { transition: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SCROLL REVEAL - a zero-height component whose script reaches into
# the parent document (same origin, so window.parent.document is
# allowed) and watches each bordered panel with an IntersectionObserver,
# adding .sr-in-view (slide-up + fade, see CSS above) the first time
# each panel enters the viewport. Panels are detected by their actual
# rendered border rather than a testid, since Streamlit has renamed
# that internal class across versions before. Runs once per panel
# (unobserve after it reveals) and re-scans on an interval to pick up
# panels not yet mounted, so it survives reruns without re-triggering
# already-revealed panels.
# ============================================================
st.iframe("""
<script>
(function() {
  var doc = window.parent.document;
  var win = window.parent;
  function bind() {
    var blocks = doc.querySelectorAll('div[data-testid="stVerticalBlock"]:not([data-sr-bound])');
    blocks.forEach(function(el) {
      var cs = win.getComputedStyle(el);
      if (parseFloat(cs.borderTopWidth) <= 0) return;
      el.setAttribute('data-sr-bound', '1');
      el.classList.add('sr-hidden');
      var obs = new win.IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('sr-in-view');
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
      obs.observe(el);
    });
  }
  bind();
  setInterval(bind, 400);
})();
</script>
""", height=1)


# ============================================================
# SVG helpers - regenerated from live widget state on every rerun
# ============================================================
def gauge_svg(pct, color, label, size=220, stroke=16):
    r = (size - stroke) / 2
    c = size / 2
    circumference = 2 * math.pi * r
    offset = circumference * (1 - pct / 100)
    # A fresh keyframe name each call forces the browser to restart the
    # draw-in animation even when Streamlit patches the same DOM node
    # in place instead of recreating it on a rerun.
    anim = f"gaugeDraw_{uuid.uuid4().hex[:8]}"
    return f"""
    <style>
    @keyframes {anim} {{ from {{ stroke-dashoffset: {circumference:.2f}; }} to {{ stroke-dashoffset: {offset:.2f}; }} }}
    </style>
    <div class="gauge-hero">
      <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="transform: rotate(-90deg);">
        <circle class="ring-track" cx="{c}" cy="{c}" r="{r}" stroke-width="{stroke}"/>
        <circle class="ring-fill" cx="{c}" cy="{c}" r="{r}" stroke-width="{stroke}" stroke="{color}"
                stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}"
                style="animation: {anim} 1.1s cubic-bezier(.3,.9,.3,1) forwards; filter: drop-shadow(0 2px 6px rgba(122,31,43,0.25));"/>
      </svg>
      <div class="gauge-readout">
        <div class="pct num" style="color:{color};">{pct:.0f}%</div>
        <div class="label">{label}</div>
      </div>
    </div>
    """


def dial_svg(value, min_v, max_v, color=OX_MID, size=72, stroke=8):
    r = (size - stroke) / 2
    c = size / 2
    circumference = 2 * math.pi * r
    frac = min(1.0, max(0.0, (value - min_v) / (max_v - min_v)))
    offset = circumference * (1 - frac)
    anim = f"dialDraw_{uuid.uuid4().hex[:8]}"
    return f"""
    <style>
    @keyframes {anim} {{ from {{ stroke-dashoffset: {circumference:.2f}; }} to {{ stroke-dashoffset: {offset:.2f}; }} }}
    </style>
    <div class="dial-card">
      <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="transform: rotate(-90deg);">
        <circle class="dial-track" cx="{c}" cy="{c}" r="{r}" stroke-width="{stroke}"/>
        <circle class="dial-fill" cx="{c}" cy="{c}" r="{r}" stroke-width="{stroke}" stroke="{color}"
                stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}"
                style="animation: {anim} 0.5s cubic-bezier(.3,.9,.3,1) forwards; filter: drop-shadow(0 1px 3px rgba(122,31,43,0.2));"/>
      </svg>
    </div>
    """


# Raw trained-model column name -> plain-language label. Every place
# a feature name reaches the UI (signal readout rows, the raw table
# below them) routes through this instead of showing the column name.
FEATURE_LABELS = {
    'age_at_cutoff': 'Age',
    'has_hypertension': 'Hypertension',
    'has_afib': 'Atrial fibrillation',
    'has_diabetes': 'Diabetes',
    'n_conditions_total': 'Number of conditions',
    'n_medications_total': 'Number of medications',
}


def readout_rows_html(shap_df):
    max_abs = max(abs(v) for v in shap_df["shap_value"]) or 1.0
    rows = []
    for _, row in shap_df.iterrows():
        v = row["shap_value"]
        width_pct = min(45.0, (abs(v) / max_abs) * 45.0)
        direction = "up" if v > 0 else "down"
        label = FEATURE_LABELS.get(row['feature'], row['feature'])
        rows.append(f"""
        <div class="readout-row">
            <span class="name">{label}</span>
            <div class="bar-track"><div class="bar-fill {direction}" style="width:{width_pct:.1f}%;"></div></div>
            <span class="amt num">{v:+.2f}</span>
        </div>
        """)
    return "\n".join(rows)


# ============================================================
# HERO: centered - oversized italic serif headline, underline,
# subtitle, then the live risk gauge stacked beneath, all centered.
# The gauge slot is filled in further down once the real widget
# values are known, so it stays live without moving off the top.
# ============================================================
st.markdown("""
<div class="hero-wrap">
<div class="eyebrow">Synthetic EHR model</div>
<h1 class="hero-title">Stroke<br>risk</h1>
<div class="title-underline"></div>
<p class="hero-sub" style="text-align: center !important;">An interpretable machine learning tool that estimates a patient's
stroke risk from a handful of clinical factors, and shows exactly what's driving that
estimate. A portfolio project by Jesse Igbide.</p>
</div>
""", unsafe_allow_html=True)
gauge_slot = st.empty()

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


@st.cache_resource
def load_explainer(_model, _background):
    # max_samples=200 explicitly, matching the "reference population of
    # 200 patients" claim in the Signal Readout caption below - the
    # default (100) was silently subsampling half the background set,
    # and doing it fresh on every single rerun. Caching this means the
    # real per-rerun cost is just explainer(patient), not rebuilding the
    # masker's background statistics from scratch on every slider drag.
    masker = shap.maskers.Independent(_background, max_samples=200)
    return shap.LinearExplainer(_model, masker)


model, scaler, background = load_artifacts()
explainer = load_explainer(model, background)

FEATURE_ORDER = ['age_at_cutoff', 'has_hypertension', 'has_afib',
                  'has_diabetes', 'n_conditions_total', 'n_medications_total']


# ============================================================
# INTERACTIVE SECTION - a fragment, so dragging a slider or flipping a
# toggle only reruns this function instead of the whole script. The
# CSS injection, the scroll-reveal iframe, and the methodology
# expander above all get skipped on every one of those reruns, not
# just re-executed for nothing every time.
# ============================================================
@st.fragment
def interactive_section():
    # INSTRUMENT PANEL: three live dials (real st.slider inputs, each
    # mirrored by an SVG dial regenerated from the current value) plus
    # three toggles. Every widget here feeds the same live recompute.
    with st.container(border=True):
        st.subheader(":material/tune: Instrument panel")

        d1, d2, d3 = st.columns(3)
        with d1:
            dial_age_slot = st.empty()
            age = st.slider(":material/cake: Age", 18, 100, 55, label_visibility="visible")
            dial_age_slot.markdown(dial_svg(age, 18, 100, color=OX_MID), unsafe_allow_html=True)
        with d2:
            dial_cond_slot = st.empty()
            n_conditions = st.slider(":material/clinical_notes: Prior conditions", 0, 150, 20)
            dial_cond_slot.markdown(dial_svg(n_conditions, 0, 150, color=OX_MID), unsafe_allow_html=True)
        with d3:
            dial_med_slot = st.empty()
            n_medications = st.slider(":material/medication: Prior medications", 0, 150, 25)
            dial_med_slot.markdown(dial_svg(n_medications, 0, 150, color=OX_MID), unsafe_allow_html=True)

        st.write("**Conditions:**")
        t1, t2, t3 = st.columns(3)
        with t1:
            has_hypertension = st.toggle(":material/favorite: Hypertension")
        with t2:
            has_afib = st.toggle(":material/cardiology: Atrial fibrillation")
        with t3:
            has_diabetes = st.toggle(":material/bloodtype: Diabetes")

    # PREDICTION - real model, unchanged inference path
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
    risk_pct = risk_proba * 100

    if risk_pct >= 60:
        risk_label, risk_color = "elevated risk", OX_BRIGHT
    elif risk_pct >= 30:
        risk_label, risk_color = "moderate risk", OX_MID
    else:
        risk_label, risk_color = "low risk", OX_DIM

    # Fill the hero gauge slot now that the real inputs are known -
    # this placeholder was created outside the fragment, up in the
    # hero, but a fragment can still update elements created before it.
    gauge_slot.markdown(gauge_svg(risk_pct, risk_color, risk_label), unsafe_allow_html=True)

    # EXPLANATION CARD - live SHAP attribution, oxblood/dim readout
    with st.container(border=True):
        st.subheader(":material/insights: Signal readout")
        st.caption("How much each factor pushed this patient's risk up or down, "
                   "compared to a reference population of 200 patients.")

        shap_values = explainer(patient_scaled)

        shap_df = pd.DataFrame({
            'feature': FEATURE_ORDER,
            'shap_value': shap_values.values[0]
        }).sort_values('shap_value', key=abs, ascending=False)

        st.markdown(readout_rows_html(shap_df), unsafe_allow_html=True)
        display_df = shap_df.assign(feature=shap_df['feature'].map(lambda f: FEATURE_LABELS.get(f, f)))
        with st.expander(":material/table_rows: Raw values"):
            st.dataframe(display_df, hide_index=True, width='stretch')


interactive_section()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="app-footer">
    <a href="https://github.com/jxts3/stroke-risk-prediction" target="_blank">
        <span class="material-symbols-outlined" style="font-size:16px;">code</span>
        View on GitHub
    </a>
</div>
""", unsafe_allow_html=True)
