import json
import os
from datetime import datetime

import pandas as pd
import streamlit as st

from src.engine import run_engine

WEIGHTS_PATH = "results/weights/weights.json"
WEIGHTS_CHART_PATH = "results/plots/weights_chart.png"
FRONTIER_CHART_PATH = "results/plots/efficient_frontier.png"

st.set_page_config(
    page_title="PortfolioOptimizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("tickers.json", "r", encoding="utf-8") as f:
    STOCKS = json.load(f)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(1300px 700px at 88% -10%, #0f5132 0%, #0c111b 34%, #070b13 100%);
    color: #e5edf7;
}

section[data-testid="stSidebar"], #MainMenu, footer, header {
    visibility: hidden;
    display: none;
}

.block-container {
    padding: 1.3rem 2rem 2.2rem 2rem;
    max-width: 1250px;
}

.hero {
    border: 1px solid #263244;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    background: linear-gradient(135deg, #121a2a 0%, #121625 100%);
    margin-bottom: 1rem;
}

.hero-title {
    margin: 0;
    color: #f1f5f9;
    font-size: 1.7rem;
    font-weight: 700;
}

.hero-title span {
    color: #4ade80;
}

.hero-subtitle {
    margin: 0.55rem 0 0 0;
    color: #94a3b8;
    font-size: 0.92rem;
    line-height: 1.5;
}

.method-chip {
    display: inline-block;
    margin-top: 0.85rem;
    background: #1f293733;
    color: #a7f3d0;
    border: 1px solid #2b4b3e;
    border-radius: 999px;
    padding: 0.26rem 0.74rem;
    font-size: 0.76rem;
}

.label-text {
    color: #93a5bc;
    font-size: 0.82rem;
    margin-bottom: 0.35rem;
}

.panel {
    border: 1px solid #263244;
    border-radius: 14px;
    background: #111827bb;
    padding: 0.9rem 0.95rem;
}

.panel-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.9rem;
}

.panel-title {
    color: #e2e8f0;
    font-size: 0.95rem;
    font-weight: 600;
}

.count-pill {
    color: #08130d;
    background: #4ade80;
    border-radius: 999px;
    padding: 0.1rem 0.55rem;
    font-size: 0.74rem;
    font-weight: 700;
}

.stock-card {
    border: 1px solid #253349;
    background: #0d1525;
    border-radius: 12px;
    padding: 0.55rem 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.stock-logo-img {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    object-fit: cover;
}

.stock-logo-fallback {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    background: #263244;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
}

.stock-ticker {
    color: #f8fafc;
    font-size: 0.86rem;
    font-weight: 600;
    line-height: 1.2;
}

.stock-name {
    color: #8ea0b8;
    font-size: 0.73rem;
    line-height: 1.2;
}

[class*="st-key-rm_"] button {
    border: 1px solid #ef4444 !important;
    background: #ef444420 !important;
    color: #fca5a5 !important;
    border-radius: 8px !important;
    min-width: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    margin-top: 8px !important;
}

[class*="st-key-run_engine"] button {
    background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%) !important;
    color: #06110c !important;
    border: none !important;
    border-radius: 11px !important;
    min-height: 40px !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 26px #22c55e33;
}

[class*="st-key-clear_all"] button {
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #cbd5e1 !important;
    background: #111827 !important;
}

.status-card {
    border: 1px dashed #36547f;
    border-radius: 12px;
    padding: 0.8rem 0.9rem;
    margin: 0.85rem 0 0.25rem 0;
    background: #0f172a66;
}

.status-title {
    color: #e2e8f0;
    font-size: 0.9rem;
    font-weight: 600;
}

.status-sub {
    color: #93a5bc;
    font-size: 0.82rem;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}

.metric-card {
    border: 1px solid #2c3c52;
    background: #101a2c;
    border-radius: 12px;
    padding: 0.8rem 0.9rem;
}

.metric-label {
    color: #9fb1c8;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.metric-value {
    color: #4ade80;
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.2rem;
}

.insight {
    border: 1px solid #2f3f57;
    border-radius: 12px;
    background: #0f172a;
    padding: 0.75rem 0.95rem;
    margin-bottom: 0.8rem;
}

.insight-title {
    color: #f1f5f9;
    font-size: 0.84rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
}

