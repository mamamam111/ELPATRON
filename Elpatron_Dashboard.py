import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ECOS | EcoBat Indonesia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Force sidebar always visible
st.markdown("""
<style>
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: flex !important; visibility: visible !important; }
</style>
""", unsafe_allow_html=True)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&family=Bebas+Neue&display=swap');

:root {
    --bg-primary:   #05080F;
    --bg-card:      #0C1220;
    --bg-card-h:    #111B2E;
    --border:       #1A2840;
    --border-acc:   #1E3A5F;
    --green:        #00E5A0;
    --blue:         #0EA5E9;
    --orange:       #F97316;
    --yellow:       #EAB308;
    --red:          #EF4444;
    --txt:          #F0F4F8;
    --txt2:         #8CA0BB;
    --txt3:         #4A6080;
}

html, body, .stApp { background-color: var(--bg-primary) !important; font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

section[data-testid="stSidebar"] {
    background: #080D18 !important;
    border-right: 1px solid var(--border) !important;
    width: 265px !important;
}

.main .block-container { padding: 2rem 2.5rem 3rem 2.5rem; max-width: 1400px; }

/* Page Header */
.page-header { margin-bottom: 1.8rem; }
.page-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: var(--green);
    background: rgba(0,229,160,0.07);
    border: 1px solid rgba(0,229,160,0.18);
    padding: 3px 10px;
    border-radius: 3px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.page-header h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3rem !important;
    color: var(--txt) !important;
    letter-spacing: 0.04em;
    margin: 0 !important;
    line-height: 1.05;
}
.page-header p { color: var(--txt2) !important; font-size: 0.95rem; margin-top: 0.5rem; font-weight: 300; }

/* KPI Cards */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 16px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.kpi-card.green::before  { background: var(--green); }
.kpi-card.blue::before   { background: var(--blue); }
.kpi-card.orange::before { background: var(--orange); }
.kpi-card.yellow::before { background: var(--yellow); }
.kpi-card.red::before    { background: var(--red); }
.kpi-label { font-size: 0.68rem; color: var(--txt3); text-transform: uppercase; letter-spacing: 0.1em; font-family: 'Space Mono', monospace; margin-bottom: 7px; }
.kpi-value { font-size: 1.75rem; font-weight: 700; color: var(--txt); line-height: 1; margin-bottom: 5px; }
.kpi-value.green  { color: var(--green); }
.kpi-value.blue   { color: var(--blue); }
.kpi-value.orange { color: var(--orange); }
.kpi-value.yellow { color: var(--yellow); }
.kpi-value.red    { color: var(--red); }
.kpi-sub { font-size: 0.75rem; color: var(--txt3); }

/* Section title */
.sec-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.67rem;
    color: var(--txt3);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    border-left: 3px solid var(--green);
    padding-left: 10px;
    margin: 1.8rem 0 1rem 0;
}

/* Insight box */
.insight-box {
    background: rgba(0,229,160,0.05);
    border: 1px solid rgba(0,229,160,0.15);
    border-left: 3px solid var(--green);
    border-radius: 6px;
    padding: 12px 16px;
    margin-top: 10px;
}
.insight-box .ins-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--green);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 6px;
}
.insight-box p { color: var(--txt2) !important; font-size: 0.82rem !important; margin: 0 !important; line-height: 1.6; }
.insight-box ul { margin: 4px 0 0 0; padding-left: 16px; }
.insight-box li { color: var(--txt2) !important; font-size: 0.82rem !important; line-height: 1.7; }

/* Info card */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    height: 100%;
}
.info-card.p1 { border-top: 3px solid var(--green); }
.info-card.p2 { border-top: 3px solid var(--blue); }
.info-card.p3 { border-top: 3px solid var(--orange); }
.card-tag { font-family: 'Space Mono', monospace; font-size: 0.66rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 7px; }
.card-tag.p1 { color: var(--green); }
.card-tag.p2 { color: var(--blue); }
.card-tag.p3 { color: var(--orange); }
.info-card h3 { color: var(--txt) !important; font-size: 1rem !important; font-weight: 600 !important; margin: 0 0 10px 0 !important; }
.info-card p, .info-card li { color: var(--txt2) !important; font-size: 0.855rem; line-height: 1.6; }

