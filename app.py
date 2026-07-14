import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px

from graph import hydro_graph


# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="HydroSphere AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────
#  Custom CSS – Premium Dark Theme
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/*
  BRAND PALETTE
  --cream:  #FFF9F2   (primary background)
  --peach:  #FFF9F2   (secondary / card bg)
  --orange: #FFF9F2   (accent / brand)
  --dark:   #2A1408   (primary text)
  --mid:    #7A4A30   (secondary text)
  --muted:  #B08060   (muted / labels)
*/

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 1.12rem;
}

.stApp {
    background: #FFF9F2;
    color: #2A1408;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; }

/* ── Hero Banner ── */
.hero-banner {
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.20);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -50%; left: -20%;
    width: 60%; height: 200%;
    background: radial-gradient(ellipse, rgba(196,82,26,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #C4521A, #E07040, #A03A10);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 1.25rem;
    color: #7A4A30;
    margin-top: 0.6rem;
    font-weight: 400;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(196,82,26,0.12);
    border: 1px solid rgba(196,82,26,0.40);
    color: #C4521A;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.3rem 0.85rem;
    border-radius: 50px;
    margin-bottom: 1rem;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2A1408;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(196,82,26,0.45), transparent);
    margin-left: 0.8rem;
}

/* ── Metric Cards ── */
.metric-card {
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.18);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    transition: border-color 0.2s, transform 0.2s;
}
.metric-card:hover {
    border-color: rgba(196,82,26,0.50);
    transform: translateY(-2px);
}
.metric-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #B08060;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.95rem;
    font-weight: 700;
    color: #2A1408;
    line-height: 1.1;
}
.metric-unit {
    font-size: 0.95rem;
    color: #7A4A30;
    font-weight: 400;
}

/* ── Data Panel ── */
.data-panel {
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.18);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    height: 100%;
}
.panel-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #C4521A;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.kv-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(196,82,26,0.15);
}
.kv-row:last-child { border-bottom: none; }
.kv-key {
    font-size: 0.98rem;
    color: #7A4A30;
    font-weight: 500;
}
.kv-val {
    font-size: 1.05rem;
    color: #2A1408;
    font-weight: 600;
}

/* ── Run Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #C4521A 0%, #A03A10 100%);
    color: #FBF0E6;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 2rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    width: 100%;
    transition: opacity 0.2s, transform 0.15s;
    cursor: pointer;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.90;
    transform: translateY(-1px);
}

/* ── Agent Timeline ── */
.agent-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.9rem 1.2rem;
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.18);
    border-left: 3px solid;
    border-radius: 10px;
    margin-bottom: 0.65rem;
    transition: border-color 0.2s;
}
.agent-icon { font-size: 1.3rem; flex-shrink: 0; }
.agent-name {
    font-size: 0.95rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}
.agent-desc {
    font-size: 0.95rem;
    color: #7A4A30;
    line-height: 1.5;
}

/* ── Risk Badge ── */
.risk-badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.risk-high   { background: rgba(196,82,26,0.15);  color: #C4521A; border: 1px solid rgba(196,82,26,0.40); }
.risk-medium { background: rgba(210,140,50,0.15); color: #C88020; border: 1px solid rgba(210,140,50,0.40); }
.risk-low    { background: rgba(100,160,80,0.15);  color: #5A9040; border: 1px solid rgba(100,160,80,0.40); }

/* ── Result Section ── */
.result-card {
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.25);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}
.result-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #C4521A;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Reasoning Box ── */
.reasoning-box {
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.22);
    border-left: 4px solid #C4521A;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    font-size: 1.08rem;
    color: #3A1A08;
    line-height: 1.8;
}

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,82,26,0.35), transparent);
    margin: 2rem 0;
}

/* ── Agent analysis cards ── */
.analysis-card {
    background: #FFE9CF;
    border: 1px solid rgba(196,82,26,0.18);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    height: 100%;
}
.analysis-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #C4521A;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.8rem;
}
.analysis-item {
    font-size: 0.88rem;
    color: #7A4A30;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.55rem 0 0.4rem;
    border-bottom: 1px solid rgba(196,82,26,0.15);
    line-height: 1.4;
}
.analysis-item:last-child { border-bottom: none; }
.analysis-item span {
    display: block;
    margin-top: 0.2rem;
    color: #2A1408;
    font-size: 1.0rem;
    font-weight: 500;
    text-transform: none;
    letter-spacing: 0;
    word-break: break-word;
    white-space: normal;
}

