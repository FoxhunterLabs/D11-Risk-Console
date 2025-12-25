import streamlit as st

def apply_style():
    st.markdown(
        """
<style>
.title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #ffcc00;
    text-transform: uppercase;
    margin-bottom: 0px;
}
.subtitle {
    font-size: 14px;
    color: #CFD8DC;
    margin-top: -6px;
    margin-bottom: 12px;
}
.status-bar {
    background-color: #111;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    gap: 10px;
    font-size: 13px;
    color: #ECEFF1;
    flex-wrap: wrap;
}
.status-item span.label { opacity: 0.7; margin-right: 4px; }
.pill { padding: 2px 10px; border-radius: 999px; font-weight: 800; }
.pill-STABLE { background: #1b5e20; color: #e8f5e9; }
.pill-ELEVATED { background: #f9a825; color: #111; }
.pill-HIGH { background: #ef6c00; color: #fff3e0; }
.pill-CRITICAL { background: #b71c1c; color: #ffebee; }
.pill-MLON { background: #0d47a1; color: #e3f2fd; }
.pill-MLOFF { background: #4e342e; color: #efebe9; }
.smallcap { font-size: 12px; opacity: 0.85; }

.mini-banner {
    background: #2b0b0b;
    border: 1px solid #7a1d1d;
    color: #ffdddd;
    padding: 8px 10px;
    border-radius: 8px;
    font-size: 12px;
    line-height: 1.25;
}
.mini-banner b { color: #ffffff; }
</style>
""",
        unsafe_allow_html=True,
    )