.insight-body {
    color: #9eb0c7;
    font-size: 0.82rem;
    line-height: 1.4;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #0f172a !important;
    border: 1px solid #2b3a51 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within > div {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 1px #22c55e40 !important;
}

.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid #2b3a51;
}

.stTabs [data-baseweb="tab"] {
    color: #8da2bd !important;
}

.stTabs [aria-selected="true"] {
    color: #4ade80 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #22c55e !important;
}

.empty-area {
    border: 1px dashed #2f415f;
    border-radius: 12px;
    background: #0f172a44;
    min-height: 290px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem;
}

.empty-title {
    color: #dce6f4;
    font-size: 1.02rem;
    font-weight: 600;
}

.empty-sub {
    color: #8ea3bf;
    font-size: 0.84rem;
    margin-top: 0.35rem;
}
</style>
""",
    unsafe_allow_html=True,
)


def logo_html(ticker: str) -> str:
    clean = ticker.replace(".SA", "")
    url = f"https://icons.brapi.dev/icons/{clean}.svg"
    return (
        f'<img src="{url}" class="stock-logo-img" '
        "onerror=\"this.style.display='none';this.nextElementSibling.style.display='flex'\" />"
        f'<div class="stock-logo-fallback" style="display:none">{clean[:2]}</div>'
    )


def initialize_state() -> None:
    defaults = {
        "selected_stocks": [],
        "ui_state": "idle",
        "run_payload": None,
        "run_error": None,
        "last_run_at": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_results() -> None:
    st.session_state.run_payload = None
    st.session_state.run_error = None
    st.session_state.last_run_at = None
    st.session_state.ui_state = "ready" if st.session_state.selected_stocks else "idle"


def load_weights() -> dict:
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    try:
        with open(WEIGHTS_PATH, "r", encoding="utf-8") as f:
            weights = json.load(f)
        return weights if isinstance(weights, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def normalize_payload(raw_payload) -> dict:
    if isinstance(raw_payload, dict):
        expected_return = float(raw_payload.get("expected_return", 0))
        volatility = float(raw_payload.get("volatility", 0))
    elif isinstance(raw_payload, (tuple, list)) and len(raw_payload) == 2:
        expected_return = float(raw_payload[0])
        volatility = float(raw_payload[1])
    else:
        raise ValueError("Engine returned an unexpected payload.")

    sharpe = expected_return / volatility if volatility else 0.0
    return {
        "expected_return": expected_return,
        "volatility": volatility,
        "sharpe": sharpe,
        "selected_stocks": list(st.session_state.selected_stocks),
    }


initialize_state()
sel = st.session_state.selected_stocks

st.markdown(
    """
<div class="hero">
  <h1 class="hero-title">Portfolio<span>Optimizer</span></h1>
  <p class="hero-subtitle">
    Build a B3 portfolio, run optimization, and inspect how the engine balances return and risk.
    The UI is structured to explain the outcome, not only display charts.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="label-text">Search B3 stocks</div>', unsafe_allow_html=True)
available = [ticker for ticker in STOCKS if ticker not in sel]
search_col, add_col = st.columns([20, 2], gap="small")

with search_col:
    chosen = st.selectbox(
        "Search B3 stocks",
        [""] + available,
        format_func=lambda x: f"{x} — {STOCKS.get(x, '')}" if x else "Type or select a stock (PETR4, VALE3, ITUB4...)",
        label_visibility="collapsed",
    )

with add_col:
    add_clicked = st.button("Add", key="add_stock", use_container_width=True, disabled=not chosen)
    if add_clicked and chosen:
        sel.append(chosen)
        reset_results()
        st.rerun()

left_col, right_col = st.columns([1.08, 2.6], gap="large")

