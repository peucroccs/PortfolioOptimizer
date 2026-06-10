import streamlit as st
import json
import os
from src.engine import run_engine

st.set_page_config(
    page_title="PortfolioOptimizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("tickers.json", "r", encoding="utf-8") as f:
    STOCKS = json.load(f)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f1117;
    color: #e2e8f0;
}
.stApp { background-color: #0f1117; }
section[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2rem 2rem 2rem; max-width: 100%; }

/* Top bar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.4rem;
}
.logo {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e2e8f0;
}
.logo span { color: #22c55e; }

.deploy-btn {
    background: #22c55e;
    color: #0f1117;
    border-radius: 8px;
    padding: 6px 20px;
    font-weight: 600;
    font-size: 0.88rem;
    cursor: pointer;
}

.search-label { font-size: 0.82rem; color: #94a3b8; margin-bottom: 6px; }

/* Panel */
.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.panel-title { font-weight: 600; font-size: 0.97rem; color: #22c55e; }
.count-badge {
    background: #22c55e;
    color: #0f1117;
    border-radius: 6px;
    padding: 1px 9px;
    font-size: 0.78rem;
    font-weight: 700;
}

/* Stock card */
.stock-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #0f1117;
    border: 1px solid #2a3142;
    border-radius: 10px;
    padding: 10px 14px;
    width: 100%;
    box-sizing: border-box;
}
.stock-logo-img {
    width: 36px; height: 36px;
    border-radius: 8px;
    object-fit: cover;
    flex-shrink: 0;
}
.stock-logo-fallback {
    width: 36px; height: 36px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.7rem; color: white;
    flex-shrink: 0;
    background: #2a3142;
    letter-spacing: -0.5px;
}
.stock-ticker { font-weight: 600; font-size: 0.88rem; line-height: 1.3; }
.stock-name   { font-size: 0.72rem; color: #64748b; line-height: 1.3; }

/* X button column — prevent clipping */
div[data-testid="stHorizontalBlock"] > div:last-child {
    overflow: visible !important;
    min-width: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* All buttons inside the X column */
div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] button {
    background: #ef444420 !important;
    border: 1.5px solid #ef4444 !important;
    color: #ef4444 !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    line-height: 1 !important;
    overflow: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-top: 8px !important;
}
div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] button:hover {
    background: #ef444440 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 4px;
    border-bottom: 1px solid #2a3142;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] { color: #22c55e !important; }
.stTabs [data-baseweb="tab-highlight"] { background: #22c55e !important; }
.stTabs [data-baseweb="tab-border"] { background: #2a3142 !important; }

/* Empty state */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 340px;
    color: #64748b;
    text-align: center;
}
.empty-title { font-size: 1.1rem; font-weight: 600; color: #94a3b8; margin-bottom: 8px; }
.empty-sub   { font-size: 0.84rem; }

/* Success banner */
.success-banner {
    background: #14532d33;
    border: 1px solid #22c55e55;
    border-radius: 10px;
    padding: 12px 16px;
    color: #4ade80;
    font-size: 0.88rem;
    margin-bottom: 16px;
}

/* + add button */
div[data-testid="stButton"]:has(button[kind="secondary"]:not([data-testid^="rm_"])) button {
    background: #22c55e !important;
    border: 1.5px solid #22c55e !important;
    color: #0f1117 !important;
    border-radius: 8px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
}

div[data-testid="stSelectbox"] label { display: none; }

/* Fixed Run button */
.run-btn-wrapper {
    position: fixed;
    bottom: 32px;
    right: 36px;
    z-index: 9999;
}
.run-btn {
    background: #22c55e;
    color: #0f1117;
    border: none;
    border-radius: 12px;
    padding: 14px 32px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 24px #22c55e55;
    letter-spacing: 0.02em;
    transition: background 0.15s, box-shadow 0.15s;
}
.run-btn:hover {
    background: #16a34a;
    box-shadow: 0 6px 32px #22c55e88;
}

/* Hide the native form / submit button — visual is handled by the fixed HTML button */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}
div[data-testid="stFormSubmitButton"] button {
    background: #22c55e !important;
    color: #0f1117 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 6px 0 !important;
    font-size: 1.1rem !important;
    font-weight: 900 !important;
    width: 100% !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px #22c55e44 !important;
    letter-spacing: 0.1em !important;
}
div[data-testid="stFormSubmitButton"] button p {
    font-size: 1.1rem !important;
    font-weight: 900 !important;
    color: #0f1117 !important;
    -webkit-text-stroke: 1px #0f1117 !important;
    margin: 0 !important;
    line-height: 1 !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background: #16a34a !important;
    box-shadow: 0 6px 28px #22c55e77 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Logo ──────────────────────────────────────────────────────────────────────
# brapi serve logos em URL fixa: https://icons.brapi.dev/icons/{TICKER}.svg
def logo_html(ticker: str) -> str:
    clean = ticker.replace(".SA", "")
    url = f"https://icons.brapi.dev/icons/{clean}.svg"
    return f'<img src="{url}" class="stock-logo-img" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'" /><div class="stock-logo-fallback" style="display:none">{clean[:2]}</div>'

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_stocks" not in st.session_state:
    st.session_state.selected_stocks = []

if "ran" not in st.session_state:
    st.session_state.ran = False

sel = st.session_state.selected_stocks

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="logo">Portfolio<span>Optimizer</span></div>
  <span class="deploy-btn">Deploy</span>
</div>
""", unsafe_allow_html=True)

# ── Search + Add ──────────────────────────────────────────────────────────────
st.markdown('<div class="search-label">Search B3 stocks</div>', unsafe_allow_html=True)

available = [t for t in STOCKS if t not in sel]
s_col, btn_col = st.columns([22, 1])

with s_col:
    chosen = st.selectbox(
        "search",
        [""] + available,
        format_func=lambda x: f"{x} — {STOCKS[x]}" if x else "Type or select a stock (e.g. PETR4, VALE3, ITUB4...)",
        label_visibility="collapsed",
    )
with btn_col:
    if st.button("➕", use_container_width=True) and chosen not in sel:
        sel.append(chosen)
        st.rerun()

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ── Main columns ──────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 3], gap="medium")

# ── LEFT panel ────────────────────────────────────────────────────────────────
with left_col:
    # ── Run button ────────────────────────────────────────────────────────────
    with st.form("run_form"):
        run_submitted = st.form_submit_button("▶   Run", use_container_width=True)

    if run_submitted and sel:
        run_engine(sel)
        st.session_state.ran = True
        st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Stock list header ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:#1a1f2e; border:1px solid #2a3142; border-radius:14px; padding:16px 16px 8px 16px;">
      <div class="panel-header">
        <span class="panel-title">Selected Stocks</span>
        <span class="count-badge">{len(sel)}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for ticker in list(sel):
        c1, c2 = st.columns([1, 0.18], gap="small")
        with c1:
            display = ticker.replace(".SA", "")
            st.markdown(f"""
            <div class="stock-card">
              {logo_html(ticker)}
              <div>
                <div class="stock-ticker">{display}</div>
                <div class="stock-name">{STOCKS.get(ticker, "")}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("✕", key=f"rm_{ticker}"):
                sel.remove(ticker)
                st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("Clear all", use_container_width=True):
        st.session_state.selected_stocks = []
        st.rerun()

# ── RIGHT panel ───────────────────────────────────────────────────────────────
with right_col:
    tab_visao, tab_frontier = st.tabs(["Overview", "Efficient Frontier"])

    with tab_visao:
        if not sel:
            st.markdown("""
            <div class="empty-state">
              <div class="empty-title">Ready to analyze</div>
              <div class="empty-sub">Add stocks to visualize metrics, charts and insights about your portfolio.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="success-banner">
              {len(sel)} asset(s) loaded successfully!
            </div>
            """, unsafe_allow_html=True)

            weights_chart = "results/plots/weights_chart.png"
            if st.session_state.ran and os.path.exists(weights_chart):
                st.image(weights_chart, use_container_width=True)

    with tab_frontier:
        frontier_img = "results/plots/efficient_frontier.png"
        if st.session_state.ran and os.path.exists(frontier_img):
            st.image(frontier_img, use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-state">
              <div class="empty-title">No results yet</div>
              <div class="empty-sub">Select stocks and press Run to generate the Efficient Frontier.</div>
            </div>
            """, unsafe_allow_html=True)