/* Streamlit table override */
.stDataFrame, .stTable { border-radius: 10px; overflow: hidden; }

thead tr th { background: rgba(196,82,26,0.10) !important; color: #C4521A !important; font-weight: 700 !important; }
tbody tr:hover td { background: rgba(196,82,26,0.05) !important; }

/* ── Landing Page Specific Styling ── */
.landing-header {
    border-bottom: 1px solid rgba(196,82,26,0.15);
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}
.landing-section {
    padding: 2rem 0;
    max-width: 900px;
    margin: 0 auto;
}
.landing-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #2A1408;
    margin-bottom: 1rem;
    text-align: center;
}
.landing-text {
    font-size: 1.25rem;
    color: #4A2511;
    line-height: 1.8;
    text-align: center;
}
.landing-feature-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
    margin-top: 2rem;
}
.landing-feature {
    padding: 1.5rem 0;
    border-left: 3px solid #C4521A;
    padding-left: 1.5rem;
    background: transparent;
}
.landing-feature-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #C4521A;
    margin-bottom: 0.6rem;
}
.landing-feature-desc {
    font-size: 1.05rem;
    color: #7A4A30;
    line-height: 1.6;
}

/* ── Mobile Responsive ── */
@media (max-width: 768px) {

    /* Streamlit layout columns stacked on mobile */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 1.2rem !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    /* Hide empty spacer columns on mobile */
    div[data-testid="column"]:not(:has(.element-container)) {
        display: none !important;
    }

    /* Center all buttons in columns on mobile */
    div[data-testid="column"] div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div[data-testid="column"] div[data-testid="stButton"] > button {
        width: auto !important;
    }

    /* Block container margins and padding */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    /* Navbar logo */
    .nav-title {
        font-size: 1.8rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
    }

    /* Hero */
    .hero-section-wrap {
        padding: 2rem 0.5rem 1.5rem !important;
    }
    .hero-title {
        font-size: 2.2rem !important;
        margin-bottom: 1.0rem !important;
    }
    .hero-section-wrap p {
        font-size: 1.05rem !important;
        line-height: 1.5 !important;
        margin-bottom: 1.2rem !important;
        text-align: center !important;
    }

    /* Problems & Layout Sections */
    .landing-section {
        padding: 1.5rem 0 !important;
    }
    .landing-title {
        font-size: 1.7rem !important;
        margin-bottom: 0.8rem !important;
    }
    .landing-how-it-works h2 {
        font-size: 1.7rem !important;
    }
    .landing-text {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    .landing-text-left {
        font-size: 1.0rem !important;
        line-height: 1.6 !important;
    }

    /* Feature Grid stack */
    .landing-feature-grid {
        grid-template-columns: 1fr !important;
        gap: 1.2rem !important;
        margin-top: 1rem !important;
    }
    .landing-feature {
        padding: 1rem 0 1rem 1.2rem !important;
    }
    .landing-feature-title {
        font-size: 1.15rem !important;
    }
    .landing-feature-desc {
        font-size: 0.95rem !important;
    }

    /* Dashboard details */
    .scenario-context {
        font-size: 1.0rem !important;
        line-height: 1.5 !important;
        margin-bottom: 1.2rem !important;
    }

    /* Metric + data cards fill full width */
    .metric-card, .data-panel, .analysis-card, .result-card, .reasoning-box {
        width: 100% !important;
        box-sizing: border-box;
    }

    /* Tighten card padding */
    .metric-card  { padding: 0.9rem 1rem; }
    .data-panel   { padding: 1rem; }
    .result-card  { padding: 1.2rem; }
    .analysis-card{ padding: 1rem; }

    /* Metric value scales down */
    .metric-value { font-size: 1.3rem; }

    /* Section headers */
    .section-header { font-size: 0.95rem; }

    /* KV rows wrap on tiny screens */
    .kv-row {
        flex-wrap: wrap;
        gap: 0.25rem;
    }
    .kv-key, .kv-val { font-size: 0.85rem; }

    /* Analysis items */
    .analysis-item span { font-size: 0.82rem; }

    /* Gauge chart: let it shrink */
    .js-plotly-plot { max-width: 100% !important; }
}

@media (max-width: 480px) {
    .hero-title   { font-size: 1.6rem !important; }
    .hero-badge   { font-size: 0.65rem; }
    .metric-value { font-size: 1.1rem; }
    .result-title { font-size: 0.85rem; }
}

</style>
""", unsafe_allow_html=True)



# ─────────────────────────────────────────────
#  Load Data
# ─────────────────────────────────────────────

with open("data/mock_data.json") as f:
    data = json.load(f)


# ─────────────────────────────────────────────
#  Page Navigation
# ─────────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "previous_page" not in st.session_state:
    st.session_state.previous_page = st.session_state.page

page_changed = False
if st.session_state.page != st.session_state.previous_page:
    page_changed = True
    st.session_state.previous_page = st.session_state.page

if page_changed:
    st.markdown("""
        <svg onload="
            var mainContainer = window.parent.document.querySelector('section.main') || document.querySelector('section.main');
            if (mainContainer) {
                mainContainer.scrollTo({ top: 0, behavior: 'instant' });
            }
        " style="display:none;"></svg>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════════════════════════════

if st.session_state.page == "landing":

    # ── Navbar ──
    nav_col1, nav_col2 = st.columns([5, 1.2])
    with nav_col1:
        st.markdown('<div class="nav-title" style="font-size: 2.2rem; font-weight: 800; color: #C4521A; font-family: \'Inter\', sans-serif;">HydroSphere AI</div>', unsafe_allow_html=True)
    with nav_col2:
        if st.button("Test Product", key="nav_test_product"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown('<div class="landing-header"></div>', unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section-wrap" style="text-align:center; padding: 4rem 1rem 3rem;">
        <div class="hero-badge">Multi-Agent AI Platform</div>
        <h1 class="hero-title" style="font-size:3.6rem; margin-bottom:1.5rem;">Water Intelligence System</h1>
        <p style="font-size:1.3rem; color:#7A4A30; max-width:800px; margin:0 auto 1.5rem; line-height:1.7;">
            Six specialized AI agents working in concert to analyze weather conditions,
            assess risk, and produce transparent, explainable allocation decisions, in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:2rem"></div>', unsafe_allow_html=True)

    # ── Problem Statement ─────────────────────────────────────────
    st.markdown("""
    <div class="landing-section">
        <h2 class="landing-title">The Challenge in Water Management</h2>
        <p class="landing-text">
            Reservoir operations teams must consolidate weather forecasts, water demand data, 
            and risk indicators from multiple siloed sources under intense time pressure. 
            Traditional workflows are slow, lack explainability, and increase the risk of misallocation. 
            HydroSphere AI automates and accelerates this process with a multi-agent system that 
            delivers clear, transparent, and reasoned recommendations in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:2rem"></div>', unsafe_allow_html=True)

    # ── 6-Agent Pipeline ──────────────────────────────────────────
    st.markdown('<div class="section-header" style="font-size: 1.25rem;">The 6-Agent Pipeline</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="landing-feature-grid">
        <div class="landing-feature">
            <div class="landing-feature-title">Weather Intelligence</div>
            <div class="landing-feature-desc">Analyzes rainfall forecasts, temperature, and evaporation risk to assess atmospheric water stress.</div>
        </div>
        <div class="landing-feature">
            <div class="landing-feature-title">Reservoir Intelligence</div>
            <div class="landing-feature-desc">Evaluates current storage levels, inflow/outflow balance, and capacity trends.</div>
        </div>
        <div class="landing-feature">
            <div class="landing-feature-title">Agriculture Analysis</div>
            <div class="landing-feature-desc">Calculates crop water requirements and irrigation priority based on soil moisture and crop type.</div>
        </div>
        <div class="landing-feature">
            <div class="landing-feature-title">Urban Demand</div>
            <div class="landing-feature-desc">Assesses domestic and industrial water consumption to determine urban supply needs.</div>
        </div>
        <div class="landing-feature">
            <div class="landing-feature-title">Risk Assessment</div>
            <div class="landing-feature-desc">Synthesizes all agent findings to identify drought, flood, and supply-chain risks.</div>
        </div>
        <div class="landing-feature">
            <div class="landing-feature-title">Decision & Allocation</div>
            <div class="landing-feature-desc">Produces an explainable water allocation recommendation balancing all competing demands.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:4rem"></div>', unsafe_allow_html=True)

    # ── How It Works ─────────────────────────────────────────────
    st.markdown("""
    <div class="landing-section landing-how-it-works" style="max-width: 900px; padding: 2rem 0; border-top: 1px solid rgba(196,82,26,0.15);">
        <h2 class="landing-title" style="font-size: 2rem;">How It Works</h2>
        <p class="landing-text landing-text-left" style="font-size: 1.1rem; color: #2A1408; text-align: left; line-height: 1.8;">
            HydroSphere AI orchestrates six specialized AI agents using <strong>LangGraph</strong>.
            Each agent analyzes a specific domain in sequence, weather, reservoir status, agricultural demand,
            urban demand, and risk, before passing its findings to the <strong>Decision Agent</strong>,
            which synthesizes all inputs into a transparent, explainable water allocation strategy.
            Every decision includes step-by-step AI reasoning so operators can understand, verify, and trust the output.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA Button ───────────────────────────────────────────────
    st.markdown('<div style="margin-top:2rem"></div>', unsafe_allow_html=True)
    _, cta_col, _ = st.columns([1, 1.5, 1])
    with cta_col:
        if st.button("Test the Product →", key="go_to_dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown('<div style="margin-top:4rem; text-align:center; color:#B08060; font-size:0.85rem;">Powered by HydroSphere AI &middot; Multi-Agent LangGraph Pipeline &middot; IBM MVP</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
#  DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════════

elif st.session_state.page == "dashboard":

    # ── Navbar ──
    nav_col1, nav_col2 = st.columns([5, 1.2])
    with nav_col1:
        st.markdown('<div class="nav-title" style="font-size: 2.2rem; font-weight: 800; color: #C4521A; font-family: \'Inter\', sans-serif;">HydroSphere AI</div>', unsafe_allow_html=True)
    with nav_col2:
        if st.button("← Back to Overview", key="back_to_landing"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown('<div class="landing-header"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    #  Hero Banner
    # ─────────────────────────────────────────────

    

    # ── Scenario Context ──
    st.markdown("""
    <div class="scenario-context" style="font-size: 1.15rem; line-height: 1.7; color: #4A2511; margin-bottom: 2rem;">
        <strong>Live Demonstration Scenario:</strong> This dataset represents a region experiencing below-average rainfall, high temperatures, declining reservoir levels (38% capacity), and increasing agricultural and urban water demand. HydroSphere AI analyzes these conditions to determine an optimal and explainable water allocation strategy while balancing essential urban supply, agricultural irrigation, and environmental sustainability.
    </div>
    """, unsafe_allow_html=True)




    # ─────────────────────────────────────────────
    #  Top KPI Strip
    # ─────────────────────────────────────────────

    reservoir = data["reservoir"]
    storage_pct = (reservoir["current_storage"] / reservoir["capacity"]) * 100
    net_flow = reservoir["daily_inflow"] - reservoir["daily_outflow"]

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Temperature</div>
            <div class="metric-value">{data["weather"]["temperature"]}<span class="metric-unit"> °C</span></div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Reservoir Level</div>
            <div class="metric-value">{storage_pct:.0f}<span class="metric-unit"> %</span></div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Crop Area</div>
            <div class="metric-value">{data["agriculture"]["area"]:,}<span class="metric-unit"> ha</span></div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Population</div>
            <div class="metric-value">{data["urban"]["population"] // 1_000_000:.1f}<span class="metric-unit"> M</span></div>
        </div>""", unsafe_allow_html=True)

    flow_color  = "#5A9040" if net_flow >= 0 else "#C4521A"
    flow_symbol = "▲" if net_flow >= 0 else "▼"
    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Net Daily Flow</div>
            <div class="metric-value" style="color:{flow_color}">{flow_symbol} {abs(net_flow)}<span class="metric-unit"> L/d</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Run Button ──
    _, btn_col, _ = st.columns([1.5, 2, 1.5])
    with btn_col:
        run = st.button("Run Water Intelligence Simulation", key="run_sim", use_container_width=True)
        if run:
            st.markdown("""
            <div style="text-align: center; color: #C4521A; font-weight: 700; font-size: 1.15rem; margin-top: 1rem; animation: bounce 2s infinite;">
                Scroll Down for Results & Agent Pipeline 👇
            </div>
            <style>
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-6px); }
                60% { transform: translateY(-3px); }
            }
            </style>
            """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)



    # ─────────────────────────────────────────────
    #  Input Data Panels
    # ─────────────────────────────────────────────

    st.markdown('<div class="section-header">System Input Data</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""<div class="data-panel">
        <div class="panel-title">Weather</div>""", unsafe_allow_html=True)
        for k, v in data["weather"].items():
            label = k.replace("_", " ").title()
            st.markdown(f"""<div class="kv-row"><span class="kv-key">{label}</span><span class="kv-val">{v}</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="data-panel">
        <div class="panel-title">Reservoir</div>""", unsafe_allow_html=True)
        for k, v in data["reservoir"].items():
            label = k.replace("_", " ").title()
            unit = " L" if k in ["capacity", "current_storage"] else (" L/d" if "flow" in k else "")
            st.markdown(f"""<div class="kv-row"><span class="kv-key">{label}</span><span class="kv-val">{v}{unit}</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class="data-panel">
        <div class="panel-title">Agriculture</div>""", unsafe_allow_html=True)
        for k, v in data["agriculture"].items():
            label = k.replace("_", " ").title()
            unit = " ha" if k == "area" else ("%" if k == "soil_moisture" else "")
            st.markdown(f"""<div class="kv-row"><span class="kv-key">{label}</span><span class="kv-val">{v}{unit}</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("""<div class="data-panel">
        <div class="panel-title">Urban</div>""", unsafe_allow_html=True)
        for k, v in data["urban"].items():
            label = k.replace("_", " ").title()
            unit = " L/p/d" if "consumption" in k else (" %" if "usage" in k else "")
            display = f"{v:,}" if isinstance(v, int) else v
            st.markdown(f"""<div class="kv-row"><span class="kv-key">{label}</span><span class="kv-val">{display}{unit}</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


    # ─────────────────────────────────────────────
    #  Reservoir Gauge Chart
    # ─────────────────────────────────────────────

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=storage_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={"text": "Reservoir Storage Level", "font": {"size": 18, "color": "#7A4A30", "family": "Inter"}},
        number={"suffix": "%", "font": {"size": 36, "color": "#2A1408", "family": "Inter"}},
        delta={"reference": 60, "increasing": {"color": "#5A9040"}, "decreasing": {"color": "#C4521A"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#B08060", "tickfont": {"color": "#7A4A30"}},
            "bar": {"color": "#C4521A", "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30],  "color": "rgba(196,82,26,0.20)"},
                {"range": [30, 60], "color": "rgba(196,82,26,0.10)"},
                {"range": [60, 100],"color": "rgba(90,144,64,0.12)"},
            ],
            "threshold": {
                "line": {"color": "#B06020", "width": 3},
                "thickness": 0.75,
                "value": 40,
            },
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#7A4A30"},
        height=280,
        margin=dict(t=40, b=10, l=40, r=40),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)




    # ─────────────────────────────────────────────
    #  Simulation Results
    # ─────────────────────────────────────────────

    if run:

        initial_state = {
            "weather_data":       data["weather"],
            "reservoir_data":     data["reservoir"],
            "agriculture_data":   data["agriculture"],
            "urban_data":         data["urban"],
            "weather_analysis":   {},
            "reservoir_analysis": {},
            "agriculture_analysis": {},
            "urban_analysis":     {},
            "risk_analysis":      {},
            "final_decision":     {},
        }

        _AGENT_LABEL = {
            "weather":     "Weather Intelligence",
            "reservoir":   "Reservoir Intelligence",
            "agriculture": "Agriculture Analysis",
            "urban":       "Urban Demand",
            "risk":        "Risk Assessment",
            "decision":    "Decision & Allocation",
        }

        result = {**initial_state}

        with st.status("Running AI Agent Pipeline...", expanded=True) as _status:
            for _chunk in hydro_graph.stream(initial_state):
                for _node, _output in _chunk.items():
                    _label = _AGENT_LABEL.get(_node, _node)
                    if _node == "decision":
                        st.write("Finalizing output — Decision & Allocation running...")
                    else:
                        st.write(f"⚙️ Running: {_label}")
                    result.update(_output)
                    st.write(f"✅ {_label} complete")
            _status.update(label="All 6 agents completed successfully!", state="complete", expanded=False)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Simulation Results</div>', unsafe_allow_html=True)

        st.success("✅ All 6 AI agents completed analysis successfully", icon=None)

        decision       = result["final_decision"]
        risk           = result.get("risk_analysis", {})
        reservoir_anal = result.get("reservoir_analysis", {})
        weather_anal   = result.get("weather_analysis", {})

        # ── Agent Analysis Summary Cards ──
        st.markdown("#### Agent Analysis Outputs")

        agri_anal  = result.get("agriculture_analysis", {})
        urban_anal = result.get("urban_analysis", {})

        def _clean_value(v) -> str:
            import re, ast
            if isinstance(v, dict):
                parts = []
                for dk, dv in list(v.items())[:4]:
                    parts.append(f"{dk.replace('_', ' ').title()}: {_clean_value(dv)}")
                return "; ".join(parts)
            if isinstance(v, list):
                cleaned = [_clean_value(i) for i in v[:3]]
                return ". ".join(cleaned)
            text = str(v).strip()
            if text.startswith(("[", "{")):
                try:
                    parsed = ast.literal_eval(text)
                    return _clean_value(parsed)
                except Exception:
                    pass
            text = re.sub(r"^[\['\"]+|[\]'\",]+$", "", text).strip()
            if re.match(r'^[a-z][a-z0-9_]+$', text):
                text = text.replace("_", " ").capitalize()
            return text

        def render_analysis_card(title, analysis):
            import json as _json
            rows_html = ""

            def _add_row(key, val):
                nonlocal rows_html
                label   = key.replace("_", " ").title()
                display = _clean_value(val)
                rows_html += f'<div class="analysis-item">{label}<br><span>{display}</span></div>'

            if isinstance(analysis, dict):
                for k, v in analysis.items():
                    _add_row(k, v)
            elif isinstance(analysis, str):
                clean = analysis.strip().strip("```json").strip("```").strip()
                try:
                    parsed = _json.loads(clean)
                    if isinstance(parsed, dict):
                        for k, v in parsed.items():
                            _add_row(k, v)
                    else:
                        rows_html = f'<div class="analysis-item"><span>{_clean_value(parsed)}</span></div>'
                except Exception:
                    clean = clean.replace("_", " ").replace("{", "").replace("}", "").replace("[", "").replace("]", "")
                    rows_html = f'<div class="analysis-item"><span>{clean[:400]}</span></div>'
            else:
                rows_html = '<div class="analysis-item"><span>No data returned.</span></div>'

            return f'<div class="analysis-card"><div class="analysis-card-title">{title}</div>{rows_html}</div>'

        ac1, ac2, ac3, ac4 = st.columns(4)
        with ac1:
            st.markdown(render_analysis_card("Weather",     weather_anal),   unsafe_allow_html=True)
        with ac2:
            st.markdown(render_analysis_card("Reservoir",   reservoir_anal), unsafe_allow_html=True)
        with ac3:
            st.markdown(render_analysis_card("Agriculture", agri_anal),      unsafe_allow_html=True)
        with ac4:
            st.markdown(render_analysis_card("Urban",       urban_anal),     unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # ── Risk Assessment ──────────────────────────────────────
        st.markdown("#### Risk Assessment")

        risk_col1, risk_col2 = st.columns([1, 2])

        with risk_col1:
            severity   = str(risk.get("severity", "Unknown")).lower()
            risk_class = "risk-high" if "high" in severity or "critical" in severity else \
                         "risk-medium" if "medium" in severity or "moderate" in severity else "risk-low"
            raw_rt = risk.get("risk_type", risk.get("type", "N/A"))
            if isinstance(raw_rt, dict):
                risk_type = ", ".join(f"{k.replace('_',' ').title()}: {v}" for k, v in raw_rt.items())
            elif isinstance(raw_rt, list):
                risk_type = ", ".join(str(i).replace("_", " ").title() for i in raw_rt)
            else:
                risk_type = str(raw_rt).replace("_", " ").title()
            st.markdown(f"""
            <div class="result-card" style="text-align:center; padding: 2rem;">
                <div style="font-size:0.75rem; color:#7A4A30; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem">Risk Type</div>
                <div style="font-size:1.3rem; font-weight:800; color:#000000; margin-bottom:1rem">{risk_type}</div>
                <div class="risk-badge {risk_class}">{risk.get("severity", "Unknown")}</div>
            </div>""", unsafe_allow_html=True)

        with risk_col2:
            raw_rec = risk.get("recommendation", "No recommendation available.")
            if isinstance(raw_rec, dict):
                recommendation = " ".join(f"{k.replace('_',' ').title()}: {v}." for k, v in raw_rec.items())
            elif isinstance(raw_rec, list):
                recommendation = " ".join(str(i).strip("'\"") for i in raw_rec)
            else:
                import ast as _ast
                rec_str = str(raw_rec).strip()
                if rec_str.startswith(("{", "[")):
                    try:
                        parsed = _ast.literal_eval(rec_str)
                        if isinstance(parsed, dict):
                            recommendation = " ".join(f"{k.replace('_',' ').title()}: {v}." for k, v in parsed.items())
                        elif isinstance(parsed, list):
                            recommendation = " ".join(str(i).strip("'\"") for i in parsed)
                        else:
                            recommendation = str(parsed)
                    except Exception:
                        recommendation = rec_str.replace("_", " ").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("'", "")
                else:
                    recommendation = rec_str
            import re
            
            # Format recommendation if it has numbered list items like (1), (2), etc.
            rec_html = ""
            pattern = r'\s*\((\d+)\)\s*'
            parts = re.split(pattern, recommendation)
            
            if len(parts) <= 1:
                rec_html = f'<div style="color: #3A1A08; font-size: 1.0rem; line-height: 1.6;">{recommendation}</div>'
            else:
                intro = parts[0].strip()
                if intro:
                    rec_html += f'<div style="margin-bottom: 0.8rem; font-weight: 600; color: #3A1A08; font-size: 1.05rem;">{intro}</div>'
                
                rec_html += '<ul style="list-style-type: none; padding-left: 0; margin: 0; display: flex; flex-direction: column; gap: 0.8rem;">'
                for i in range(1, len(parts), 2):
                    num = parts[i]
                    content = parts[i+1].strip()
                    rec_html += (
                        f'<li style="display: flex; align-items: flex-start; gap: 0.8rem; line-height: 1.6;">'
                        f'<span style="display: inline-flex; align-items: center; justify-content: center; background: #C4521A; color: white; font-weight: 700; border-radius: 50%; min-width: 1.5rem; height: 1.5rem; font-size: 0.85rem; margin-top: 0.15rem; flex-shrink: 0;">{num}</span>'
                        f'<span style="color: #3A1A08; font-size: 1.0rem;">{content}</span>'
                        f'</li>'
                    )
                rec_html += '</ul>'

            st.markdown(
                f'<div class="result-card" style="height:100%">'
                f'<div class="result-title">Risk Recommendation</div>'
                f'<div class="reasoning-box" style="border-left-color:#C4521A;">{rec_html}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div style="margin-top:1.5rem"></div>', unsafe_allow_html=True)

        # ── Final Allocation ─────────────────────────────────────
        st.markdown("#### Final Water Allocation")

        alloc_col1, alloc_col2 = st.columns([1, 1])

        def _to_pct(val):
            v = float(val) if val else 0
            return round(v * 100 if v <= 1.0 else v)

        agri_pct  = _to_pct(decision.get("agriculture_allocation", 0))
        urban_pct = _to_pct(decision.get("urban_allocation",       0))
        env_pct   = _to_pct(decision.get("environmental_reserve",  0))

        with alloc_col1:
            fig_pie = go.Figure(go.Pie(
                labels=["Agriculture", "Urban", "Environmental Reserve"],
                values=[agri_pct, urban_pct, env_pct],
                hole=0.55,
                marker=dict(
                    colors=["#C4521A", "#7A4A30", "#D4A882"],
                    line=dict(color="#FBF0E6", width=3)
                ),
                textfont=dict(family="Inter", size=13, color="white"),
                hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#7A4A30"),
                legend=dict(
                    font=dict(color="#7A4A30", size=13),
                    bgcolor="rgba(0,0,0,0)",
                    orientation="h",
                    yanchor="bottom", y=-0.15,
                    xanchor="center", x=0.5,
                ),
                margin=dict(t=20, b=30, l=20, r=20),
                height=300,
                annotations=[dict(
                    text="<b>Total</b><br>100%",
                    x=0.5, y=0.5,
                    font=dict(size=14, color="#2A1408", family="Inter"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with alloc_col2:
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=["Agriculture", "Urban", "Environment"],
                y=[agri_pct, urban_pct, env_pct],
                marker=dict(
                    color=["#C4521A", "#7A4A30", "#D4A882"],
                    line=dict(width=0),
                    cornerradius=8,
                ),
                text=[f"{v}%" for v in [agri_pct, urban_pct, env_pct]],
                textposition="outside",
                textfont=dict(color="#2A1408", size=15, family="Inter"),
                hovertemplate="<b>%{x}</b>: %{y}%<extra></extra>",
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(
                    range=[0, max(agri_pct, urban_pct, env_pct) * 1.25],
                    showgrid=True,
                    gridcolor="rgba(196,82,26,0.12)",
                    tickfont=dict(color="#B08060"),
                    title=dict(text="Allocation %", font=dict(color="#B08060")),
                ),
                xaxis=dict(tickfont=dict(color="#7A4A30", size=12), showline=False),
                margin=dict(t=20, b=20, l=10, r=10),
                height=300,
                bargap=0.35,
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Calculate Liter-based distribution
        total_outflow = reservoir.get("daily_outflow", 0)
        agri_liters = (agri_pct / 100.0) * total_outflow
        urban_liters = (urban_pct / 100.0) * total_outflow
        env_liters = (env_pct / 100.0) * total_outflow

        # ── Allocation Metric Cards ──
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card" style="border-color: rgba(196,82,26,0.5); text-align:center; padding:1.4rem;">
                <div class="metric-label" style="color:#C4521A">Agriculture</div>
                <div class="metric-value" style="color:#C4521A; font-size:2.5rem">{agri_pct}%</div>
                <div style="font-size:1.15rem; color:#C4521A; font-weight:600; margin-top:0.4rem; opacity:0.9;">({agri_liters:.1f} L/d)</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card" style="border-color: rgba(122,74,48,0.5); text-align:center; padding:1.4rem;">
                <div class="metric-label" style="color:#7A4A30">Urban</div>
                <div class="metric-value" style="color:#7A4A30; font-size:2.5rem">{urban_pct}%</div>
                <div style="font-size:1.15rem; color:#7A4A30; font-weight:600; margin-top:0.4rem; opacity:0.9;">({urban_liters:.1f} L/d)</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card" style="border-color: rgba(212,168,130,0.7); text-align:center; padding:1.4rem;">
                <div class="metric-label" style="color:#B08060">Environmental Reserve</div>
                <div class="metric-value" style="color:#B08060; font-size:2.5rem">{env_pct}%</div>
                <div style="font-size:1.15rem; color:#B08060; font-weight:600; margin-top:0.4rem; opacity:0.9;">({env_liters:.1f} L/d)</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.5rem"></div>', unsafe_allow_html=True)

        # ── AI Reasoning ──
        st.markdown("#### AI Decision Reasoning")
        
        reasoning_data = decision.get("reasoning", "No reasoning provided.")
        reasoning_html = ""
        
        # Try to parse string to dict if it is a string representation of a JSON/dict
        if isinstance(reasoning_data, str):
            reasoning_data = reasoning_data.strip()
            if reasoning_data.startswith("{"):
                import json as _json
                try:
                    reasoning_data = _json.loads(reasoning_data)
                except Exception:
                    import ast as _ast
                    try:
                        reasoning_data = _ast.literal_eval(reasoning_data)
                    except Exception:
                        pass
                        
        if isinstance(reasoning_data, dict):
            reasoning_html = '<div style="display: flex; flex-direction: column; gap: 1.2rem;">'
            items = list(reasoning_data.items())
            for idx, (r_key, r_val) in enumerate(items):
                r_title = r_key.replace("_", " ").title()
                is_last = (idx == len(items) - 1)
                border_style = "" if is_last else "border-bottom: 1px solid rgba(196,82,26,0.15); padding-bottom: 0.8rem;"
                reasoning_html += (
                    f'<div style="{border_style}">'
                    f'<div style="font-weight: 700; color: #C4521A; font-size: 1.05rem; margin-bottom: 0.3rem;">{r_title}</div>'
                    f'<div style="color: #3A1A08; font-size: 1.0rem; line-height: 1.6;">{r_val}</div>'
                    f'</div>'
                )
            reasoning_html += '</div>'
        else:
            reasoning_html = f'<div style="color: #3A1A08; font-size: 1.0rem; line-height: 1.6;">{reasoning_data}</div>'

        st.markdown(
            f'<div class="reasoning-box">{reasoning_html}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div style="margin-top:2rem; text-align:center; color:#B08060; font-size:0.78rem;">Powered by HydroSphere AI · Multi-Agent LangGraph Pipeline · IBM MVP</div>', unsafe_allow_html=True)
