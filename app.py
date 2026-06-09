"""
app.py  —  Global Forest Watch Data Visualization Dashboard
Course     : Exploratory Data Analysis
Instructor : Ali Hassan Sherazi
Dataset    : Global Forest Watch — Tree Cover Loss & Gain 2001-2023

CHECKLIST
✓ Dashboard title + description at the top
✓ Sidebar with all 6 required filter types
✓ All 6 filters linked to all 10 charts (+ bonus)
✓ KPI cards: total records, key averages, notable highs/lows
✓ All 10 chart types present and labeled
✓ Charts grouped logically into sections
✓ Consistent forest-green color theme
✓ Proper font sizes — not cluttered
✓ Responsive wide layout
"""

import streamlit as st

st.set_page_config(
    page_title="Global Forest Watch Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Merriweather:wght@700;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0B1E10 !important;
    color: #E8F5E9 !important;
    font-family: 'Nunito', sans-serif !important;
}
h1,h2,h3,h4 { font-family:'Merriweather',serif !important; color:#C8E6C9 !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#071209 0%,#0D2016 100%) !important;
    border-right: 2px solid #1F4028 !important;
}
[data-testid="stSidebar"] * { color:#A5D6A7 !important; }

.kpi-card {
    background:linear-gradient(135deg,#122819,#0D2016);
    border:1px solid #1F4028; border-radius:14px;
    padding:16px 12px 12px; text-align:center;
    box-shadow:0 4px 18px rgba(0,0,0,.45);
}
.kpi-label { font-size:9px; text-transform:uppercase; letter-spacing:2px; color:#558B2F; margin-bottom:5px; }
.kpi-value { font-family:'Merriweather',serif; font-size:22px; font-weight:900; color:#69F0AE; line-height:1.1; }
.kpi-sub   { font-size:9px; color:#2E7D32; margin-top:4px; }

.chart-box {
    background:#112B18; border:1px solid #1F4028;
    border-radius:12px; padding:14px 14px 6px; margin-bottom:14px;
}
.sec-hdr {
    font-size:10px; font-weight:800; text-transform:uppercase;
    letter-spacing:3px; color:#4CAF50;
    border-bottom:1px solid #1F4028; padding-bottom:7px; margin:26px 0 14px;
}
div[data-testid="stButton"]>button {
    background:#2E7D32 !important; color:#E8F5E9 !important;
    border:none !important; border-radius:8px !important;
    font-weight:700 !important;
}
div[data-testid="stButton"]>button:hover { background:#388E3C !important; }
</style>
""", unsafe_allow_html=True)

import pandas as pd, numpy as np
from filters import load_data, apply_filters, compute_kpis
from charts  import (chart_pie, chart_histogram, chart_line, chart_bar,
                     chart_scatter, chart_boxplot, chart_heatmap, chart_area,
                     chart_countplot, chart_violin, chart_bubble)

# ── Load ──────────────────────────────────────────────────────────────────────
df = load_data("data/GlobalForestWatch_TreeCoverLoss.csv")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — 6 REQUIRED FILTERS
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌿 Dashboard Filters")
    st.markdown(
        "<p style='font-size:11px;color:#2E7D32;margin-top:-8px;'>"
        "All 6 filters apply to every chart simultaneously.</p>",
        unsafe_allow_html=True)
    st.markdown("---")

    # Filter 1 — Date / Time Range
    st.markdown("**📅 Filter 1 · Year Range**")
    y_min, y_max = int(df["Year"].min()), int(df["Year"].max())
    year_range = st.slider("Year range", y_min, y_max, (y_min, y_max),
                           step=1, label_visibility="collapsed")

    st.markdown("---")

    # Filter 2 — Category (Region dropdown)
    st.markdown("**🌍 Filter 2 · Region (Category)**")
    regions_all = sorted(df["Region"].dropna().unique())
    sel_region  = st.selectbox("Region", ["All"] + regions_all,
                               label_visibility="collapsed")

    st.markdown("---")

    # Filter 3 — Numerical Range Slider
    st.markdown("**📊 Filter 3 · Annual Loss Range (ha)**")
    lo, hi = float(df["TreeCoverLoss_ha"].min()), float(df["TreeCoverLoss_ha"].max())
    loss_range = st.slider("Loss (ha)", lo, hi, (lo, hi),
                           label_visibility="collapsed")

    st.markdown("---")

    # Filter 4 — Multi-Select (Biome)
    st.markdown("**🌲 Filter 4 · Biome (Multi-Select)**")
    biomes_all = sorted(df["Biome"].dropna().unique())
    sel_biomes = st.multiselect("Biome", biomes_all, default=[],
                                placeholder="All biomes",
                                label_visibility="collapsed")

    st.markdown("---")

    # Filter 5 — Multi-Select (Countries)
    st.markdown("**📍 Filter 5 · Countries (Multi-Select)**")
    countries_all = sorted(df["Country"].dropna().unique())
    sel_countries = st.multiselect("Countries", countries_all, default=[],
                                   placeholder="All countries",
                                   label_visibility="collapsed")

    st.markdown("---")

    # Filter 6 — Search / Text
    st.markdown("**🔍 Filter 6 · Search Country**")
    search = st.text_input("Search", value="", placeholder="e.g. Brazil",
                           label_visibility="collapsed")

    st.markdown("---")

    # Reset button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    st.markdown(
        "<p style='font-size:10px;color:#1B5E20;text-align:center;margin-top:10px;'>"
        "Source: Global Forest Watch<br>Filters 1–6 → all 10 charts</p>",
        unsafe_allow_html=True)

# ── Apply filters → fdf used by EVERY chart ───────────────────────────────────
fdf = apply_filters(
    df,
    year_range  = year_range,
    region      = sel_region,
    biomes      = sel_biomes,
    countries   = sel_countries,
    loss_range  = loss_range,
    search      = search,
)
line_countries = sel_countries if sel_countries else None

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER — Title + description
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;padding:22px 0 4px;'>
  <div style='font-family:Merriweather,serif;font-size:36px;font-weight:900;color:#A5D6A7;'>
    🌳 Global Forest Watch Dashboard
  </div>
  <div style='font-size:13px;color:#558B2F;margin-top:9px;max-width:680px;margin-inline:auto;'>
    Tree cover loss · Deforestation drivers · Carbon emissions · Land-use change
    across 40 countries &amp; 4 biomes · 2001–2023
  </div>
</div>
<hr style='border-color:#1F4028;margin:14px 0 20px;'>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# KPI SUMMARY CARDS — Total Records · Key Averages · Notable Highs/Lows
# ═══════════════════════════════════════════════════════════════════════════════
k = compute_kpis(fdf)

def kcard(label, val, sub=""):
    return (f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{val}</div>'
            f'<div class="kpi-sub">{sub}</div></div>')

k1,k2,k3,k4,k5,k6,k7,k8 = st.columns(8)
k1.markdown(kcard("Total Records",   k["records"],         "filtered rows"),      unsafe_allow_html=True)
k2.markdown(kcard("Total Loss",      k["loss"],            "tree cover"),         unsafe_allow_html=True)
k3.markdown(kcard("Avg Annual Loss", k["ann"],             "global per year"),    unsafe_allow_html=True)
k4.markdown(kcard("Carbon Lost",     k["carbon"],          "CO₂ equivalent"),     unsafe_allow_html=True)
k5.markdown(kcard("Avg Tree Cover",  k["cover"],           "filtered avg"),       unsafe_allow_html=True)
k6.markdown(kcard("Most Affected",   str(k["country"])[:12], "highest total loss"), unsafe_allow_html=True)
k7.markdown(kcard("Top Driver",      str(k["driver"])[:14], "most frequent"),     unsafe_allow_html=True)
k8.markdown(kcard("Total Alerts",    k["alerts"],          "deforestation"),      unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION A — Trends Over Time   [Chart 3 Line + Chart 8 Area]
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">📈  Section A — Trends Over Time</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_line(fdf, countries=line_countries), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_area(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION B — Distribution & Spread   [Chart 2 Histogram + Chart 6 Box + Chart 10 Violin]
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">📊  Section B — Distribution &amp; Spread</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_histogram(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_boxplot(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.pyplot(chart_violin(fdf), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION C — Category Comparisons   [Chart 1 Pie + Chart 4 Bar + Chart 9 Count]
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">🌍  Section C — Category Comparisons</div>', unsafe_allow_html=True)
col5, col6 = st.columns([1, 2])
with col5:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_pie(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col6:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_bar(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.pyplot(chart_countplot(fdf), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION D — Relationships & Correlation   [Chart 5 Scatter + Chart 7 Heatmap + Bonus Bubble]
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">🔬  Section D — Relationships &amp; Correlation</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_scatter(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col8:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(chart_heatmap(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.pyplot(chart_bubble(fdf), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA PREVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">🗃  Filtered Data Preview</div>', unsafe_allow_html=True)
hl = [c for c in ["TreeCoverLoss_ha","CarbonLoss_tCO2"] if c in fdf.columns]
st.dataframe(
    fdf.head(500).style.background_gradient(subset=hl, cmap="YlOrRd") if hl else fdf.head(500),
    use_container_width=True, height=290)
st.caption(
    f"{len(fdf):,} filtered rows · "
    f"{fdf['Country'].nunique() if not fdf.empty else 0} countries · "
    f"{fdf['Year'].nunique() if not fdf.empty else 0} years")

st.markdown("""
<hr style='border-color:#1F4028;margin-top:36px;'>
<p style='text-align:center;font-size:11px;color:#1B5E20;padding-bottom:16px;'>
  Data: Global Forest Watch (synthetic sample) &nbsp;·&nbsp;
  Python · Pandas · Matplotlib · Seaborn · Streamlit
</p>""", unsafe_allow_html=True)
