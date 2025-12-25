import streamlit as st

def render_status(*, tick: int, base_state: str, ml_state: str, base_risk: float, ml_risk: float, ml_on: bool, open_recs: int, seed: int, model_name: str):
    margin = 100.0 - float(ml_risk)

    pill_base = f"<span class='pill pill-{base_state}'>{base_state}</span>"
    pill_ml = f"<span class='pill pill-{ml_state}'>{ml_state}</span>"
    ml_pill = "<span class='pill pill-MLON'>ML ON</span>" if ml_on else "<span class='pill pill-MLOFF'>ML OFF</span>"

    st.markdown(
        f"""
        <div class="status-bar">
            <div class="status-item"><span class="label">Tick:</span> {tick}</div>
            <div class="status-item"><span class="label">State (base):</span> {pill_base}</div>
            <div class="status-item"><span class="label">State (ML):</span> {pill_ml}</div>
            <div class="status-item"><span class="label">Risk (base):</span> {base_risk:.1f}%</div>
            <div class="status-item"><span class="label">Risk (ML):</span> {ml_risk:.1f}%</div>
            <div class="status-item"><span class="label">Margin:</span> {margin:.1f}%</div>
            <div class="status-item"><span class="label">Open Recs:</span> {open_recs}</div>
            <div class="status-item"><span class="label">ML:</span> {ml_pill}</div>
            <div class="status-item"><span class="label">Active:</span> seed={seed}, tick={tick}</div>
            <div class="status-item"><span class="label">Model:</span> {model_name}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
