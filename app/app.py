import time
from collections import deque

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from core.config import SimConfig, BaseWeights
from core.compute import compute_full_row_from_raw
from core.proposals import maybe_generate_proposal
from core.invariants import enforce_invariant, InvariantViolation

from sim.raw_generator import generate_raw_tick

from ml.config import MLRuntimeConfig
from ml.overlays import compute_ml_overlay

from ui.style import apply_style
from ui.status import render_status


CODE_VERSION = "d11-risk-console_ui_v0"
DT_SECONDS = 0.25

st.set_page_config(page_title="D11 Risk Console", layout="wide")
apply_style()

st.markdown("<div class='title'>D11 Risk Console</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Deterministic Risk Reasoning · ML Advisory Overlay · Human-Gated Decisions</div>", unsafe_allow_html=True)


def init_state():
    ss = st.session_state
    ss.seed = ss.get("seed") or int(time.time()) & 0x7FFFFFFF
    ss.tick = ss.get("tick", 0)
    ss.running = ss.get("running", False)
    ss.last_update = ss.get("last_update", time.time())

    ss.sim_cfg = ss.get("sim_cfg") or SimConfig()
    ss.weights = ss.get("weights") or BaseWeights()

    ss.history = ss.get("history") or deque(maxlen=1200)
    ss.proposals = ss.get("proposals") or deque(maxlen=32)
    ss.next_proposal_id = ss.get("next_proposal_id", 1)

    ss.ml_cfg = ss.get("ml_cfg") or MLRuntimeConfig()
    ss.ml_enabled = ss.get("ml_enabled", True)

    # placeholder: artifact loading comes later (models/)
    ss.ml_artifact = ss.get("ml_artifact", None)

if "history" not in st.session_state:
    init_state()

ss = st.session_state


# ---- Controls
c1, c2 = st.columns([1, 1])
with c1:
    if st.button("▶ Start Simulation", use_container_width=True):
        ss.running = True
        ss.last_update = time.time()
with c2:
    if st.button("⏸ Pause", use_container_width=True):
        ss.running = False


# ---- Sidebar
st.sidebar.header("Console")

ss.ml_enabled = st.sidebar.checkbox("Enable ML overlay (advisory)", value=bool(ss.ml_enabled))

with st.sidebar.expander("ML Runtime", expanded=True):
    ss.ml_cfg.window = int(st.slider("Rolling window (ticks)", 20, 120, int(ss.ml_cfg.window), 5))
    ss.ml_cfg.caution_mult_max = float(st.slider("Max caution", 1.00, 1.60, float(ss.ml_cfg.caution_mult_max), 0.01))
    ss.ml_cfg.gnss_weight_mult_max = float(st.slider("Max GNSS weight", 1.00, 1.60, float(ss.ml_cfg.gnss_weight_mult_max), 0.01))


# ---- Simulation step
if ss.running and (time.time() - ss.last_update) >= DT_SECONDS:
    prev = ss.history[-1] if ss.history else None
    tick = int(ss.tick) + 1

    raw = generate_raw_tick(prev, seed=int(ss.seed), tick=tick, cfg=ss.sim_cfg)
    df_tmp = pd.DataFrame(list(ss.history) + [raw])

    # ML overlay (optional)
    gnss_mult = 1.0
    caution_mult = 1.0
    overlay = {"anomaly": 0.0, "ood": 0.0, "uncertainty": 0.0, "caution_mult": 1.0}

    if ss.ml_enabled and ss.ml_artifact is not None:
        overlay = compute_ml_overlay(df_tmp, ss.ml_cfg, ss.ml_artifact)
        caution_mult = float(overlay["caution_mult"])
        # example gnss bias: tie to ood/anomaly (simple; can be upgraded later)
        gnss_mult = max(1.0, min(ss.ml_cfg.gnss_weight_mult_max, 1.0 + 0.7 * float(overlay["anomaly"])))

    # invariants: ML never reduces
    try:
        enforce_invariant(gnss_mult >= 1.0, "ML attempted to reduce GNSS penalty weight")
        enforce_invariant(caution_mult >= 1.0, "ML attempted to reduce caution multiplier")
    except InvariantViolation:
        ss.running = False
        st.error("SAFETY VIOLATION — SYSTEM HALTED (invariant failed)")
        st.stop()

    row = compute_full_row_from_raw(
        raw,
        weights=ss.weights,
        cfg=ss.sim_cfg,
        gnss_weight_mult=gnss_mult,
        caution_mult=caution_mult,
    )

    # final invariant: overlay risk cannot be lower
    try:
        enforce_invariant(row["overall_risk_with_ml"] >= row["overall_risk"], "ML reduced risk below base")
    except InvariantViolation:
        ss.running = False
        st.error("SAFETY VIOLATION — SYSTEM HALTED (risk decreased)")
        st.stop()

    ss.tick = tick
    ss.history.append(row)
    ss.last_update = time.time()

    # proposals deterministic-only
    p = maybe_generate_proposal(row, ss.proposals, ss.next_proposal_id)
    if p is not None:
        ss.proposals.append(p)
        ss.next_proposal_id += 1

    st.rerun()


# ---- Render
if not ss.history:
    st.info("Press Start Simulation to bring the console online. Synthetic telemetry only.")
    st.stop()

df = pd.DataFrame(list(ss.history))
latest = df.iloc[-1]

open_recs = sum(1 for p in ss.proposals if p.status == "PENDING")
ml_on = bool(ss.ml_enabled) and (ss.ml_artifact is not None)

render_status(
    tick=int(latest["tick"]),
    base_state=str(latest["state"]),
    ml_state=str(latest["state_with_ml"]),
    base_risk=float(latest["overall_risk"]),
    ml_risk=float(latest["overall_risk_with_ml"]),
    ml_on=ml_on,
    open_recs=open_recs,
    seed=int(ss.seed),
    model_name="(none)" if ss.ml_artifact is None else "loaded",
)

st.markdown("---")
left, right = st.columns([1.35, 1.0])

with left:
    st.subheader("Machine Timeline (Last 120 Ticks)")
    tail = df.tail(120)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tail["tick"], y=tail["overall_risk_with_ml"], name="Overall Risk (ML overlay)", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=tail["tick"], y=tail["overall_risk"], name="Base Risk (deterministic)", line=dict(width=1, dash="dot")))
    fig.update_layout(height=320, margin=dict(l=40, r=10, t=10, b=40), yaxis=dict(range=[0, 100], title="Risk (%)"))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Risk Breakdown (Current Tick)")
    risk_df = pd.DataFrame({
        "Mode": ["Rollover", "Slip / Traction", "Obstacle", "GNSS Penalty"],
        "Value": [
            float(latest["rollover_risk"]),
            float(latest["slip_risk"]),
            float(latest["obstacle_risk"]),
            float((100.0 - float(latest["gnss_confidence"])) * ss.weights.gnss_penalty),
        ],
    })
    bar_fig = px.bar(risk_df, x="Mode", y="Value", range_y=[0, 100], height=240)
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")
st.subheader("Human-Gated Recommendations")
if not ss.proposals:
    st.info("No proposals yet.")
else:
    for p in list(ss.proposals)[-6:]:
        st.write(f"#{p.id} [{p.status}] {p.title} — {p.rationale}")