/* Risk badge */
.badge { display: inline-block; font-family: 'Space Mono', monospace; font-size: 0.62rem; font-weight: 700; padding: 2px 8px; border-radius: 3px; letter-spacing: 0.08em; text-transform: uppercase; }
.badge.extreme { background: rgba(239,68,68,0.12);  color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
.badge.high    { background: rgba(249,115,22,0.12); color: #F97316; border: 1px solid rgba(249,115,22,0.3); }
.badge.medium  { background: rgba(234,179,8,0.12);  color: #EAB308; border: 1px solid rgba(234,179,8,0.3); }
.badge.low     { background: rgba(34,197,94,0.12);  color: #22C55E; border: 1px solid rgba(34,197,94,0.3); }

/* Risk row */
.risk-row { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 13px 16px; margin: 7px 0; }
.risk-row:hover { border-color: var(--border-acc); }
.risk-name { font-weight: 600; color: var(--txt); font-size: 0.88rem; margin: 5px 0 4px; }
.risk-mit  { font-size: 0.79rem; color: var(--txt2); }

/* Step card */
.step-card { display: flex; gap: 14px; align-items: flex-start; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 14px; margin: 7px 0; }
.step-num { font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; line-height: 1; min-width: 36px; color: var(--green); }
.step-content h4 { margin: 0 0 3px 0 !important; color: var(--txt) !important; font-size: 0.9rem !important; }
.step-content p  { margin: 0 !important; color: var(--txt2) !important; font-size: 0.81rem !important; }

/* Grade card */
.grade-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; text-align: center; }
.grade-letter { font-family: 'Bebas Neue', sans-serif; font-size: 4.5rem; line-height: 1; margin-bottom: 6px; }

/* Divider */
.divider { height: 1px; background: var(--border); margin: 1.8rem 0; }

/* Sidebar brand */
.sb-brand { padding: 18px 16px 12px; border-bottom: 1px solid var(--border); margin-bottom: 10px; }
.sb-name  { font-family: 'Bebas Neue', sans-serif; font-size: 1.75rem; color: var(--green); letter-spacing: 0.08em; margin: 0; }
.sb-sub   { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: var(--txt3); letter-spacing: 0.12em; text-transform: uppercase; }

/* Custom alert */
.c-alert { background: rgba(14,165,233,0.07); border: 1px solid rgba(14,165,233,0.2); border-radius: 7px; padding: 12px 16px; color: var(--txt2); font-size: 0.84rem; margin-top: 10px; }

/* Stat row inside card */
.stat-row { display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid var(--border); }
.stat-label { color: var(--txt2); font-size: 0.79rem; }
.stat-value { font-weight: 600; font-size: 0.84rem; color: var(--txt); }
.stat-value.accent { color: var(--green); }
.stat-value.warn   { color: var(--orange); }

.stSlider label, .stSelectbox label, .stMultiSelect label { color: var(--txt2) !important; font-size: 0.84rem !important; }
h2, h3 { color: var(--txt) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Plot defaults ──────────────────────────────────────────────────────────────
BG   = "#0C1220"
FONT = "#F0F4F8"
GRID = "#1A2840"
G = "#00E5A0"; B = "#0EA5E9"; O = "#F97316"; Y = "#EAB308"; R = "#EF4444"

def layout(title="", h=380):
    return dict(
        plot_bgcolor=BG, paper_bgcolor=BG,
        font=dict(color=FONT, family="DM Sans"),
        title=dict(text=title, font=dict(size=13, color=FONT), x=0),
        height=h,
        margin=dict(l=12, r=12, t=40 if title else 18, b=12),
        legend=dict(bgcolor=BG, bordercolor=GRID, borderwidth=1),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
    )

# ─── Helpers ───────────────────────────────────────────────────────────────────
def kpi(items):
    cols = st.columns(len(items))
    for col, (val, label, sub, clr) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="kpi-card {clr}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value {clr}">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

def sec(title):
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)

def div():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def insight(bullets: list, title="Key Insight"):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    st.markdown(f"""
    <div class="insight-box">
        <div class="ins-title">💡 {title}</div>
        <ul>{items}</ul>
    </div>""", unsafe_allow_html=True)

def stat(label, val, cls=""):
    st.markdown(f"""
    <div class="stat-row">
        <span class="stat-label">{label}</span>
        <span class="stat-value {cls}">{val}</span>
    </div>""", unsafe_allow_html=True)

# ─── Data ──────────────────────────────────────────────────────────────────────
years       = [2022, 2023, 2024, 2025]
sales_vol   = [10_327, 25_730, 43_180, 94_250]
revenue_h   = [82.6, 122.7, 329.9, 678.6]
margin_h    = [31.25, 33.33, 36.00, 38.89]

baas_yrs    = [2025, 2026, 2027, 2028, 2029]
new_cust    = [28_275, 53_016, 80_996, 119_653, 161_072]
sub_rev     = [118.8, 341.4, 681.6, 1_184.1, 1_860.6]
nb_rev      = [142.5, 267.2, 408.2, 603.1, 811.8]
cum_baas    = [28_275, 81_291, 162_287, 281_940, 443_012]

eol_yrs     = [2026, 2027, 2028, 2029, 2030, 2031, 2032]
eol_sales   = [1_200, 2_400, 5_000, 15_400, 22_000, 45_000, 78_000]
eol_cap     = [116, 307, 1_300, 9_675, 9_675, 24_310, 49_725]

sp_yrs      = [2025, 2026, 2027, 2028, 2029]
sp_stations = [150, 188, 235, 294, 368]
sp_units    = [21_600, 21_859, 33_840, 21_178, 52_992]
sp_cumul    = [21_600, 43_459, 77_299, 98_477, 109_037]
sp_opex     = [6.15, 5.66, 5.70, 5.76, 5.83]

p3_yrs      = [2030, 2031, 2032, 2033]
ga_u        = [1_859, 4_168, 6_885, 10_421]
gb_u        = [2_788, 6_252, 10_480, 15_789]
gc_u        = [1_549, 3_421, 5_789, 9_716]

# SPKLU geographic data (source: PLN 2024, via Casebook 2026 / Appendix 7)
spklu_df = pd.DataFrame({
    "Region":       ["DKI Jakarta","West Java","Central Java – DIY",
                     "East Java, Bali & Nusa Tenggara","Banten",
                     "Sumatra","Sulawesi, Kalimantan, Maluku, Papua"],
    "SPKLU":        [790, 539, 279, 518, 271, 401, 404],
    "SPBKLU":       [587, 390,  72, 221, 326, 238,  68],
    "Phase":        ["Phase 1","Phase 1","Phase 2","Phase 2","Phase 1","Phase 3","Phase 3"],
    "EV_Density":   ["Very High","High","Medium","Medium","High","Low","Very Low"],
    "Lat":          [-6.21, -6.90, -7.50, -7.90, -6.10,  0.50, -2.00],
    "Lon":          [106.85,107.60,110.40,112.70,106.10,101.50,117.50],
})

risks = [
    {"id":"R1","name":"EoL battery leakage to informal markets","L":4,"S":5,"level":"Extreme","pillar":"All",
     "mitigation":"Deposit calibrated above secondary market price (Rp 3–4.5M); BaaS structurally prevents new-unit leakage."},
    {"id":"R2","name":"Consumer non-participation in deposit scheme","L":4,"S":4,"level":"Extreme","pillar":"Pillar 1",
     "mitigation":"SPKLU integration (Pillar 2) reduces friction; QR/RFID traceability builds consumer trust."},
    {"id":"R3","name":"Regulatory non-compliance by 2030 deadline","L":3,"S":5,"level":"Extreme","pillar":"All",
     "mitigation":"ECOS architecture maps directly to PerPres 55/2019 and Permenperin 6/2022 requirements."},
    {"id":"R4","name":"SPKLU partnership adoption failure","L":3,"S":4,"level":"Extreme","pillar":"Pillar 2",
     "mitigation":"EcoBat absorbs infrastructure cost; operator compensation tied to actual collection volume."},
    {"id":"R5","name":"Java-outside geographic coverage gap","L":3,"S":3,"level":"High","pillar":"Pillar 2",
     "mitigation":"Phased rollout prioritises Java first; BaaS logistics fleet compensates in low-density zones."},
    {"id":"R6","name":"Safety incident from non-standard battery modification","L":2,"S":5,"level":"Extreme","pillar":"Pillar 1",
     "mitigation":"Reducing informal market volume through BaaS and deposit scheme is the primary control mechanism."},
    {"id":"R7","name":"Deposit capital lock-up and cash-flow strain","L":4,"S":3,"level":"Extreme","pillar":"Pillar 1",
     "mitigation":"Phased rollout limits simultaneous exposure; Pillar 3 grading revenue offsets operational costs."},
    {"id":"R8","name":"Second-life ESS market underdevelopment","L":2,"S":4,"level":"High","pillar":"Pillar 3",
     "mitigation":"Material recovery (Li, Co, Ni) acts as revenue floor; dual-pathway model per Chirumalla et al. (2022)."},
    {"id":"R9","name":"QR/RFID traceability failure or data breach","L":3,"S":2,"level":"Medium","pillar":"Pillar 2",
     "mitigation":"Redundant capture at collection point; grading facility serves as secondary verification layer."},
    {"id":"R10","name":"EV growth outpacing EoL system readiness","L":5,"S":2,"level":"Extreme","pillar":"All",
     "mitigation":"BaaS prevents future accumulation; deposit scheme front-loads returns before peak EoL wave arrives."},
    {"id":"R11","name":"BaaS fleet operator resistance","L":2,"S":3,"level":"Medium","pillar":"Pillar 1",
     "mitigation":"NIO/CATL precedent as proof-of-concept; Shi & Hu (2024) formally prove BaaS reduces total consumer cost."},
    {"id":"R12","name":"Competitive replication of ECOS infrastructure","L":2,"S":2,"level":"Low","pillar":"All",
     "mitigation":"Traceability database and SPKLU relationship network are structurally slow to replicate; data moat compounds over time."},
]
df_risk = pd.DataFrame(risks)
df_risk["Score"] = df_risk["L"] * df_risk["S"]


# ─── Hide sidebar + inject top nav CSS ─────────────────────────────────────────
st.markdown("""
<style>
section[data-testid="stSidebar"]  { display: none !important; }
[data-testid="collapsedControl"]   { display: none !important; }
.main .block-container {
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    padding-top: 0.5rem !important;
}
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background: rgba(0,229,160,0.12) !important;
    border: 1px solid rgba(0,229,160,0.4) !important;
    color: #00E5A0 !important;
}
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid #1A2840 !important;
    color: #8CA0BB !important;
}
div[data-testid="stHorizontalBlock"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    border-radius: 6px !important;
    padding: 6px 4px !important;
}
</style>
""", unsafe_allow_html=True)

# Brand bar
st.markdown("""
<div style="background:#080D18;border-bottom:1px solid #1A2840;
            padding:12px 20px;margin:-0.5rem -1.5rem 1rem -1.5rem;
            display:flex;align-items:center;">
    <span style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                color:#00E5A0;letter-spacing:0.08em;margin-right:20px;">⚡ ECOS</span>
    <span style="font-family:'Space Mono',monospace;font-size:0.58rem;
                color:#4A6080;margin-right:auto;">EcoBat Indonesia · IEEEBIG 2026 · Team Elpatron</span>
    <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:#4A6080;">
        Source: PLN (2024) · Casebook Data (2026)</span>
</div>
""", unsafe_allow_html=True)

# Session state
PAGES = [
    ("🏠 Overview",   "Overview"),
    ("🟢 Pillar 1",   "Pillar 1"),
    ("🔵 Pillar 2",   "Pillar 2"),
    ("🔴 Pillar 3",   "Pillar 3"),
    ("💰 Financial",  "Financial"),
    ("⚠️ Risk",        "Risk"),
    ("🎛️ Simulator",  "Simulator"),
    ("📍 ROI by City", "ROI"),
    ("🤖 Ask ECOS AI", "AI"),
    ("📄 Export PDF",  "PDF"),
]

if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0

nav_cols = st.columns(len(PAGES))
for i, (col, (label, _)) in enumerate(zip(nav_cols, PAGES)):
    with col:
        if st.button(label, key=f"nav_{i}", use_container_width=True,
                     type="primary" if st.session_state.page_idx == i else "secondary"):
            st.session_state.page_idx = i
            st.rerun()

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
page = PAGES[st.session_state.page_idx][1]



# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Executive Overview · Team Elpatron · IEEEBIG 2026</div>
        <h1>EcoBat Circular<br>Ownership System</h1>
        <p>Decentralized Reverse Logistics Transformation & Battery-as-a-Service Model for End-of-Life Battery Management in Indonesia</p>
    </div>""", unsafe_allow_html=True)

    kpi([
        ("Rp 7.70 T",   "Net System Benefit",    "5-Year Projection",          "green"),
        ("94,251",       "Units Sold — 2025",      "+800% growth since 2022",    "blue"),
        ("12%",          "Current Return Rate",    "88% leaks to informal market","orange"),
        ("Rp 26.34 M",  "Material Value/Battery", "Li + Co + Ni recovery",      "yellow"),
        ("2030",         "Regulatory Deadline",    "MoEF Regulation No. 9/2024", "blue"),
    ])
    div()

    col_l, col_r = st.columns([1.15, 1])
    with col_l:
        sec("CONSUMER BARRIER ANALYSIS")
        df_b = pd.DataFrame({
            "Barrier":  ["Distance to collection point","No financial incentive",
                         "Process too complicated","Overall willingness to return",
                         "Digital system acceptance"],
            "Percent":  [41, 37, 22, 28, 68],
            "Addressed by": ["Pillar 2","Pillar 1","Pillar 1+2","—","Pillar 2"],
        })
        cmap = {"Pillar 1": G, "Pillar 2": B, "Pillar 1+2": Y, "—": "#4A6080"}
        fig_b = px.bar(df_b, x="Percent", y="Barrier", orientation="h",
                       color="Addressed by", color_discrete_map=cmap, text="Percent")
        fig_b.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig_b.update_layout(**layout("Consumer Survey Results — n=1,250 (Q4 2025)", 310))
        fig_b.update_layout(xaxis=dict(range=[0, 88], gridcolor=GRID), showlegend=True)
        st.plotly_chart(fig_b, use_container_width=True)

        insight([
            "Distance (41%) is the single largest structural barrier — not attitude. ECOS Pillar 2 converts existing SPKLU stations into collection points, eliminating the need to build standalone infrastructure.",
            "37% cite no financial incentive. Pillar 1 deposit scheme is calibrated above secondary market price (Rp 3–4.5M on OLX), flipping the economic calculus in EcoBat's favour.",
            "68% accept digital/app-based return systems — a strong signal that Pillar 2's QR/RFID traceability will face low adoption friction.",
        ])

    with col_r:
        sec("CRITICAL SITUATION")
        for emoji, title, desc in [
            ("🔴","88% of Batteries Leak to Informal Markets",
             "Of 173,487 cumulative units sold (2022–2025), only ~12% return through official EcoBat channels."),
            ("🟡","Material Value Lost: Rp 26.34M per Battery",
             "Batteries resold via OLX forfeit recoverable Lithium, Cobalt, and Nickel worth up to Rp 26.34M each."),
            ("🟠","Hard Regulatory Deadline: 2030",
             "PerPres 55/2019, Permenperin 6/2022, and MoEF No. 9/2024 mandate operational recycling infrastructure."),
            ("🔵","EoL Wave Is Already Visible",
             "Earliest units sold in 2022 hit end-of-life by 2027. EoL volume reaches 76,500 units/year by 2032."),
        ]:
            st.markdown(f"""
            <div class="step-card">
                <div style="font-size:1.4rem;line-height:1">{emoji}</div>
                <div class="step-content"><h4>{title}</h4><p>{desc}</p></div>
            </div>""", unsafe_allow_html=True)

    div()
    sec("THREE-PILLAR ECOS FRAMEWORK")
    c1, c2, c3 = st.columns(3)
    for col, cls, tag, title, desc, bullets, num, numsub in [
        (c1,"p1","PILLAR 1","🟢 BaaS & Deposit Scheme",
         "Eliminates the ownership gap that allows batteries to leak into informal channels.",
         ["BaaS: EcoBat retains battery ownership throughout lifecycle",
          "Deposit scheme for 173,487 legacy units — set above OLX resale price",
          "Target final BaaS adoption: 70%"],
         "Rp 5,826.8 B","Net Benefit · 88.4% Margin"),
        (c2,"p2","PILLAR 2","🔵 Secondary Energy Hub",
         "Solves the physical accessibility barrier flagged by 41% of surveyed consumers.",
         ["Dual-purpose SPKLU stations: charging + EoL collection",
          "368 partner stations covering >50% of national SPKLU infrastructure",
          "Cost/unit: Rp 266,875 — 46.6% cheaper than standalone collection"],
         "Rp 25.4 B","Total Cost Savings vs Direct Collection"),
        (c3,"p3","PILLAR 3","🔴 Battery Grading Facility",
         "Monetises every collected battery through State-of-Health grading.",
         ["Grade A+B (SoH >50%): Second-life ESS for industrial & commercial buyers",
          "Grade C: Material recovery — Li/Co/Ni at net Rp 23.3M per unit",
          "153,040 units processed across 2029–2032"],
         "Rp 1,901.9 B","Net Profit · 88.0% Margin"),
    ]:
        with col:
            bl = "".join(f"<li>{b}</li>" for b in bullets)
            color = "var(--green)" if cls=="p1" else "var(--blue)" if cls=="p2" else "var(--orange)"
            st.markdown(f"""
            <div class="info-card {cls}">
                <div class="card-tag {cls}">{tag}</div>
                <h3>{title}</h3>
                <p style="margin-bottom:10px;font-size:0.83rem">{desc}</p>
                <ul style="padding-left:16px;margin:0">{bl}</ul>
                <div style="font-size:1.45rem;font-weight:700;color:{color};margin-top:14px">{num}</div>
                <div style="font-size:0.72rem;color:var(--txt3)">{numsub}</div>
            </div>""", unsafe_allow_html=True)

    div()
    sec("HISTORICAL SALES PERFORMANCE")
    cc1, cc2 = st.columns(2)
    with cc1:
        fig_s = make_subplots(specs=[[{"secondary_y": True}]])
        fig_s.add_trace(go.Bar(x=years, y=sales_vol, name="Sales Volume (Units)",
                               marker_color=B, marker_line_width=0,
                               text=sales_vol, textposition="outside", textfont=dict(size=10)),
                         secondary_y=False)
        fig_s.add_trace(go.Scatter(x=years, y=margin_h, name="Profit Margin (%)",
                                    mode="lines+markers",
                                    line=dict(color=G, width=2.5), marker=dict(size=8, color=G)),
                         secondary_y=True)
        fig_s.update_layout(**layout("Sales Volume & Profit Margin (2022–2025)", 320))
        fig_s.update_yaxes(title_text="Units", gridcolor=GRID, secondary_y=False)
        fig_s.update_yaxes(title_text="Margin (%)", secondary_y=True, range=[28, 44])
        st.plotly_chart(fig_s, use_container_width=True)
        insight([
            "Sales surged 812.7% from 10,327 (2022) to 94,250 units (2025) — yet the return infrastructure has not scaled proportionally.",
            "Profit margin improved consistently from 31.2% to 38.9%, confirming EcoBat's pricing power and COGS efficiency.",
            "The 800%+ growth trajectory means EoL volumes will accelerate sharply from 2027. ECOS must be operational before that wave peaks.",
        ])

    with cc2:
        fig_eol = go.Figure()
        fig_eol.add_trace(go.Bar(x=eol_yrs, y=eol_sales, name="Projected EoL Volume",
                                  marker_color="#1A2840", marker_line_color=B,
                                  marker_line_width=1.5,
                                  text=eol_sales, textposition="outside", textfont=dict(size=9)))
        fig_eol.add_trace(go.Bar(x=eol_yrs, y=eol_cap, name="Units Captured by ECOS",
                                  marker_color=O, marker_line_width=0,
                                  text=eol_cap, textposition="inside", textfont=dict(size=9)))
        fig_eol.update_layout(**layout("Projected EoL Volume vs ECOS Capture (2026–2032)", 320))
        fig_eol.update_layout(barmode="overlay")
        st.plotly_chart(fig_eol, use_container_width=True)
        insight([
            "Capture rate is low in early years (2026–2028) because the deposit scheme and SPKLU network are still being rolled out.",
            "By 2031–2032, ECOS capture accelerates sharply as the network matures and BaaS batteries begin reaching EoL.",
            "The gap between EoL volume and captured units represents the market for competitors — closing it fast is EcoBat's primary strategic advantage.",
        ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PILLAR 1
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Pillar 1":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Pillar 1 · Ownership Restructuring</div>
        <h1>Battery-as-a-Service<br>& Deposit Scheme</h1>
        <p>Restructuring the ownership model at point-of-sale to eliminate the structural gap that allows batteries to leak into informal channels.</p>
    </div>""", unsafe_allow_html=True)

    kpi([
        ("443,012",      "Cumulative BaaS Customers", "End of projection period (2029)", "green"),
        ("70%",          "Final Adoption Rate",        "Fleet-first → retail sequencing", "green"),
        ("Rp 6,419.4 B","Gross BaaS Revenue",         "5-Year projection",               "green"),
        ("156,138",      "Legacy Units Recovered",     "90% of 173,487 units in market",  "yellow"),
        ("Rp 5,826.8 B","Net Benefit — Pillar 1",     "Profit margin 88.4%",             "green"),
    ])
    div()

    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        sec("BATTERY-AS-A-SERVICE — HOW IT WORKS")
        for i, (title, desc) in enumerate([
            ("Root Cause",
             "Once a battery is sold, EcoBat loses all legal and economic leverage to recover it. This is an incentive design failure, not a consumer awareness problem."),
            ("BaaS Solution",
             "EcoBat sells access to battery usage — not the battery itself. The asset stays on EcoBat's books throughout its lifecycle, guaranteeing retrieval at EoL."),
            ("Implementation Sequence",
             "Phase 1 starts with fleet operators in logistics & transportation (predictable usage patterns, contract structures already support service models). Retail expansion follows."),
            ("Global Validation",
             "NIO + CATL (March 2024): after revising their BaaS program, adoption exceeded 70% among NIO buyers. Shi & Hu (2024) formally prove BaaS increases producer profitability while reducing total consumer cost."),
        ], 1):
            st.markdown(f"""
            <div class="step-card">
                <div class="step-num">{i:02d}</div>
                <div class="step-content"><h4>{title}</h4><p>{desc}</p></div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        sec("DEPOSIT SCHEME — LEGACY UNITS")
        st.markdown("""
        <div class="info-card p1">
            <div class="card-tag p1">173,487 Units Already in Consumer Hands</div>
            <h3>Why the Deposit Works</h3>
            <p style="margin-bottom:14px">
                The deposit is set <strong style="color:#F0F4F8">above the OLX secondary market price</strong>
                (Rp 3–4.5M), making formal return the financially rational choice over reselling.
            </p>""", unsafe_allow_html=True)
        for label, val, cls in [
            ("OLX Secondary Market Price",      "Rp 3–4.5 M",   ""),
            ("EcoBat Deposit (calibrated above)","Rp 4.5 M+",   "accent"),
            ("Total Cash Outflow (deposits)",    "Rp 281.0 B",   "warn"),
            ("Retained Sales via Voucher",       "+Rp 655.8 B",  "accent"),
            ("Total Deposit Outflow (net)",      "Rp 936.8 B",   "warn"),
            ("Recovery Rate Target",             "90%",          "accent"),
            ("Consumer Incentive #1 Preference", "Discount voucher (52%)", ""),
        ]:
            stat(label, val, cls)
        st.markdown("</div>", unsafe_allow_html=True)

    div()
    sec("BaaS CUSTOMER GROWTH & REVENUE (2025–2029)")
    c1, c2 = st.columns(2)
    with c1:
        fig_c = make_subplots(specs=[[{"secondary_y": True}]])
        fig_c.add_trace(go.Bar(x=baas_yrs, y=new_cust, name="New BaaS Customers",
                               marker_color=G, marker_line_width=0,
                               text=new_cust, textposition="outside", textfont=dict(size=10)),
                         secondary_y=False)
        fig_c.add_trace(go.Scatter(x=baas_yrs, y=cum_baas, name="Cumulative BaaS",
                                    mode="lines+markers",
                                    line=dict(color=Y, width=2.5), marker=dict(size=8, color=Y)),
                         secondary_y=True)
        fig_c.update_layout(**layout("New vs. Cumulative BaaS Customers", 350))
        fig_c.update_yaxes(title_text="New Customers / Year", gridcolor=GRID, secondary_y=False)
        fig_c.update_yaxes(title_text="Cumulative Customers", secondary_y=True)
        st.plotly_chart(fig_c, use_container_width=True)
        insight([
            "New customer acquisition grows from 28,275 (2025) to 161,072 (2029) — a 5.7× increase, driven by expanding retail BaaS availability post-2026.",
            "Cumulative base reaches 443,012 by 2029, approaching the 70% final adoption target. Each customer locks in guaranteed EoL recovery.",
        ])

    with c2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Bar(x=baas_yrs, y=sub_rev, name="Subscription Revenue (Rp B)",
                               marker_color=G, marker_line_width=0,
                               text=[f"Rp{v:.0f}B" for v in sub_rev],
                               textposition="outside", textfont=dict(size=9)))
        fig_r.add_trace(go.Bar(x=baas_yrs, y=nb_rev, name="Non-Battery EV Revenue (Rp B)",
                               marker_color="#1E3A5F", marker_line_width=0,
                               text=[f"Rp{v:.0f}B" for v in nb_rev],
                               textposition="outside", textfont=dict(size=9)))
        fig_r.update_layout(**layout("Subscription vs. Non-Battery EV Revenue", 350))
        fig_r.update_layout(barmode="group")
        st.plotly_chart(fig_r, use_container_width=True)
        insight([
            "Subscription revenue scales from Rp 118.8B (2025) to Rp 1,860.6B (2029) — a 15.7× increase over 5 years.",
            "Non-battery EV revenue (vehicle chassis, accessories) is additive: BaaS customers still purchase the full EV, excluding the battery cost.",
            "Combined revenue streams total Rp 6,419.4B gross, making Pillar 1 the dominant value driver at 75.7% of total ECOS net benefit.",
        ])

    div()
    sec("PILLAR 1 FINANCIAL SUMMARY")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card p1"><div class="card-tag p1">BaaS Model</div><h3>Revenue Metrics</h3>', unsafe_allow_html=True)
        for l, v, c in [
            ("Total BaaS Customers (2029)","443,012 units",""),
            ("Total Subscription Revenue","Rp 4,186.6 B",""),
            ("Total Non-Battery EV Revenue","Rp 2,232.8 B",""),
            ("Battery Depreciation (Cost)","Rp 311.5 B","warn"),
            ("GROSS BaaS REVENUE","Rp 6,419.4 B","accent"),
        ]: stat(l, v, c)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card p1"><div class="card-tag p1">Deposit Scheme</div><h3>Legacy Unit Recovery</h3>', unsafe_allow_html=True)
        for l, v, c in [
            ("Total Legacy Units in Market","173,487 units",""),
            ("Units Recovered (90%)","156,138 units","accent"),
            ("Cash Outflow — Deposits","Rp 281.0 B","warn"),
            ("Voucher Subsidy Outflow","Rp 655.8 B","warn"),
            ("TOTAL DEPOSIT OUTFLOW","Rp 936.8 B","warn"),
        ]: stat(l, v, c)
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card p1"><div class="card-tag p1">Financial Summary</div><h3>Bottom Line</h3>', unsafe_allow_html=True)
        for l, v, c in [
            ("Total Cash Inflow","Rp 10,720.2 B","accent"),
            ("Total Cash Outflow","Rp 1,248.3 B","warn"),
            ("NET BENEFIT — PILLAR 1","Rp 9,471.9 B","accent"),
            ("Profit Margin","88.4%","accent"),
        ]: stat(l, v, c)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PILLAR 2
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Pillar 2":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Pillar 2 · Decentralized Collection Network</div>
        <h1>Secondary Energy Hub<br>— SPKLU Network</h1>
        <p>Converting existing EV charging stations (SPKLU) into dual-purpose EoL battery collection points —
        eliminating the distance barrier cited by 41% of consumers.</p>
    </div>""", unsafe_allow_html=True)

    kpi([
        ("368",          "Partner SPKLU Stations",  "Target by 2029",                    "blue"),
        (">50%",         "National Coverage",        "Of total SPKLU infrastructure",     "blue"),
        ("109,037",      "Units Collected (5-Yr)",   "Cumulative 2025–2029",              "blue"),
        ("Rp 266,875",   "Cost per Unit Acquired",   "vs Rp 500K direct (−46.6%)",       "green"),
        ("Rp 25.4 B",    "Total Cost Savings",       "vs standalone direct collection",   "green"),
    ])
    div()

    sec("SPKLU INFRASTRUCTURE MAP — INDONESIA (Source: PLN, Dec 2024)")
    col_map, col_inf = st.columns([1.6, 1])
    with col_map:
        phase_filter = st.multiselect(
            "Filter by Implementation Phase",
            ["Phase 1", "Phase 2", "Phase 3"],
            default=["Phase 1", "Phase 2", "Phase 3"]
        )
        df_f = spklu_df[spklu_df["Phase"].isin(phase_filter)]
        c_phase = {"Phase 1": G, "Phase 2": Y, "Phase 3": O}
        s_density = {"Very High": 42, "High": 32, "Medium": 22, "Low": 14, "Very Low": 9}

        fig_map = go.Figure()
        for ph in phase_filter:
            df_ph = df_f[df_f["Phase"] == ph]
            for _, row in df_ph.iterrows():
                fig_map.add_trace(go.Scattergeo(
                    lon=[row["Lon"]], lat=[row["Lat"]],
                    mode="markers+text",
                    marker=dict(
                        size=s_density[row["EV_Density"]],
                        color=c_phase[ph], opacity=0.82,
                        line=dict(width=2, color="white"), symbol="circle"
                    ),
                    text=row["Region"],
                    textposition="top center",
                    textfont=dict(size=9.5, color="#F0F4F8"),
                    name=ph, showlegend=False,
                    hovertemplate=(
                        f"<b>{row['Region']}</b><br>"
                        f"Phase: {ph}<br>"
                        f"SPKLU units: {row['SPKLU']}<br>"
                        f"SPBKLU units: {row['SPBKLU']}<br>"
                        f"EV Density: {row['EV_Density']}<br>"
                        f"Est. Partner Target: ~{max(8, row['SPKLU']//6)} stations"
                        "<extra></extra>"
                    )
                ))
        # Legend proxies
        for ph, clr in c_phase.items():
            if ph in phase_filter:
                fig_map.add_trace(go.Scattergeo(lon=[None], lat=[None], mode="markers",
                                                  marker=dict(size=11, color=clr),
                                                  name=f"{ph} Priority", showlegend=True))
        fig_map.update_geos(
            scope="asia", center=dict(lon=118, lat=-2), projection_scale=4.2,
            showland=True, landcolor="#0C1220",
            showocean=True, oceancolor="#080D18",
            showcoastlines=True, coastlinecolor="#1A2840",
            showcountries=True, countrycolor="#1A2840",
            showframe=False, showlakes=False,
        )
        fig_map.update_layout(
            paper_bgcolor=BG, geo_bgcolor=BG, height=460,
            margin=dict(l=0,r=0,t=0,b=0),
            legend=dict(bgcolor="#0C1220", bordercolor=GRID, borderwidth=1,
                        font=dict(color=FONT, size=11), x=0.01, y=0.99)
        )
        st.plotly_chart(fig_map, use_container_width=True)
        insight([
            "70% of Indonesia's 3,202 SPKLU units are concentrated in Java — mirroring EV adoption patterns and validating Phase 1 focus on Java.",
            "Circle size represents EV density: DKI Jakarta and West Java are the highest-priority targets for early SPKLU partnerships.",
            "Hover each region to see SPKLU/SPBKLU counts and estimated partner station targets per area.",
        ])

    with col_inf:
        sec("SPKLU DATA BY REGION (PLN, Dec 2024)")
        disp = df_f[["Region","SPKLU","SPBKLU","Phase","EV_Density"]].copy()
        disp.columns = ["Region","SPKLU","SPBKLU","Phase","EV Density"]
        st.dataframe(disp, use_container_width=True, hide_index=True, height=210)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        sec("CONVERSION LOGIC")
        for emoji, title, desc in [
            ("🎯","Leveraging Existing Touchpoints",
             "EV drivers already visit SPKLU regularly. Adding battery collection requires no new real-estate or standalone infrastructure investment."),
            ("💰","Operator Revenue Alignment",
             "SPKLU operators receive volume-based compensation per battery collected — creating aligned incentives without capital expenditure on their side."),
            ("📡","QR/RFID Traceability",
             "Every battery entering the system is logged with its condition and routed toward the Pillar 3 grading facility — building a long-term asset database."),
            ("📊","68% Digital Acceptance",
             "Survey confirms 68% of consumers are willing to use a digital/app-based return system, validating the tech-enabled collection model."),
        ]:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:9px 0;border-bottom:1px solid var(--border)">
                <span style="font-size:1.1rem">{emoji}</span>
                <div>
                    <p style="color:var(--txt);font-weight:600;font-size:0.86rem;margin:0 0 2px">{title}</p>
                    <p style="color:var(--txt2);font-size:0.79rem;margin:0">{desc}</p>
                </div>
            </div>""", unsafe_allow_html=True)

    div()
    sec("NETWORK GROWTH, COST EFFICIENCY & OPEX BREAKDOWN")
    c1, c2, c3 = st.columns(3)
    with c1:
        fig_net = make_subplots(specs=[[{"secondary_y": True}]])
        fig_net.add_trace(go.Bar(x=sp_yrs, y=sp_stations, name="Partner Stations",
                                  marker_color=B, marker_line_width=0,
                                  text=sp_stations, textposition="outside", textfont=dict(size=10)),
                           secondary_y=False)
        fig_net.add_trace(go.Scatter(x=sp_yrs, y=sp_cumul, name="Cumul. Units Collected",
                                      mode="lines+markers",
                                      line=dict(color=G, width=2.5), marker=dict(size=8, color=G)),
                           secondary_y=True)
        fig_net.update_layout(**layout("Network Growth & Cumulative Collection", 340))
        fig_net.update_yaxes(title_text="Partner Stations", gridcolor=GRID, secondary_y=False)
        fig_net.update_yaxes(title_text="Cumulative Units", secondary_y=True)
        st.plotly_chart(fig_net, use_container_width=True)
        insight([
            "Station count grows 2.5× from 150 (2025) to 368 (2029), achieving >50% national SPKLU coverage.",
            "Collection volume accelerates in 2029 as BaaS legacy returns and deposit-scheme batteries begin flowing through the network.",
        ])

    with c2:
        fig_cc = go.Figure()
        fig_cc.add_trace(go.Bar(
            x=["Direct Collection\n(Standalone)", "SPKLU Partner\nNetwork"],
            y=[500_000, 266_875],
            marker_color=[R, G], marker_line_width=0,
            text=["Rp 500,000", "Rp 266,875"],
            textposition="outside", textfont=dict(size=12, color=FONT),
            width=0.5,
        ))
        fig_cc.add_annotation(
            x=0.5, y=385_000,
            text="<b>−46.6%</b>",
            showarrow=True, arrowhead=2, arrowcolor=G,
            ax=0, ay=-40, font=dict(size=16, color=G)
        )
        fig_cc.update_layout(**layout("Cost per Unit Acquired — Channel Comparison", 340))
        fig_cc.update_layout(yaxis_range=[0, 680_000], showlegend=False)
        st.plotly_chart(fig_cc, use_container_width=True)
        insight([
            "Leveraging existing SPKLU infrastructure saves Rp 233,125 per unit — a 46.6% reduction versus building standalone facilities.",
            "Over 5 years and 109,037 units, this translates to Rp 25.4B in cumulative cost savings.",
        ])

    with c3:
        labels_op = ["Operator\nCompensation","Logistics\nPickup","QR/RFID\nTraceability","Station\nSetup"]
        vals_op   = [56.2, 28.1, 9.4, 6.3]
        fig_op = px.pie(values=vals_op, names=labels_op,
                         color_discrete_sequence=[B, G, Y, O], hole=0.5)
        fig_op.update_traces(textposition="outside", textfont_size=11)
        fig_op.update_layout(**layout("OPEX Composition — 5-Year (Rp 29.1B)", 340))
        st.plotly_chart(fig_op, use_container_width=True)
        insight([
            "Operator compensation (56.2%) is the dominant cost — intentionally so, as it aligns SPKLU operators' incentives with EcoBat's collection goals.",
            "Tech traceability (QR/RFID) is only 9.4% of OPEX, making the digital tracking layer highly cost-effective.",
        ])

    div()
    sec("ANNUAL OPEX BREAKDOWN BY COMPONENT (Rp Billion)")
    fig_oy = go.Figure()
    for label, vals, clr in [
        ("Operator Compensation",   [3.2,3.1,3.3,3.3,3.3], B),
        ("Logistics Pickup",        [1.6,1.6,1.6,1.6,1.6], G),
        ("QR/RFID Traceability",    [0.6,0.5,0.5,0.5,0.6], Y),
        ("Station Setup (one-time)",[0.8,0.2,0.2,0.3,0.4], O),
    ]:
        fig_oy.add_trace(go.Bar(x=sp_yrs, y=vals, name=label,
                                 marker_color=clr, marker_line_width=0))
    fig_oy.add_trace(go.Scatter(x=sp_yrs, y=sp_opex, name="Total OPEX",
                                 mode="lines+markers",
                                 line=dict(color="white", width=2, dash="dot"),
                                 marker=dict(size=8, color="white")))
    fig_oy.update_layout(**layout("", 320))
    fig_oy.update_layout(barmode="stack")
    st.plotly_chart(fig_oy, use_container_width=True)
    insight([
        "Total OPEX remains stable at ~Rp 5.7–6.2B/year despite the station network more than doubling — demonstrating strong cost efficiency as the network scales.",
        "Station setup cost (one-time) drops from Rp 0.8B in 2025 to Rp 0.2–0.4B in subsequent years, confirming the front-loaded capex profile.",
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PILLAR 3
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Pillar 3":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Pillar 3 · Battery Monetisation</div>
        <h1>Battery Grading<br>Facility</h1>
        <p>Every collected battery is classified by State-of-Health and routed to the highest-value pathway:
        second-life ESS sales or material recovery of Lithium, Cobalt, and Nickel.</p>
    </div>""", unsafe_allow_html=True)

    kpi([
        ("153,040",      "Total Units Processed",    "2029–2032 projection",        "orange"),
        ("114,780",      "Second-Life Units (A+B)",  "75% of total processed",      "green"),
        ("84,172",       "Material Recovery Units",  "Grade C + unsold inventory",  "orange"),
        ("Rp 2,162.0 B","Total Pillar 3 Revenue",   "ESS + Material streams",      "orange"),
        ("88.0%",        "Profit Margin",             "Net Profit Rp 1,901.9 B",    "green"),
    ])
    div()

    sec("STATE-OF-HEALTH GRADING SYSTEM")
    c1, c2, c3 = st.columns(3)
    for col, letter, name, soh, clr, desc, rate, rev in [
        (c1,"A","Premium ESS","SoH 75–80%",G,
         "Refurbished and sold as premium second-life Energy Storage Systems to industrial operators and large commercial properties.",
         "Sell rate: 85%","Gross Revenue: Rp 239.7 B"),
        (c2,"B","Standard ESS","SoH 50–75%",B,
         "Refurbished as standard-grade ESS for SMEs, energy managers, and commercial building owners after testing.",
         "Sell rate: 80%","Net after Refurb: Rp 197.0 B"),
        (c3,"C","Material Recovery","SoH < 50%",O,
         "Disassembled and processed for extraction of Lithium, Cobalt, and Nickel through a 4-stage process: Collection → Disassembly → Pyrometallurgy → Compliance.",
         "Net value: Rp 23.3M/unit","Material Revenue: Rp 1,965.0 B"),
    ]:
        with col:
            st.markdown(f"""
            <div class="grade-card">
                <div class="grade-letter" style="color:{clr}">{letter}</div>
                <h4 style="color:{clr} !important;font-size:0.98rem !important;margin:0 0 4px">{name}</h4>
                <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:var(--txt3);
                            background:rgba(255,255,255,0.04);padding:2px 8px;border-radius:4px;
                            display:inline-block;margin-bottom:12px">{soh}</div>
                <p style="font-size:0.81rem !important;text-align:left !important;min-height:80px">{desc}</p>
                <div style="border-top:1px solid var(--border);padding-top:10px;margin-top:8px">
                    <div style="font-size:0.75rem;color:var(--txt3)">{rate}</div>
                    <div style="font-size:0.95rem;font-weight:700;color:{clr};margin-top:3px">{rev}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    div()
    sec("MATERIAL RECOVERY VALUE & REVENUE WATERFALL")
    col_mat, col_wf = st.columns([1, 1.3])
    with col_mat:
        mat_df = pd.DataFrame({
            "Material": ["Lithium","Cobalt","Nickel","TOTAL"],
            "Recovery (%)": ["85–92","92–96","90–94","—"],
            "Content (kg)": [7.5, 4.2, 11.0, 22.7],
            "Price (IDR/kg)": ["1,200,000","2,800,000","650,000","—"],
            "Value (Rp M)": ["7.65–8.28","10.89–11.34","6.44–6.72","24.97–26.34"],
        })
        st.dataframe(mat_df, use_container_width=True, hide_index=True)

        fig_mb = go.Figure()
        fig_mb.add_trace(go.Bar(
            x=["Lithium","Cobalt","Nickel"],
            y=[7.97, 11.12, 6.58],
            marker_color=[G, O, B], marker_line_width=0,
            text=["Rp 7.97M","Rp 11.12M","Rp 6.58M"],
            textposition="outside", textfont=dict(size=11)
        ))
        fig_mb.update_layout(**layout("Material Value Contribution per Battery (Rp Juta)", 270))
        fig_mb.update_layout(showlegend=False)
        st.plotly_chart(fig_mb, use_container_width=True)
        insight([
            "Cobalt is the highest-value material at Rp 11.12M/battery despite having the lowest mass (4.2 kg) — reflecting its premium market price of Rp 2.8M/kg.",
            "Total recoverable value per battery (Rp 24.97–26.34M) is over 90× the Pillar 2 acquisition cost of Rp 266,875 — making the collection investment extraordinarily efficient.",
        ])

    with col_wf:
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative","relative","total","relative","relative","total","relative","total"],
            x=["Gross ESS\nRevenue","Refurb\nCost","Net ESS\nRevenue",
               "Gross Material\nRevenue","Recycling\nCost","Net Material\nRevenue",
               "Grading\nCost","NET PILLAR 3\nPROFIT"],
            y=[239.7,-42.7,197.0, 2159.4,-194.4,1965.0, -23.0,1901.9],
            text=["Rp 239.7B","Rp 42.7B","Rp 197.0B",
                  "Rp 2,159.4B","Rp 194.4B","Rp 1,965.0B","Rp 23.0B","Rp 1,901.9B"],
            textposition="outside", textfont=dict(size=9.5),
            connector=dict(line=dict(color=GRID, width=1.5)),
            increasing=dict(marker=dict(color=G)),
            decreasing=dict(marker=dict(color=R)),
            totals=dict(marker=dict(color=O)),
        ))
        fig_wf.update_layout(**layout("Pillar 3 Cost vs Revenue Waterfall (Rp Billion)", 450))
        st.plotly_chart(fig_wf, use_container_width=True)
        insight([
            "Material recovery (Rp 1,965.0B net) dwarfs ESS revenue (Rp 197.0B net) by 10×, confirming that raw material extraction — not refurbishment — is the primary value driver in Pillar 3.",
            "Total operating costs (Rp 260.1B) are only 12% of gross revenue (Rp 2,162.0B), yielding an 88.0% net margin.",
            "Even if the second-life ESS market underperforms (Risk R8), material recovery alone sustains Pillar 3 profitability.",
        ])

    div()
    sec("GRADING VOLUME PROJECTION (2030–2033)")
    fig_gv = go.Figure()
    for label, vals, clr in [
        ("Grade A — Premium ESS (35%)",        ga_u, G),
        ("Grade B — Standard ESS (45%)",        gb_u, B),
        ("Grade C — Material Recovery (20%)",   gc_u, O),
    ]:
        fig_gv.add_trace(go.Bar(x=p3_yrs, y=vals, name=label,
                                 marker_color=clr, marker_line_width=0))
    totals_gv = [a+b+c for a,b,c in zip(ga_u,gb_u,gc_u)]
    fig_gv.add_trace(go.Scatter(x=p3_yrs, y=totals_gv, name="Total Units",
                                  mode="lines+markers+text",
                                  line=dict(color="white",width=2),
                                  text=totals_gv, textposition="top center",
                                  textfont=dict(size=11)))
    fig_gv.update_layout(**layout("Battery Grading Volume by SoH Grade", 360))
    fig_gv.update_layout(barmode="stack")
    st.plotly_chart(fig_gv, use_container_width=True)
    insight([
        "Total processed units grow from 5,257 (2030) to 35,926 (2033), reflecting BaaS batteries beginning to reach EoL at scale.",
        "Grade B (45%) is the largest segment — standard ESS provides a reliable secondary revenue stream alongside material recovery.",
        "Grade C batteries increase proportionally as older, more degraded legacy units enter the system in later years.",
    ])

    div()
    sec("INTERACTIVE BATTERY SOH CLASSIFIER")
    col_in, col_out = st.columns([1, 1])
    with col_in:
        soh_v  = st.slider("State of Health — SoH (%)", 0, 100, 68)
        cycles = st.number_input("Estimated Charge Cycles", 0, 3000, 800, 50)
        brand  = st.selectbox("EV Brand", ["Wuling Air EV","Hyundai Ioniq 5","BYD Atto 3",
                                            "Toyota bZ4X","Honda e:N1","Other"])
    with col_out:
        if soh_v >= 75:
            grade, path, clr = "A", "Premium ESS", G
            val_est = soh_v / 100 * 35
            desc = "Battery qualifies for premium ESS application. Minimal refurbishing required before resale."
        elif soh_v >= 50:
            grade, path, clr = "B", "Standard ESS", B
            val_est = soh_v / 100 * 25
            desc = "Battery can be refurbished for standard-grade stationary energy storage applications."
        else:
            grade, path, clr = "C", "Material Recovery", O
            val_est = 23.345
            desc = "SoH below automotive EoL threshold. Routed to material extraction for Li/Co/Ni recovery."

        st.markdown(f"""
        <div style="background:var(--bg-card);border:2px solid {clr};border-radius:12px;
                    padding:26px;text-align:center;">
            <div style="font-family:'Space Mono',monospace;font-size:0.67rem;color:var(--txt3);
                        letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px">
                {brand} · SoH {soh_v}% · {cycles} cycles
            </div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:5.5rem;
                        color:{clr};line-height:1;margin-bottom:6px">GRADE {grade}</div>
            <div style="font-size:1.05rem;font-weight:600;color:{clr};margin-bottom:8px">{path}</div>
            <div style="font-size:0.83rem;color:var(--txt2);margin-bottom:18px">{desc}</div>
            <div style="background:rgba(255,255,255,0.04);border-radius:7px;padding:12px">
                <div style="font-size:0.7rem;color:var(--txt3);margin-bottom:3px;
                             font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.1em">
                    Estimated Value</div>
                <div style="font-size:1.7rem;font-weight:700;color:{Y}">
                    ~Rp {val_est:.2f} Million / unit
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — FINANCIAL SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Financial":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Financial Summary · 5-Year Integrated Projection</div>
        <h1>ECOS Integrated<br>Financial Performance</h1>
        <p>A net system benefit of Rp 7.70 Trillion over five years, with profit margins exceeding 88% across all revenue-generating pillars.</p>
    </div>""", unsafe_allow_html=True)

    kpi([
        ("Rp 9,237.1 B","Total ECOS Revenue",     "Pillar 1 + Pillar 3",            "green"),
        ("Rp 1,537.5 B","Total Cost / Outflow",   "All three pillars combined",      "orange"),
        ("Rp 7,699.6 B","NET SYSTEM BENEFIT",     "5-Year projection",               "green"),
        ("88.0%",        "Profit Margin",          "Pillar 3 grading operations",     "yellow"),
        (">90×",         "ROI on Acquisition",    "Rp 267K cost → Rp 26.3M value",   "green"),
    ])
    div()

    col_main, col_side = st.columns([1.5, 1])
    with col_main:
        sec("REVENUE vs. COST vs. NET BENEFIT — BY PILLAR")
        p_labels = ["Pillar 1\n(BaaS + Deposit)","Pillar 2\n(SPKLU Network)",
                    "Pillar 3\n(Grading)","TOTAL ECOS"]
        rev_v  = [7075.1, 0,   2162.0, 9237.1]
        cost_v = [1248.3, 29.1, 260.1, 1537.5]
        net_v  = [5826.8,-29.1,1901.9, 7699.6]
        fig_pp = go.Figure()
        for name, vals, clr in [("Revenue (Rp B)", rev_v, B),
                                  ("Cost (Rp B)", cost_v, R),
                                  ("Net Benefit (Rp B)", net_v, G)]:
            fig_pp.add_trace(go.Bar(name=name, x=p_labels, y=vals,
                                     marker_color=clr, marker_line_width=0,
                                     text=[f"Rp {v:,.1f}B" for v in vals],
                                     textposition="outside", textfont=dict(size=10)))
        fig_pp.update_layout(**layout("", 400))
        fig_pp.update_layout(barmode="group")
        st.plotly_chart(fig_pp, use_container_width=True)
        insight([
            "Pillar 1 dominates, contributing 75.7% (Rp 5,826.8B) of total net benefit — BaaS subscription is the primary recurring revenue engine.",
            "Pillar 2 is intentionally a cost centre: its Rp 29.1B OPEX is fully funded by Pillar 3 revenue, and it enables both Pillar 1 deposits and Pillar 3 material input.",
            "Pillar 3 contributes 24.7% (Rp 1,901.9B) at an 88.0% margin, acting as a self-sustaining monetisation engine for all collected batteries.",
            "Total cost-to-revenue ratio is only 16.6%, confirming the system's capital efficiency.",
        ])

    with col_side:
        sec("NET BENEFIT SHARE")
        fig_pie = px.pie(values=[5826.8, 1901.9], names=["Pillar 1 (75.7%)", "Pillar 3 (24.7%)"],
                          color_discrete_sequence=[G, O], hole=0.55)
        fig_pie.update_traces(textposition="outside", textfont_size=12)
        fig_pie.update_layout(**layout("", 270))
        fig_pie.update_layout(annotations=[dict(
            text="<b>Rp 7.70 T</b>", x=0.5, y=0.5,
            font_size=15, font_color=FONT, showarrow=False
        )])
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        for l, v, c in [
            ("Pillar 1 Revenue",    "Rp 7,075.1 B", "accent"),
            ("Pillar 1 Cost",       "Rp 1,248.3 B", "warn"),
            ("Pillar 2 OPEX",       "Rp 29.1 B",    "warn"),
            ("Pillar 3 Revenue",    "Rp 2,162.0 B", "accent"),
            ("Pillar 3 Cost",       "Rp 260.1 B",   "warn"),
            ("NET SYSTEM BENEFIT",  "Rp 7,699.6 B", "accent"),
        ]: stat(l, v, c)
        st.markdown("</div>", unsafe_allow_html=True)

    div()
    sec("PILLAR INTERDEPENDENCY — SELF-SUSTAINING SYSTEM")
    flows = [
        ("Pillar 1 (BaaS)","→","Pillar 2 (Hub)",
         "156,138 deposit units need collection infrastructure"),
        ("Pillar 1 (Deposit)","→","Pillar 3 (Grading)",
         "Recovered batteries enter grading for monetisation"),
        ("Pillar 2 (Hub)","→","Pillar 3 (Grading)",
         "109,037 units via SPKLU feed into grading"),
        ("Pillar 3 (Revenue)","→","Pillar 1 (Incentives)",
         "Rp 2,162B revenue funds Rp 936.8B deposit outflow"),
        ("Pillar 3 (Revenue)","→","Pillar 2 (OPEX)",
         "Rp 1,901.9B profit funds Rp 29.1B station OPEX"),
    ]
    cols_f = st.columns(len(flows))
    for col, (frm, arr, to, desc) in zip(cols_f, flows):
        with col:
            st.markdown(f"""
            <div class="info-card" style="text-align:center;padding:14px">
                <div style="font-size:0.73rem;font-weight:600;color:var(--txt)">{frm}</div>
                <div style="font-size:1.4rem;color:var(--green);margin:5px 0">{arr}</div>
                <div style="font-size:0.73rem;font-weight:600;color:var(--txt);margin-bottom:7px">{to}</div>
                <div style="font-size:0.7rem;color:var(--txt2)">{desc}</div>
            </div>""", unsafe_allow_html=True)

    div()
    sec("PROJECTED EoL VOLUME vs. ECOS CAPTURE RATE (2026–2032)")
    fig_e2 = go.Figure()
    fig_e2.add_trace(go.Bar(x=eol_yrs, y=eol_sales, name="Projected EoL Volume",
                             marker_color="#1A2840", marker_line_color=B,
                             marker_line_width=1.5,
                             text=eol_sales, textposition="outside", textfont=dict(size=9)))
    fig_e2.add_trace(go.Bar(x=eol_yrs, y=eol_cap, name="Captured by ECOS",
                             marker_color=G, marker_line_width=0,
                             text=eol_cap, textposition="inside", textfont=dict(size=9)))
    fig_e2.update_layout(**layout("", 340))
    fig_e2.update_layout(barmode="overlay")
    st.plotly_chart(fig_e2, use_container_width=True)
    insight([
        "ECOS capture accelerates sharply in 2031–2032 as the network matures and BaaS units begin reaching EoL — the system is designed to be ready before peak volumes arrive.",
        "The capture gap in 2026–2028 represents units that will enter informal channels. ECOS's phased rollout acknowledges this as an acceptable trade-off for infrastructure quality.",
        "By 2032, projected capture rate approaches 65% of annual EoL volume — a significant structural improvement over the current 12% baseline.",
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — RISK ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Risk":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Risk Assessment · Likelihood × Severity Matrix</div>
        <h1>ECOS Risk<br>Assessment</h1>
        <p>12 risks identified using a Likelihood × Severity matrix (scored 1–5 on each axis).
        Each risk is mapped to affected pillars with structured mitigation strategies.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, lvl, clr, bg in [
        (c1,"Extreme","#EF4444","rgba(239,68,68,0.07)"),
        (c2,"High",   "#F97316","rgba(249,115,22,0.07)"),
        (c3,"Medium", "#EAB308","rgba(234,179,8,0.07)"),
        (c4,"Low",    "#22C55E","rgba(34,197,94,0.07)"),
    ]:
        n = len(df_risk[df_risk["level"] == lvl])
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-color:{clr};background:{bg}">
                <div class="kpi-label" style="color:{clr}">{lvl} Risk</div>
                <div class="kpi-value" style="color:{clr}">{n}</div>
                <div class="kpi-sub">of 12 identified risks</div>
            </div>""", unsafe_allow_html=True)

    div()
    col_sc, col_dt = st.columns([1.1, 1])
    with col_sc:
        sec("RISK SCATTER MATRIX")
        clrmap = {"Extreme":"#EF4444","High":"#F97316","Medium":"#EAB308","Low":"#22C55E"}
        fig_sc = px.scatter(
            df_risk, x="S", y="L", size="Score",
            color="level", text="id",
            color_discrete_map=clrmap,
            hover_data={"name":True,"mitigation":True,"pillar":True,"id":False},
            size_max=48,
        )
        fig_sc.update_traces(textposition="top center",
                              textfont=dict(size=11, color=FONT, family="Space Mono"))
        fig_sc.add_hline(y=3, line_dash="dot", line_color=GRID, line_width=1.5)
        fig_sc.add_vline(x=3, line_dash="dot", line_color=GRID, line_width=1.5)
        for x, y, txt in [
            (1.5, 4.5,"HIGH LIKELIHOOD\nLOW SEVERITY"),
            (4.2, 4.5,"CRITICAL ZONE"),
            (1.5, 1.5,"MONITOR"),
            (4.2, 1.5,"HIGH SEVERITY\nLOW LIKELIHOOD"),
        ]:
            fig_sc.add_annotation(x=x, y=y, text=txt,
                                   font=dict(size=8, color="#4A6080"),
                                   showarrow=False)
        fig_sc.update_layout(**layout("", 440))
        fig_sc.update_layout(
            xaxis=dict(title="Severity (1–5)", range=[0.3,5.7], gridcolor=GRID),
            yaxis=dict(title="Likelihood (1–5)", range=[0.3,5.7], gridcolor=GRID),
            legend=dict(bgcolor=BG, title_text="Level"),
        )
        st.plotly_chart(fig_sc, use_container_width=True)
        insight([
            "R1 (EoL leakage, score 20) and R3 (regulatory non-compliance, score 15) sit in the Critical Zone — highest combined Likelihood × Severity.",
            "R10 (EV growth outpacing readiness, score 10) has the highest Likelihood (5) but lower Severity (2) because ECOS's BaaS mechanism structurally prevents future accumulation.",
            "R12 (competitive replication) is the only Low risk — ECOS's traceability data moat and SPKLU relationships are difficult to replicate quickly.",
        ])

    with col_dt:
        sec("RISK DETAIL — FILTER & EXPLORE")
        f_lvl = st.multiselect("Risk Level", ["Extreme","High","Medium","Low"],
                                default=["Extreme","High"])
        f_pil = st.multiselect("Pillar", ["All","Pillar 1","Pillar 2","Pillar 3"],
                                default=["All","Pillar 1","Pillar 2","Pillar 3"])
        df_filt = df_risk[df_risk["level"].isin(f_lvl) & df_risk["pillar"].isin(f_pil)]
        sc_clr = {"Extreme":"#EF4444","High":"#F97316","Medium":"#EAB308","Low":"#22C55E"}
        for _, r in df_filt.iterrows():
            clr = sc_clr[r["level"]]
            st.markdown(f"""
            <div class="risk-row">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">
                    <span class="badge {r['level'].lower()}">{r['level']}</span>
                    <span style="font-family:'Space Mono',monospace;font-size:0.68rem;color:var(--txt3)">
                        {r['id']} · {r['pillar']} · L{r['L']}×S{r['S']}={r['Score']}
                    </span>
                </div>
                <div class="risk-name">{r['name']}</div>
                <div class="risk-mit">🛡 {r['mitigation']}</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — SCENARIO SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Simulator":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Interactive · Scenario Planning Tool</div>
        <h1>ECOS Scenario<br>Simulator</h1>
        <p>Adjust key parameters and see the real-time impact on ECOS integrated financial performance versus the baseline projection.</p>
    </div>""", unsafe_allow_html=True)

    col_sl, col_out = st.columns([1, 1.4])
    with col_sl:
        sec("INPUT PARAMETERS")
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        baas_a  = st.slider("🟢 BaaS Adoption Rate (%)", 20, 95, 70,
                             help="% of new EV buyers choosing BaaS over outright purchase")
        dep_r   = st.slider("🟡 Deposit Recovery Rate (%)", 40, 100, 90,
                             help="% of 173,487 legacy units successfully returned")
        sp_cov  = st.slider("🔵 SPKLU Network Coverage (%)", 15, 80, 50,
                             help="% of national SPKLU infrastructure partnered with EcoBat")
        ga_pct  = st.slider("🔴 Grade A Battery Ratio (%)", 15, 55, 35,
                             help="% of collected batteries grading as SoH >75%")
        li_p    = st.slider("Lithium Price (Rp Million/kg)", 0.8, 2.5, 1.2, 0.05)
        co_p    = st.slider("Cobalt Price (Rp Million/kg)",  1.5, 5.0, 2.8, 0.1)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="c-alert" style="margin-top:10px">
            <b>Tip:</b> Try dropping BaaS Adoption to 40% to see the cascading revenue impact.
            Cobalt price has the highest per-unit sensitivity of all material inputs.
        </div>""", unsafe_allow_html=True)

    with col_out:
        sec("PROJECTED OUTPUT — REAL-TIME")

        # Calculations
        adj_cust    = int(443_012 * baas_a / 70)
        adj_sub     = 6_419.4 * baas_a / 70
        adj_rec     = int(173_487 * dep_r / 100)
        adj_dep_out = adj_rec * 6.5 / 1000
        adj_sp_u    = int(109_037 * sp_cov / 50)
        total_b     = adj_rec + adj_sp_u
        ga = int(total_b * ga_pct / 100)
        gb = int(total_b * 0.45)
        gc = total_b - ga - gb
        mat_per     = 7.5*li_p + 4.2*co_p + 11.0*0.65
        mat_total   = gc * mat_per / 1000
        ess_total   = (ga*2.5 + gb*1.8) / 1000
        total_rev   = adj_sub + mat_total + ess_total
        total_cost  = adj_dep_out + 29.1 + 260.1
        net_b       = total_rev - total_cost
        margin      = net_b / total_rev * 100 if total_rev > 0 else 0
        delta       = net_b - 7_699.6
        delta_pct   = delta / 7_699.6 * 100
        delta_sign  = "+" if delta >= 0 else ""
        delta_clr   = G if delta >= 0 else R

        kpi([
            (f"{adj_cust:,}",          "BaaS Customers",       f"Adoption {baas_a}%",       "green"),
            (f"{adj_rec:,}",           "Legacy Units Recovered",f"{dep_r}% of 173,487",      "yellow"),
            (f"Rp {mat_per:.2f} M",   "Material Value/Battery","Li+Co+Ni at scenario prices","orange"),
            (f"Rp {net_b:,.1f} B",    "Net Benefit",           f"{delta_sign}{delta:.1f}B vs baseline","green"),
        ])

        # Revenue breakdown
        fig_sim = go.Figure()
        cats = ["BaaS\nSubscription","ESS\nRevenue","Material\nRecovery",
                "TOTAL\nREVENUE","Total\nCost","NET\nBENEFIT"]
        vals = [adj_sub, ess_total, mat_total, total_rev, total_cost, net_b]
        clrs = [B, G, O, Y, R, G]
        for cat, val, clr in zip(cats, vals, clrs):
            fig_sim.add_trace(go.Bar(x=[cat], y=[abs(val)], name=cat,
                                      marker_color=clr, marker_line_width=0,
                                      text=[f"Rp {abs(val):,.1f}B"],
                                      textposition="outside", textfont=dict(size=10),
                                      showlegend=False))
        fig_sim.update_layout(**layout("Scenario Revenue Breakdown (Rp Billion)", 310))
        st.plotly_chart(fig_sim, use_container_width=True)

        c_g1, c_g2 = st.columns(2)
        with c_g1:
            fig_gp = px.pie(values=[ga, gb, gc],
                             names=[f"Grade A ({ga:,})", f"Grade B ({gb:,})", f"Grade C ({gc:,})"],
                             color_discrete_sequence=[G, B, O], hole=0.5)
            fig_gp.update_layout(**layout("Grade Distribution", 240))
            st.plotly_chart(fig_gp, use_container_width=True)

        with c_g2:
            fig_vs = go.Figure()
            for name, val, clr in [("Scenario", net_b, G if net_b>=7699.6 else R),
                                     ("Baseline\n(70%/90%)", 7_699.6, B)]:
                fig_vs.add_trace(go.Bar(x=[name], y=[val], marker_color=clr,
                                         text=[f"Rp {val:,.1f}B"],
                                         textposition="outside", textfont=dict(size=11),
                                         showlegend=False, marker_line_width=0))
            fig_vs.update_layout(**layout("vs. Baseline", 240))
            fig_vs.update_layout(yaxis_range=[0, max(net_b, 7699.6)*1.28])
            st.plotly_chart(fig_vs, use_container_width=True)

        st.markdown(f"""
        <div style="background:{'rgba(0,229,160,0.06)' if delta>=0 else 'rgba(239,68,68,0.06)'};
                    border:1px solid {'rgba(0,229,160,0.18)' if delta>=0 else 'rgba(239,68,68,0.18)'};
                    border-radius:8px;padding:14px 18px;margin-top:8px">
            <span style="font-family:'Space Mono',monospace;font-size:0.67rem;color:var(--txt3);
                          text-transform:uppercase;letter-spacing:0.1em">Delta vs Baseline</span>
            <div style="font-size:1.35rem;font-weight:700;color:{delta_clr};margin-top:4px">
                {delta_sign}Rp {abs(delta):,.1f} B &nbsp;·&nbsp; {delta_sign}{delta_pct:.1f}%
            </div>
            <div style="font-size:0.81rem;color:var(--txt2);margin-top:3px">
                Net Margin: {margin:.1f}% &nbsp;·&nbsp;
                Material Value/unit: Rp {mat_per:.2f}M &nbsp;·&nbsp;
                Total Batteries: {total_b:,} units
            </div>
        </div>""", unsafe_allow_html=True)

        insight([
            f"At {baas_a}% BaaS adoption, subscription revenue {'exceeds' if adj_sub>4186 else 'falls below'} the baseline Rp 4,186.6B — every 10% adoption change shifts revenue by ~Rp {6419.4*0.1:.0f}B.",
            f"At Cobalt Rp {co_p:.1f}M/kg, material value per battery is Rp {mat_per:.2f}M. A 1M/kg increase in cobalt price adds ~Rp {4.2*gc/1000:.1f}B to total material revenue.",
            f"{'Scenario outperforms' if delta >= 0 else 'Scenario underperforms'} baseline by Rp {abs(delta):,.1f}B ({delta_sign}{delta_pct:.1f}%). {'Green zone — system remains highly profitable.' if delta >= 0 else 'Adjust BaaS adoption or deposit recovery to recover profitability.'}",
        ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — ROI CALCULATOR BY CITY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "ROI":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">ROI Calculator · City-Level Analysis</div>
        <h1>Real-Time ROI<br>Calculator by City</h1>
        <p>Select any Indonesian city to model ECOS deployment ROI — SPKLU coverage,
        projected EoL volume, material revenue, and payback period.</p>
    </div>""", unsafe_allow_html=True)

    # City database
    cities = {
        "Jakarta": {
            "province":"DKI Jakarta","spklu":790,"ev_density":0.95,
            "pop_m":10.6,"ev_units_2025":28000,"industry_score":0.95,
        },
        "Bandung": {
            "province":"West Java","spklu":180,"ev_density":0.70,
            "pop_m":2.5,"ev_units_2025":6200,"industry_score":0.80,
        },
        "Surabaya": {
            "province":"East Java","spklu":145,"ev_density":0.65,
            "pop_m":2.9,"ev_units_2025":5800,"industry_score":0.78,
        },
        "Bekasi": {
            "province":"West Java","spklu":120,"ev_density":0.72,
            "pop_m":3.1,"ev_units_2025":7100,"industry_score":0.75,
        },
        "Tangerang": {
            "province":"Banten","spklu":110,"ev_density":0.68,
            "pop_m":2.2,"ev_units_2025":5200,"industry_score":0.74,
        },
        "Depok": {
            "province":"West Java","spklu":95,"ev_density":0.65,
            "pop_m":2.3,"ev_units_2025":4800,"industry_score":0.70,
        },
        "Semarang": {
            "province":"Central Java","spklu":88,"ev_density":0.55,
            "pop_m":1.7,"ev_units_2025":3200,"industry_score":0.68,
        },
        "Medan": {
            "province":"North Sumatra","spklu":72,"ev_density":0.45,
            "pop_m":2.5,"ev_units_2025":2100,"industry_score":0.60,
        },
        "Makassar": {
            "province":"South Sulawesi","spklu":55,"ev_density":0.38,
            "pop_m":1.5,"ev_units_2025":1400,"industry_score":0.55,
        },
        "Palembang": {
            "province":"South Sumatra","spklu":48,"ev_density":0.35,
            "pop_m":1.7,"ev_units_2025":1100,"industry_score":0.52,
        },
        "Balikpapan": {
            "province":"East Kalimantan","spklu":42,"ev_density":0.40,
            "pop_m":0.7,"ev_units_2025":900,"industry_score":0.60,
        },
        "Denpasar": {
            "province":"Bali","spklu":68,"ev_density":0.60,
            "pop_m":0.9,"ev_units_2025":2800,"industry_score":0.72,
        },
    }

    col_inp, col_out = st.columns([1, 1.6])
    with col_inp:
        sec("CITY PARAMETERS")
        city_name = st.selectbox("Select City", list(cities.keys()))
        c = cities[city_name]

        st.markdown(f"""
        <div class="info-card p2" style="margin-top:12px">
            <div class="card-tag p2">{c['province']}</div>
            <h3>{city_name}</h3>""", unsafe_allow_html=True)
        for label, val in [
            ("Existing SPKLU Units",    f"{c['spklu']} units"),
            ("EV Units in Market 2025", f"{c['ev_units_2025']:,} units"),
            ("Population",              f"{c['pop_m']}M people"),
            ("EV Density Score",        f"{c['ev_density']*100:.0f}/100"),
            ("Industry Score",          f"{c['industry_score']*100:.0f}/100"),
        ]:
            st.markdown(f"""
            <div class="stat-row">
                <span class="stat-label">{label}</span>
                <span class="stat-value">{val}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        sec("DEPLOYMENT PARAMETERS")
        partner_pct   = st.slider("SPKLU Partnership Rate (%)", 10, 80, 40,
                                   help="% of city's SPKLU units that become collection partners")
        deposit_r     = st.slider("Deposit Recovery Rate (%)", 50, 100, 85)
        baas_r        = st.slider("BaaS Adoption Rate (%)", 20, 90, 65)
        years_deploy  = st.slider("Deployment Horizon (Years)", 1, 7, 5)

    with col_out:
        # Calculations
        partner_stations = max(1, int(c['spklu'] * partner_pct / 100))
        units_via_spklu  = partner_stations * 84 * years_deploy  # 84 avg/station/year
        legacy_units     = int(c['ev_units_2025'] * 0.6)         # 60% already EoL eligible
        recovered_legacy = int(legacy_units * deposit_r / 100)
        baas_units       = int(c['ev_units_2025'] * baas_r / 100 * years_deploy * 0.3)
        total_batteries  = units_via_spklu + recovered_legacy + baas_units

        # Revenue
        mat_val_per      = 24.97   # Rp million mid estimate
        grade_c_share    = 0.20
        grade_ab_share   = 0.80
        mat_rev          = total_batteries * grade_c_share * mat_val_per / 1000  # Rp B
        ess_rev          = total_batteries * grade_ab_share * 2.15 / 1000        # Rp B
        baas_sub_rev     = baas_units * 3.6 / 1000                               # Rp B avg sub
        total_rev        = mat_rev + ess_rev + baas_sub_rev

        # Costs
        setup_cost       = partner_stations * 0.012   # Rp B per station
        opex_total       = partner_stations * 0.075 * years_deploy  # Rp B/yr
        deposit_cost     = recovered_legacy * 5.5 / 1000
        total_cost       = setup_cost + opex_total + deposit_cost
        net_benefit      = total_rev - total_cost
        roi_pct          = (net_benefit / total_cost * 100) if total_cost > 0 else 0
        payback_months   = (total_cost / (total_rev / (years_deploy * 12))) if total_rev > 0 else 999
        payback_months   = min(payback_months, 999)

        sec(f"PROJECTED ROI — {city_name.upper()} ({years_deploy}-YEAR HORIZON)")
        kpi([
            (f"{partner_stations}", "Partner Stations", f"{partner_pct}% of {c['spklu']} SPKLU", "blue"),
            (f"{total_batteries:,}", "Total Batteries Collected", "Via SPKLU + Deposit + BaaS", "green"),
            (f"Rp {total_rev:,.1f} B", "Total Revenue", f"Over {years_deploy} years", "green"),
            (f"{roi_pct:,.0f}%", "ROI", f"Net Rp {net_benefit:,.1f}B", "yellow"),
            (f"{payback_months:.0f} mo", "Payback Period", "From deployment start", "blue"),
        ])

        # Revenue waterfall
        fig_roi = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative","relative","relative","total","relative","relative","relative","total"],
            x=["Material\nRecovery","ESS\nRevenue","BaaS\nSubscription",
               "TOTAL\nREVENUE","Setup\nCost","OPEX","Deposit\nOutflow","NET\nBENEFIT"],
            y=[mat_rev, ess_rev, baas_sub_rev, total_rev,
               -setup_cost, -opex_total, -deposit_cost, net_benefit],
            text=[f"Rp {abs(v):.2f}B" for v in [mat_rev, ess_rev, baas_sub_rev, total_rev,
                                                   -setup_cost, -opex_total, -deposit_cost, net_benefit]],
            textposition="outside", textfont=dict(size=10),
            connector=dict(line=dict(color=GRID, width=1.5)),
            increasing=dict(marker=dict(color=G)),
            decreasing=dict(marker=dict(color=R)),
            totals=dict(marker=dict(color=O)),
        ))
        fig_roi.update_layout(**layout(f"ROI Waterfall — {city_name}", 380))
        st.plotly_chart(fig_roi, use_container_width=True)

        # Year-by-year projection
        sec("YEAR-BY-YEAR PROJECTION")
        yr_labels = [f"Year {i+1}" for i in range(years_deploy)]
        cumulative_factor = [(i+1)/years_deploy for i in range(years_deploy)]
        yr_rev  = [total_rev * f * (1 + 0.15*i/years_deploy) / sum(cumulative_factor) * years_deploy / years_deploy
                   for i, f in enumerate(cumulative_factor)]
        yr_cost = [total_cost * f / sum(cumulative_factor) for f in cumulative_factor]
        yr_net  = [r - c for r, c in zip(yr_rev, yr_cost)]

        fig_yr = go.Figure()
        fig_yr.add_trace(go.Bar(x=yr_labels, y=yr_rev, name="Revenue",
                                 marker_color=G, marker_line_width=0,
                                 text=[f"Rp {v:.2f}B" for v in yr_rev], textposition="outside"))
        fig_yr.add_trace(go.Bar(x=yr_labels, y=yr_cost, name="Cost",
                                 marker_color=R, marker_line_width=0,
                                 text=[f"Rp {v:.2f}B" for v in yr_cost], textposition="outside"))
        fig_yr.add_trace(go.Scatter(x=yr_labels, y=yr_net, name="Net Benefit",
                                     mode="lines+markers",
                                     line=dict(color=Y, width=2.5), marker=dict(size=9)))
        fig_yr.update_layout(**layout("", 300))
        fig_yr.update_layout(barmode="group")
        st.plotly_chart(fig_yr, use_container_width=True)

        insight([
            f"{city_name} has {c['spklu']} SPKLU units — partnering {partner_pct}% ({partner_stations} stations) creates an accessible collection network without new infrastructure.",
            f"Total {total_batteries:,} batteries collected generates Rp {total_rev:.1f}B revenue over {years_deploy} years at {roi_pct:.0f}% ROI.",
            f"Estimated payback period: {payback_months:.0f} months from deployment start — {'strong investment case' if payback_months < 24 else 'moderate timeline, consider increasing partner stations'}.",
        ])

    div()
    sec("CITY COMPARISON — ALL CITIES")
    comparison_data = []
    for cn, cd in cities.items():
        ps = max(1, int(cd['spklu'] * 0.40))
        tb = ps * 84 * 5 + int(cd['ev_units_2025'] * 0.6 * 0.85) + int(cd['ev_units_2025'] * 0.65 * 0.3 * 5 * 0.3)
        rev = tb * 0.20 * 24.97 / 1000 + tb * 0.80 * 2.15 / 1000
        cst = ps * 0.012 + ps * 0.075 * 5 + int(cd['ev_units_2025'] * 0.6 * 0.85) * 5.5 / 1000
        comparison_data.append({
            "City": cn, "Province": cd['province'],
            "Partner Stations": ps, "Batteries": tb,
            "Revenue (Rp B)": round(rev, 2),
            "Cost (Rp B)": round(cst, 2),
            "Net Benefit (Rp B)": round(rev - cst, 2),
            "ROI (%)": round((rev-cst)/cst*100 if cst>0 else 0, 0),
        })
    df_comp = pd.DataFrame(comparison_data).sort_values("Net Benefit (Rp B)", ascending=False)

    fig_comp = px.bar(df_comp, x="City", y="Net Benefit (Rp B)",
                       color="Net Benefit (Rp B)",
                       color_continuous_scale=["#EF4444","#F97316","#00E5A0"],
                       text="Net Benefit (Rp B)")
    fig_comp.update_traces(texttemplate="Rp %{text}B", textposition="outside", marker_line_width=0)
    fig_comp.update_layout(**layout("Net Benefit by City — 5-Year Baseline (40% SPKLU, 85% Deposit, 65% BaaS)", 380))
    fig_comp.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_comp, use_container_width=True)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — AI CHAT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "AI":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">AI-Powered · ECOS Knowledge Assistant</div>
        <h1>Ask ECOS AI</h1>
        <p>Ask any question about the ECOS framework, financial projections, risk assessment,
        or battery lifecycle management. Powered by Claude AI with full ECOS context.</p>
    </div>""", unsafe_allow_html=True)

    ECOS_CONTEXT = """
    You are ECOS AI, an expert assistant for the EcoBat Circular Ownership System (ECOS) —
    a business case developed by Team Elpatron for IEEEBIG 2026.

    KEY FACTS ABOUT ECOS:
    - EcoBat Indonesia sold 94,251 battery units in 2025, up 800%+ since 2022 (10,327 units)
    - Current return rate: only 12%. 88% of batteries leak to informal markets (OLX, etc.)
    - 173,487 cumulative units sold 2022-2025 are in consumer hands
    - Batteries resold informally forfeit material value of Rp 24.97-26.34 million each
    - Regulatory deadline: 2030 (PerPres 55/2019, Permenperin 6/2022, MoEF No.9/2024)

    ECOS THREE-PILLAR FRAMEWORK:
    Pillar 1 - BaaS & Deposit Scheme:
    - Battery-as-a-Service: EcoBat retains battery ownership, consumers pay subscription
    - Target: 443,012 cumulative BaaS customers by 2029, 70% final adoption
    - Deposit scheme for 173,487 legacy units, set above OLX price (Rp 3-4.5M)
    - 90% recovery rate target, 156,138 units recovered
    - Net Benefit: Rp 5,826.8 Billion, Margin 88.4%

    Pillar 2 - Secondary Energy Hub (SPKLU Network):
    - Convert existing SPKLU EV charging stations into dual-purpose collection points
    - Target: 368 partner stations, >50% national coverage by 2029
    - 109,037 units collected over 5 years
    - Cost/unit: Rp 266,875 vs Rp 500,000 standalone (46.6% savings)
    - Total OPEX: Rp 29.1 Billion (5 years)
    - 70% of Indonesia's 3,202 SPKLU units concentrated in Java (PLN 2024)

    Pillar 3 - Battery Grading Facility:
    - Grade A (SoH 75-80%): Premium ESS, 85% sell rate
    - Grade B (SoH 50-75%): Standard ESS, 80% sell rate
    - Grade C (SoH <50%): Material recovery - Lithium (85-92%), Cobalt (92-96%), Nickel (90-94%)
    - Material value per battery: Rp 24.97-26.34 Million
    - 153,040 units processed 2029-2032
    - Net Profit: Rp 1,901.9 Billion, Margin 88.0%

    INTEGRATED FINANCIALS (5-Year):
    - Total Revenue: Rp 9,237.1 Billion
    - Total Cost: Rp 1,537.5 Billion
    - NET SYSTEM BENEFIT: Rp 7,699.6 Billion (Rp 7.70 Trillion)
    - ROI on acquisition: >90x (Rp 267K cost → Rp 26.3M material value)

    TOP RISKS:
    R1 (Extreme): EoL leakage to informal markets — mitigated by deposit above market price
    R2 (Extreme): Consumer non-participation — mitigated by SPKLU friction reduction
    R3 (Extreme): Regulatory non-compliance — ECOS maps to all relevant regulations
    R10 (Extreme): EV growth outpacing readiness — BaaS prevents accumulation

    Answer questions clearly, cite specific numbers from the ECOS data above,
    and explain concepts in a way that is accessible to competition judges.
    Keep answers concise but data-rich. Use bullet points for lists.
    """

    # Init chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Suggested questions
    sec("SUGGESTED QUESTIONS")
    suggestions = [
        "What is the ROI justification for Pillar 2's SPKLU network?",
        "How does the deposit scheme beat the OLX secondary market?",
        "What happens if BaaS adoption only reaches 40%?",
        "Why is Cobalt the most valuable material in recovery?",
        "How does ECOS comply with the 2030 regulatory deadline?",
        "Compare ECOS to NIO's BaaS model in China.",
    ]
    sug_cols = st.columns(3)
    for i, (col, sug) in enumerate(zip(sug_cols * 2, suggestions)):
        with col:
            if st.button(sug, key=f"sug_{i}", use_container_width=True, type="secondary"):
                st.session_state.chat_history.append({"role": "user", "content": sug})
                st.session_state._trigger_ai = True
                st.rerun()

    div()
    sec("CONVERSATION")

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background:#1A2840;border-radius:10px 10px 0 10px;
                        padding:12px 16px;margin:8px 0;margin-left:15%;
                        border:1px solid #2D4A6E;">
                <div style="font-size:0.7rem;color:#4A6080;font-family:'Space Mono',monospace;
                             margin-bottom:5px;">YOU</div>
                <div style="color:#F0F4F8;font-size:0.9rem">{msg['content']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#0C1220;border-radius:10px 10px 10px 0;
                        padding:14px 18px;margin:8px 0;margin-right:15%;
                        border:1px solid #1A2840;border-left:3px solid #00E5A0;">
                <div style="font-size:0.7rem;color:#00E5A0;font-family:'Space Mono',monospace;
                             margin-bottom:6px;">⚡ ECOS AI</div>
                <div style="color:#8CA0BB;font-size:0.875rem;line-height:1.7;
                             white-space:pre-wrap">{msg['content']}</div>
            </div>""", unsafe_allow_html=True)

    # Input
    col_inp2, col_btn = st.columns([5, 1])
    with col_inp2:
        user_input = st.text_input("", placeholder="Ask anything about ECOS...",
                                    label_visibility="collapsed", key="chat_input")
    with col_btn:
        send = st.button("Send →", type="primary", use_container_width=True)

    # Clear button
    if st.session_state.chat_history:
        if st.button("🗑 Clear conversation", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    # Handle send
    trigger = getattr(st.session_state, "_trigger_ai", False)
    if (send and user_input) or trigger:
        if trigger:
            st.session_state._trigger_ai = False
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call Claude API
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            st.error("⚠️ ANTHROPIC_API_KEY not found in Streamlit Secrets. "
                     "Go to Manage App → Secrets and add your key.")
        else:
            import requests, json
            with st.spinner("ECOS AI is thinking..."):
                messages_payload = [
                    {"role": "user", "content": ECOS_CONTEXT + "\n\nNow answer the following question:"},
                    {"role": "assistant", "content": "Understood. I'm ready to answer questions about ECOS."},
                ] + st.session_state.chat_history

                try:
                    resp = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": "claude-haiku-4-5-20251001",
                            "max_tokens": 1024,
                            "messages": messages_payload,
                        },
                        timeout=30,
                    )
                    data = resp.json()
                    if "content" in data and data["content"]:
                        answer = data["content"][0]["text"]
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"API error: {data.get('error', {}).get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — EXPORT PDF
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "PDF":
    st.markdown("""
    <div class="page-header">
        <div class="page-tag">Export · Report Generator</div>
        <h1>Export ECOS<br>Summary Report</h1>
        <p>Generate a formatted HTML report of ECOS key metrics, financial projections,
        and risk summary — ready to print or save as PDF.</p>
    </div>""", unsafe_allow_html=True)

    sec("REPORT CONFIGURATION")
    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    with col_cfg1:
        include_overview  = st.checkbox("Executive Overview", value=True)
        include_pillar1   = st.checkbox("Pillar 1 — BaaS & Deposit", value=True)
        include_pillar2   = st.checkbox("Pillar 2 — SPKLU Network", value=True)
    with col_cfg2:
        include_pillar3   = st.checkbox("Pillar 3 — Battery Grading", value=True)
        include_financial = st.checkbox("Financial Summary", value=True)
        include_risk      = st.checkbox("Risk Assessment", value=True)
    with col_cfg3:
        report_title  = st.text_input("Report Title", "ECOS — Executive Summary Report")
        prepared_for  = st.text_input("Prepared For", "IEEEBIG 2026 Jury Panel")
        prepared_by   = st.text_input("Prepared By", "Team Elpatron")

    div()

    if st.button("⚡ Generate HTML Report", type="primary", use_container_width=True):
        sections = []

        if include_overview:
            sections.append("""
            <div class="section">
                <h2>1. Executive Overview</h2>
                <div class="kpi-grid">
                    <div class="kpi"><div class="kpi-val green">Rp 7.70 T</div><div class="kpi-lbl">Net System Benefit (5-Year)</div></div>
                    <div class="kpi"><div class="kpi-val blue">94,251</div><div class="kpi-lbl">Units Sold 2025 (+800%)</div></div>
                    <div class="kpi"><div class="kpi-val orange">12%</div><div class="kpi-lbl">Current Return Rate</div></div>
                    <div class="kpi"><div class="kpi-val yellow">Rp 26.34 M</div><div class="kpi-lbl">Material Value/Battery</div></div>
                </div>
                <p>EcoBat Indonesia sold 94,251 battery units in 2025, capping 800%+ growth since 2022.
                The current centralized return system captures only 12% of batteries entering end-of-life phase.
                ECOS addresses this through a three-pillar framework targeting Rp 7.70 Trillion net system benefit over 5 years.</p>
                <h3>Consumer Barrier Analysis (n=1,250, Q4 2025)</h3>
                <table><tr><th>Barrier</th><th>Percentage</th><th>Addressed By</th></tr>
                <tr><td>Distance to collection point</td><td>41%</td><td>Pillar 2</td></tr>
                <tr><td>No financial incentive</td><td>37%</td><td>Pillar 1</td></tr>
                <tr><td>Process too complicated</td><td>22%</td><td>Pillar 1+2</td></tr>
                <tr><td>Digital system acceptance</td><td>68%</td><td>Pillar 2 (enabler)</td></tr></table>
            </div>""")

        if include_pillar1:
            sections.append("""
            <div class="section">
                <h2>2. Pillar 1 — BaaS & Deposit Scheme</h2>
                <div class="kpi-grid">
                    <div class="kpi"><div class="kpi-val green">443,012</div><div class="kpi-lbl">Cumulative BaaS Customers (2029)</div></div>
                    <div class="kpi"><div class="kpi-val green">70%</div><div class="kpi-lbl">Final Adoption Rate</div></div>
                    <div class="kpi"><div class="kpi-val green">Rp 6,419.4 B</div><div class="kpi-lbl">Gross BaaS Revenue</div></div>
                    <div class="kpi"><div class="kpi-val yellow">156,138</div><div class="kpi-lbl">Legacy Units Recovered (90%)</div></div>
                </div>
                <table><tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total BaaS Customers (2029)</td><td>443,012 units</td></tr>
                <tr><td>Gross BaaS Revenue</td><td>Rp 6,419.4 Billion</td></tr>
                <tr><td>Legacy Units Recovered</td><td>156,138 units (90%)</td></tr>
                <tr><td>Total Deposit Outflow</td><td>Rp 936.8 Billion</td></tr>
                <tr><td><strong>NET BENEFIT — PILLAR 1</strong></td><td><strong>Rp 5,826.8 Billion (88.4% margin)</strong></td></tr></table>
            </div>""")

        if include_pillar2:
            sections.append("""
            <div class="section">
                <h2>3. Pillar 2 — Secondary Energy Hub (SPKLU Network)</h2>
                <div class="kpi-grid">
                    <div class="kpi"><div class="kpi-val blue">368</div><div class="kpi-lbl">Partner SPKLU Stations</div></div>
                    <div class="kpi"><div class="kpi-val blue">>50%</div><div class="kpi-lbl">National Coverage</div></div>
                    <div class="kpi"><div class="kpi-val blue">109,037</div><div class="kpi-lbl">Units Collected (5-Year)</div></div>
                    <div class="kpi"><div class="kpi-val green">−46.6%</div><div class="kpi-lbl">Cost Savings vs Direct</div></div>
                </div>
                <table><tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Partner Stations (2029)</td><td>368 stations</td></tr>
                <tr><td>National SPKLU Coverage</td><td>&gt;50%</td></tr>
                <tr><td>Total Units Collected</td><td>109,037 units</td></tr>
                <tr><td>Cost per Unit Acquired</td><td>Rp 266,875 (vs Rp 500,000 direct)</td></tr>
                <tr><td>Total Setup Investment</td><td>Rp 1.8 Billion</td></tr>
                <tr><td>Total 5-Year OPEX</td><td>Rp 29.1 Billion</td></tr>
                <tr><td><strong>Total Cost Savings</strong></td><td><strong>Rp 25.4 Billion</strong></td></tr></table>
            </div>""")

        if include_pillar3:
            sections.append("""
            <div class="section">
                <h2>4. Pillar 3 — Battery Grading Facility</h2>
                <div class="kpi-grid">
                    <div class="kpi"><div class="kpi-val orange">153,040</div><div class="kpi-lbl">Total Units Processed</div></div>
                    <div class="kpi"><div class="kpi-val green">114,780</div><div class="kpi-lbl">Second-Life Units (A+B)</div></div>
                    <div class="kpi"><div class="kpi-val orange">Rp 2,162.0 B</div><div class="kpi-lbl">Total Revenue</div></div>
                    <div class="kpi"><div class="kpi-val green">88.0%</div><div class="kpi-lbl">Profit Margin</div></div>
                </div>
                <table><tr><th>Grade</th><th>SoH Range</th><th>Pathway</th><th>Units</th><th>Revenue</th></tr>
                <tr><td>A — Premium ESS</td><td>75–80%</td><td>Second-life ESS (premium)</td><td>~40,180</td><td>Rp 239.7B gross</td></tr>
                <tr><td>B — Standard ESS</td><td>50–75%</td><td>Second-life ESS (standard)</td><td>~68,900</td><td>Rp 197.0B net</td></tr>
                <tr><td>C — Material Recovery</td><td>&lt;50%</td><td>Li/Co/Ni extraction</td><td>84,172</td><td>Rp 1,965.0B net</td></tr>
                <tr><td colspan="4"><strong>NET PILLAR 3 PROFIT</strong></td><td><strong>Rp 1,901.9 Billion</strong></td></tr></table>
                <h3>Material Recovery Value per Battery</h3>
                <table><tr><th>Material</th><th>Recovery %</th><th>Content (kg)</th><th>Value (Rp M)</th></tr>
                <tr><td>Lithium</td><td>85–92%</td><td>7.5</td><td>7.65–8.28</td></tr>
                <tr><td>Cobalt</td><td>92–96%</td><td>4.2</td><td>10.89–11.34</td></tr>
                <tr><td>Nickel</td><td>90–94%</td><td>11.0</td><td>6.44–6.72</td></tr>
                <tr><td><strong>TOTAL</strong></td><td>—</td><td>22.7</td><td><strong>24.97–26.34</strong></td></tr></table>
            </div>""")

        if include_financial:
            sections.append("""
            <div class="section">
                <h2>5. Integrated Financial Summary (5-Year Projection)</h2>
                <div class="kpi-grid">
                    <div class="kpi"><div class="kpi-val green">Rp 9,237.1 B</div><div class="kpi-lbl">Total Revenue</div></div>
                    <div class="kpi"><div class="kpi-val orange">Rp 1,537.5 B</div><div class="kpi-lbl">Total Cost</div></div>
                    <div class="kpi"><div class="kpi-val green">Rp 7,699.6 B</div><div class="kpi-lbl">NET SYSTEM BENEFIT</div></div>
                    <div class="kpi"><div class="kpi-val green">&gt;90×</div><div class="kpi-lbl">ROI on Acquisition</div></div>
                </div>
                <table><tr><th>Component</th><th>Revenue (Rp B)</th><th>Cost (Rp B)</th><th>Net Benefit (Rp B)</th></tr>
                <tr><td>Pillar 1 (BaaS + Deposit)</td><td>7,075.1</td><td>1,248.3</td><td>5,826.8</td></tr>
                <tr><td>Pillar 2 (SPKLU Network)</td><td>—</td><td>29.1</td><td>−29.1</td></tr>
                <tr><td>Pillar 3 (Grading)</td><td>2,162.0</td><td>260.1</td><td>1,901.9</td></tr>
                <tr><td><strong>TOTAL ECOS</strong></td><td><strong>9,237.1</strong></td><td><strong>1,537.5</strong></td><td><strong>7,699.6</strong></td></tr></table>
            </div>""")

        if include_risk:
            risk_rows = "\n".join([
                f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['level']}</td>"
                f"<td>{r['L']}×{r['S']}={r['L']*r['S']}</td><td>{r['pillar']}</td>"
                f"<td>{r['mitigation']}</td></tr>"
                for r in risks
            ])
            sections.append(f"""
            <div class="section">
                <h2>6. Risk Assessment</h2>
                <table>
                    <tr><th>ID</th><th>Risk</th><th>Level</th><th>Score</th><th>Pillar</th><th>Mitigation</th></tr>
                    {risk_rows}
                </table>
            </div>""")

        import datetime
        date_str = datetime.datetime.now().strftime("%d %B %Y")
        html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{report_title}</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;600;700&display=swap');
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'DM Sans', sans-serif; background: #fff; color: #1a1a2e; font-size: 13px; }}
    .cover {{ background: #05080F; color: white; padding: 60px 50px; min-height: 200px; }}
    .cover h1 {{ font-size: 2.8rem; font-weight: 700; color: #00E5A0; line-height: 1.1; margin-bottom: 10px; }}
    .cover .sub {{ color: #8CA0BB; font-size: 0.95rem; margin-top: 8px; }}
    .cover .meta {{ margin-top: 30px; display: flex; gap: 40px; }}
    .cover .meta div {{ border-top: 2px solid #1A2840; padding-top: 10px; }}
    .cover .meta .lbl {{ font-size: 0.65rem; color: #4A6080; text-transform: uppercase; letter-spacing: 0.12em; }}
    .cover .meta .val {{ color: #F0F4F8; font-size: 0.9rem; font-weight: 600; margin-top: 3px; }}
    .section {{ padding: 30px 50px; border-bottom: 1px solid #e8edf2; }}
    .section:last-child {{ border-bottom: none; }}
    h2 {{ font-size: 1.3rem; font-weight: 700; color: #05080F; margin-bottom: 16px;
           border-left: 4px solid #00E5A0; padding-left: 12px; }}
    h3 {{ font-size: 1rem; font-weight: 600; color: #1a1a2e; margin: 16px 0 10px; }}
    p {{ color: #4A5568; line-height: 1.7; margin-bottom: 12px; font-size: 0.875rem; }}
    .kpi-grid {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }}
    .kpi {{ flex: 1; min-width: 120px; background: #f8fafc; border: 1px solid #e2e8f0;
             border-radius: 8px; padding: 14px; text-align: center; }}
    .kpi-val {{ font-size: 1.3rem; font-weight: 700; margin-bottom: 4px; }}
    .kpi-lbl {{ font-size: 0.68rem; color: #718096; text-transform: uppercase; letter-spacing: 0.08em; }}
    .green {{ color: #059669; }} .blue {{ color: #0284C7; }}
    .orange {{ color: #EA580C; }} .yellow {{ color: #D97706; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 0.82rem; }}
    th {{ background: #05080F; color: #00E5A0; padding: 8px 12px; text-align: left;
           font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    td {{ padding: 8px 12px; border-bottom: 1px solid #e8edf2; color: #2D3748; vertical-align: top; }}
    tr:nth-child(even) td {{ background: #f8fafc; }}
    .footer {{ background: #05080F; color: #4A6080; padding: 20px 50px;
               font-size: 0.72rem; text-align: center; }}
    @media print {{
        .section {{ page-break-inside: avoid; }}
        .cover {{ page-break-after: always; }}
    }}
</style>
</head>
<body>
<div class="cover">
    <div style="font-size:0.7rem;color:#00E5A0;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:12px">
        ⚡ ECOS — EcoBat Circular Ownership System
    </div>
    <h1>{report_title}</h1>
    <div class="sub">Decentralized Reverse Logistics Transformation & Battery-as-a-Service Model</div>
    <div class="meta">
        <div><div class="lbl">Prepared For</div><div class="val">{prepared_for}</div></div>
        <div><div class="lbl">Prepared By</div><div class="val">{prepared_by}</div></div>
        <div><div class="lbl">Date</div><div class="val">{date_str}</div></div>
        <div><div class="lbl">Competition</div><div class="val">IEEEBIG 2026</div></div>
    </div>
</div>
{"".join(sections)}
<div class="footer">
    ECOS — Team Elpatron · IEEEBIG 2026 · Data: Casebook Data (2026) · PLN (2024) · Generated {date_str}
</div>
</body>
</html>"""

        st.download_button(
            label=" Download HTML Report",
            data=html_report,
            file_name=f"ECOS_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.html",
            mime="text/html",
            type="primary",
            use_container_width=True,
        )

        st.success(" Report generated! Click the button above to download. Open in browser → Ctrl+P → Save as PDF.")

        div()
        sec("REPORT PREVIEW")
        st.markdown(f"""
        <div style="background:white;border:1px solid #1A2840;border-radius:10px;
                    padding:30px;max-height:500px;overflow-y:auto;">
            {html_report}
        </div>""", unsafe_allow_html=True)