with left_col:
    run_clicked = st.button("Run optimization", key="run_engine", use_container_width=True, disabled=len(sel) < 2)
    if run_clicked and len(sel) < 2:
        st.warning("Select at least 2 assets to run optimization.")

    if run_clicked and len(sel) >= 2:
        st.session_state.ui_state = "running"
        st.session_state.run_error = None
        with st.spinner("Fetching market data and solving max-Sharpe allocation..."):
            try:
                engine_payload = run_engine(sel)
                st.session_state.run_payload = normalize_payload(engine_payload)
                st.session_state.ui_state = "success"
                st.session_state.last_run_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except Exception as exc:
                st.session_state.run_payload = None
                st.session_state.ui_state = "error"
                st.session_state.run_error = str(exc)
        st.rerun()

    st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="panel">
  <div class="panel-head">
    <span class="panel-title">Selected assets</span>
    <span class="count-pill">{len(sel)}</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

    for ticker in list(sel):
        card_col, remove_col = st.columns([1, 0.21], gap="small")
        with card_col:
            display = ticker.replace(".SA", "")
            st.markdown(
                f"""
<div class="stock-card">
  {logo_html(ticker)}
  <div>
    <div class="stock-ticker">{display}</div>
    <div class="stock-name">{STOCKS.get(ticker, "")}</div>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )
        with remove_col:
            if st.button("✕", key=f"rm_{ticker}"):
                sel.remove(ticker)
                reset_results()
                st.rerun()

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    if st.button("Clear all", key="clear_all", use_container_width=True, disabled=not sel):
        st.session_state.selected_stocks = []
        reset_results()
        st.rerun()

with right_col:
    run_payload = st.session_state.run_payload
    weights = load_weights()
    selection_matches_weights = bool(weights) and set(weights.keys()) == set(sel)
    has_success_results = (
        st.session_state.ui_state == "success"
        and run_payload is not None
        and selection_matches_weights
        and os.path.exists(WEIGHTS_CHART_PATH)
        and os.path.exists(FRONTIER_CHART_PATH)
    )

    if st.session_state.ui_state == "error":
        st.error(f"Optimization failed. {st.session_state.run_error or 'Please try again.'}")

    tabs = st.tabs(["Overview", "Allocation", "Efficient Frontier"])

    with tabs[0]:
        if not sel:
            st.markdown(
                """
<div class="empty-area">
  <div>
    <div class="empty-title">Start with your B3 asset universe</div>
    <div class="empty-sub">Add assets on the left. After that, run optimization to reveal expected return, volatility, and Sharpe.</div>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )
        elif st.session_state.ui_state in {"idle", "ready"}:
            st.markdown(
                f"""
<div class="status-card">
  <div class="status-title">Portfolio ready: {len(sel)} asset(s) selected</div>
  <div class="status-sub">Next step: run optimization to generate the strategy narrative and charts.</div>
</div>
""",
                unsafe_allow_html=True,
            )
        elif st.session_state.ui_state == "running":
            st.info("Optimization is running. Results will appear here once complete.")
        elif has_success_results:
            ret = run_payload["expected_return"] * 100
            vol = run_payload["volatility"] * 100
            sharpe = run_payload["sharpe"]

            st.markdown(
                f"""
<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-label">Expected Return</div>
    <div class="metric-value">{ret:.2f}%</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Volatility</div>
    <div class="metric-value">{vol:.2f}%</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Sharpe Ratio</div>
    <div class="metric-value">{sharpe:.3f}</div>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

        else:
            st.warning("Results are stale for the current selection. Please run optimization again.")

    with tabs[1]:
        if has_success_results:
            st.image(WEIGHTS_CHART_PATH, use_container_width=True)
            st.caption("Bar chart of optimal portfolio allocation across selected assets.")

            weights_df = (
                pd.DataFrame(
                    [
                        {"Ticker": ticker.replace(".SA", ""), "Weight (%)": round(weight * 100, 2)}
                        for ticker, weight in weights.items()
                    ]
                )
                .sort_values("Weight (%)", ascending=False)
                .reset_index(drop=True)
            )
            st.dataframe(weights_df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download weights (JSON)",
                data=json.dumps(weights, indent=2),
                file_name="optimized_weights.json",
                mime="application/json",
            )
        else:
            st.markdown(
                """
<div class="empty-area">
  <div>
    <div class="empty-title">Allocation view pending</div>
    <div class="empty-sub">Run optimization to inspect the portfolio weights chart and table.</div>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

    with tabs[2]:
        if has_success_results:
            st.image(FRONTIER_CHART_PATH, use_container_width=True)
            st.caption("5,000 random long-only portfolios are sampled; the star marks the max-Sharpe solution.")
        else:
            st.markdown(
                """
<div class="empty-area">
  <div>
    <div class="empty-title">Efficient frontier unavailable</div>
    <div class="empty-sub">Run optimization to render the risk-return landscape.</div>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )