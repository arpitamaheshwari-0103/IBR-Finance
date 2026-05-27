import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Payment Systems | Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme & Custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ---- Root Variables ---- */
:root {
    --bg-dark:      #0B0F1A;
    --bg-card:      #131929;
    --bg-card2:     #1A2236;
    --accent-blue:  #2F80ED;
    --accent-teal:  #27AE95;
    --accent-amber: #F2994A;
    --accent-red:   #EB5757;
    --text-primary: #E8EDF5;
    --text-muted:   #8A94A8;
    --border:       rgba(255,255,255,0.07);
    --radius:       12px;
}

/* ---- Global ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}
.main .block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 1400px; }

/* ---- Hide Streamlit branding ---- */
#MainMenu, footer, header { visibility: hidden; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .css-1d391kg { padding-top: 1.5rem; }

/* ---- KPI Cards ---- */
.kpi-grid { display: flex; gap: 16px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.kpi-card {
    flex: 1; min-width: 180px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: transform .15s ease, box-shadow .15s ease;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,.4); }
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-blue::before   { background: var(--accent-blue); }
.kpi-teal::before   { background: var(--accent-teal); }
.kpi-amber::before  { background: var(--accent-amber); }
.kpi-red::before    { background: var(--accent-red); }

.kpi-label {
    font-size: 11px; font-weight: 600; letter-spacing: 1.2px;
    text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px;
}
.kpi-value {
    font-size: 28px; font-weight: 700; color: var(--text-primary);
    line-height: 1; margin-bottom: 6px; font-family: 'DM Mono', monospace;
}
.kpi-sub { font-size: 12px; color: var(--text-muted); }
.kpi-badge {
    display: inline-block; padding: 2px 8px; border-radius: 20px;
    font-size: 11px; font-weight: 600; margin-top: 6px;
}
.badge-up   { background: rgba(39,174,149,.15); color: var(--accent-teal); }
.badge-down { background: rgba(235,87,87,.15);  color: var(--accent-red); }
.badge-neg  { background: rgba(242,153,74,.15);  color: var(--accent-amber); }

/* ---- Section Headers ---- */
.section-header {
    font-size: 13px; font-weight: 600; letter-spacing: 1.4px;
    text-transform: uppercase; color: var(--text-muted);
    margin: 2rem 0 1rem 0; padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

/* ---- Insight Box ---- */
.insight-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent-blue);
    border-radius: var(--radius);
    padding: 18px 22px; margin-bottom: 12px;
}
.insight-box.teal  { border-left-color: var(--accent-teal); }
.insight-box.amber { border-left-color: var(--accent-amber); }
.insight-box.red   { border-left-color: var(--accent-red); }
.insight-title {
    font-size: 13px; font-weight: 700; letter-spacing: .5px;
    color: var(--text-primary); margin-bottom: 6px;
}
.insight-body { font-size: 13px; color: var(--text-muted); line-height: 1.6; }

/* ---- Chart containers ---- */
.chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px; margin-bottom: 16px;
}
.chart-title {
    font-size: 14px; font-weight: 600; color: var(--text-primary);
    margin-bottom: 4px;
}
.chart-sub { font-size: 12px; color: var(--text-muted); margin-bottom: 16px; }

/* ---- Dashboard header ---- */
.dash-header {
    padding: 24px 0 16px 0; margin-bottom: .5rem;
    border-bottom: 1px solid var(--border);
}
.dash-title {
    font-size: 26px; font-weight: 700; color: var(--text-primary);
    letter-spacing: -.3px; margin-bottom: 4px;
}
.dash-subtitle { font-size: 14px; color: var(--text-muted); }
.dash-tag {
    display: inline-block; padding: 3px 10px;
    border: 1px solid var(--border); border-radius: 20px;
    font-size: 11px; color: var(--text-muted); margin-top: 10px;
}

/* ---- Plotly chart background ---- */
.js-plotly-plot .plotly { background: transparent !important; }

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 8px; color: var(--text-muted);
    font-size: 13px; font-weight: 500; padding: 6px 18px;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-blue) !important;
    color: white !important; border-color: var(--accent-blue) !important;
}

/* ---- Selectbox / Slider ---- */
.stSelectbox label, .stSlider label, .stMultiSelect label {
    font-size: 12px !important; font-weight: 600 !important;
    letter-spacing: .8px; text-transform: uppercase;
    color: var(--text-muted) !important;
}

/* ---- Divider ---- */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly shared theme ────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8A94A8", size=12),
    title_font=dict(family="DM Sans, sans-serif", color="#E8EDF5", size=14),
    legend=dict(
        bgcolor="rgba(19,25,41,0.9)",
        bordercolor="rgba(255,255,255,0.07)",
        borderwidth=1,
        font=dict(size=12, color="#E8EDF5"),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.07)",
        tickfont=dict(size=11),
        showspikes=True, spikecolor="rgba(255,255,255,0.2)",
        spikemode="across", spikethickness=1,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.07)",
        tickfont=dict(size=11),
    ),
    hoverlabel=dict(
        bgcolor="#1A2236",
        bordercolor="rgba(255,255,255,0.1)",
        font=dict(family="DM Sans", size=12, color="#E8EDF5"),
    ),
    margin=dict(l=10, r=10, t=40, b=40),
)

COLOR_BLUE  = "#2F80ED"
COLOR_TEAL  = "#27AE95"
COLOR_AMBER = "#F2994A"
COLOR_RED   = "#EB5757"

# ── Data Loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("payments_data.csv")
    df["date"] = pd.to_datetime(df["Month_Year"], format="%Y-%m")
    df = df.sort_values("date").reset_index(drop=True)

    events = pd.read_csv("event_markers.csv")
    events["date"] = pd.to_datetime(events["Date"], format="%Y-%m")

    insights = pd.read_csv("key_insights.csv")
    kpi = dict(zip(insights["Metric"], insights["Value"]))
    return df, events, kpi

df, events, kpi = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-size:18px;font-weight:700;color:#E8EDF5;margin-bottom:4px'>🏦 India Payments</div>
    <div style='font-size:12px;color:#8A94A8;margin-bottom:24px'>Analytics Intelligence</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Date Range</div>', unsafe_allow_html=True)
    min_year = int(df["date"].dt.year.min())
    max_year = int(df["date"].dt.year.max())
    year_range = st.slider("Select year range", min_year, max_year, (min_year, max_year))

    st.markdown('<div class="section-header">Variables</div>', unsafe_allow_html=True)
    show_vars = st.multiselect(
        "Select metrics to display",
        ["UPI_Transactions", "ATM_Withdrawals", "DebitCard_POS", "IMPS"],
        default=["UPI_Transactions", "ATM_Withdrawals"],
    )
    if not show_vars:
        show_vars = ["UPI_Transactions", "ATM_Withdrawals"]

    st.markdown('<div class="section-header">Chart Options</div>', unsafe_allow_html=True)
    show_events  = st.toggle("Show event markers", value=True)
    show_ma      = st.toggle("Show 3-month moving avg.", value=False)
    log_scale    = st.toggle("Logarithmic Y-axis", value=False)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#8A94A8;line-height:1.7'>
    <b style='color:#E8EDF5'>Sources</b><br>
    RBI DBIE — Table 45<br>
    NPCI Monthly Statistics<br>
    <br>
    <b style='color:#E8EDF5'>Period</b>: Jan 2018 – May 2026<br>
    <b style='color:#E8EDF5'>Observations</b>: 97 months
    </div>
    """, unsafe_allow_html=True)

# ── Filter data ────────────────────────────────────────────────────────────────
mask = (df["date"].dt.year >= year_range[0]) & (df["date"].dt.year <= year_range[1])
dff = df[mask].copy()

# Moving averages
for col in ["UPI_Transactions", "ATM_Withdrawals", "DebitCard_POS", "IMPS"]:
    dff[f"{col}_MA3"] = dff[col].rolling(3).mean()

# ── Dashboard Header ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
  <div class="dash-title">India Payment Systems Intelligence</div>
  <div class="dash-subtitle">
    FinTech vs Conventional Banking — Structural Transformation Analysis ({year_range[0]}–{year_range[1]})
  </div>
  <span class="dash-tag">🔴 LIVE DATA &nbsp;·&nbsp; RBI DBIE &nbsp;·&nbsp; NPCI</span>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
latest_upi = dff["UPI_Transactions"].iloc[-1]
peak_atm   = dff["ATM_Withdrawals"].max()
corr_val   = round(dff["UPI_Transactions"].corr(dff["ATM_Withdrawals"]), 3)
upi_growth = round(((dff["UPI_Transactions"].iloc[-1] / dff["UPI_Transactions"].iloc[0]) - 1) * 100, 1)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-blue">
    <div class="kpi-label">Latest UPI Volume</div>
    <div class="kpi-value">{latest_upi:,.0f}M</div>
    <div class="kpi-sub">Monthly transactions</div>
    <div class="kpi-badge badge-up">▲ {upi_growth:,.0f}% since Jan 2018</div>
  </div>
  <div class="kpi-card kpi-amber">
    <div class="kpi-label">Peak ATM Withdrawals</div>
    <div class="kpi-value">{peak_atm:,.0f}M</div>
    <div class="kpi-sub">All-time monthly peak</div>
    <div class="kpi-badge badge-down">▼ Declining post-2020</div>
  </div>
  <div class="kpi-card kpi-red">
    <div class="kpi-label">UPI–ATM Correlation</div>
    <div class="kpi-value">{corr_val}</div>
    <div class="kpi-sub">Pearson r coefficient</div>
    <div class="kpi-badge badge-neg">Strong inverse relationship</div>
  </div>
  <div class="kpi-card kpi-teal">
    <div class="kpi-label">Observations</div>
    <div class="kpi-value">{len(dff)}</div>
    <div class="kpi-sub">Monthly data points</div>
    <div class="kpi-badge badge-up">Jan {year_range[0]} – present</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Trend Analysis",
    "🔗  Correlation",
    "📊  Comparative",
    "🔍  Strategic Insights",
])

# ─────────────────────────────────────────────────────────────────
# TAB 1 — Trend Analysis
# ─────────────────────────────────────────────────────────────────
VAR_COLORS = {
    "UPI_Transactions": COLOR_BLUE,
    "ATM_Withdrawals":  COLOR_AMBER,
    "DebitCard_POS":    COLOR_TEAL,
    "IMPS":             COLOR_RED,
}
VAR_LABELS = {
    "UPI_Transactions": "UPI Transactions",
    "ATM_Withdrawals":  "ATM Withdrawals",
    "DebitCard_POS":    "Debit Card POS",
    "IMPS":             "IMPS",
}

with tab1:
    fig = go.Figure()

    for var in show_vars:
        fig.add_trace(go.Scatter(
            x=dff["date"], y=dff[var],
            name=VAR_LABELS[var],
            mode="lines+markers",
            line=dict(color=VAR_COLORS[var], width=2),
            marker=dict(size=3, color=VAR_COLORS[var]),
            hovertemplate=f"<b>{VAR_LABELS[var]}</b><br>%{{x|%b %Y}}: %{{y:,.0f}}M<extra></extra>",
        ))
        if show_ma:
            fig.add_trace(go.Scatter(
                x=dff["date"], y=dff[f"{var}_MA3"],
                name=f"{VAR_LABELS[var]} (3M MA)",
                mode="lines",
                line=dict(color=VAR_COLORS[var], width=1.5, dash="dot"),
                opacity=0.5,
                hovertemplate=f"<b>{VAR_LABELS[var]} (3M avg)</b><br>%{{x|%b %Y}}: %{{y:,.0f}}M<extra></extra>",
            ))

    # Event markers
    if show_events:
        for _, row in events.iterrows():
            if row["date"].year >= year_range[0] and row["date"].year <= year_range[1]:
                fig.add_vline(
                    x=row["date"].timestamp() * 1000,
                    line_dash="dash", line_color="rgba(255,255,255,0.25)", line_width=1,
                )
                fig.add_annotation(
                    x=row["date"], y=1, yref="paper",
                    text=f"  {row['Event']}",
                    showarrow=False, xanchor="left",
                    font=dict(size=10, color="rgba(255,255,255,0.5)"),
                    bgcolor="rgba(19,25,41,0.8)",
                    bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
                    borderpad=4,
                )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="Payment Volume Trends — Monthly (Millions)",
        xaxis_title="",
        yaxis_title="Transactions (Million)",
        yaxis_type="log" if log_scale else "linear",
        height=420,
        legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h", y=-0.18),
    )
    st.plotly_chart(fig, use_container_width=True)

    # YoY growth sub-chart for UPI
    st.markdown('<div class="section-header">Year-over-Year Growth</div>', unsafe_allow_html=True)
    dff["UPI_YoY"] = dff["UPI_Transactions"].pct_change(12) * 100
    dff["ATM_YoY"] = dff["ATM_Withdrawals"].pct_change(12) * 100

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=dff["date"], y=dff["UPI_YoY"],
        name="UPI YoY %",
        marker_color=COLOR_BLUE,
        opacity=0.85,
        hovertemplate="<b>UPI Growth</b><br>%{x|%b %Y}: %{y:.1f}%<extra></extra>",
    ))
    fig2.add_trace(go.Bar(
        x=dff["date"], y=dff["ATM_YoY"],
        name="ATM YoY %",
        marker_color=COLOR_AMBER,
        opacity=0.85,
        hovertemplate="<b>ATM Change</b><br>%{x|%b %Y}: %{y:.1f}%<extra></extra>",
    ))
    fig2.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_width=1)
    fig2.update_layout(
        **PLOTLY_LAYOUT,
        title="Annual Growth Rate Comparison (%)",
        barmode="group", height=280,
        legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h", y=-0.25),
        yaxis_title="YoY Change (%)",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# TAB 2 — Correlation
# ─────────────────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns([1, 1])

    with col_a:
        # Correlation heatmap
        corr_df = dff[["UPI_Transactions", "ATM_Withdrawals", "DebitCard_POS", "IMPS"]].corr()
        heat = px.imshow(
            corr_df,
            text_auto=".3f",
            color_continuous_scale=[
                [0.0, "#EB5757"],
                [0.5, "#131929"],
                [1.0, "#2F80ED"],
            ],
            zmin=-1, zmax=1,
            title="Correlation Matrix",
        )
        heat.update_layout(
            **PLOTLY_LAYOUT, height=360,
            coloraxis_colorbar=dict(
                tickfont=dict(color="#8A94A8"),
                title=dict(text="r", font=dict(color="#8A94A8")),
            ),
        )
        heat.update_traces(textfont=dict(size=12, color="#E8EDF5"))
        st.plotly_chart(heat, use_container_width=True)

    with col_b:
        # Scatter: UPI vs ATM
        scatter = px.scatter(
            dff,
            x="UPI_Transactions", y="ATM_Withdrawals",
            color="date",
            color_continuous_scale=["#1A2236", COLOR_BLUE],
            trendline="ols",
            title="UPI vs ATM — Scatter with OLS Trend",
            labels={
                "UPI_Transactions": "UPI Transactions (M)",
                "ATM_Withdrawals":  "ATM Withdrawals (M)",
            },
            hover_data={"date": "|%b %Y"},
        )
        scatter.update_traces(
            marker=dict(size=6, opacity=0.75),
            selector=dict(mode="markers"),
        )
        scatter.update_layout(
            **PLOTLY_LAYOUT, height=360,
            coloraxis_showscale=False,
        )
        st.plotly_chart(scatter, use_container_width=True)

    # Rolling 12-month correlation
    st.markdown('<div class="section-header">Rolling 12-Month Correlation</div>', unsafe_allow_html=True)
    dff["rolling_corr"] = (
        dff["UPI_Transactions"]
        .rolling(12)
        .corr(dff["ATM_Withdrawals"])
    )
    fig_rc = go.Figure()
    fig_rc.add_trace(go.Scatter(
        x=dff["date"], y=dff["rolling_corr"],
        fill="tozeroy",
        fillcolor="rgba(47,128,237,0.12)",
        line=dict(color=COLOR_BLUE, width=2),
        name="Rolling r",
        hovertemplate="<b>Rolling r</b>: %{y:.3f}<br>%{x|%b %Y}<extra></extra>",
    ))
    fig_rc.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_width=1)
    fig_rc.update_layout(
        **PLOTLY_LAYOUT,
        title="Rolling 12-Month Pearson r  (UPI vs ATM Withdrawals)",
        yaxis_title="Correlation (r)",
        height=260,
    )
    st.plotly_chart(fig_rc, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# TAB 3 — Comparative
# ─────────────────────────────────────────────────────────────────
with tab3:
    # Market share area chart
    dff_share = dff.copy()
    total_cols = ["UPI_Transactions", "ATM_Withdrawals", "DebitCard_POS", "IMPS"]
    dff_share["total"] = dff_share[total_cols].sum(axis=1)
    for col in total_cols:
        dff_share[f"{col}_pct"] = (dff_share[col] / dff_share["total"]) * 100

    fig_share = go.Figure()
    for var, color in VAR_COLORS.items():
        fig_share.add_trace(go.Scatter(
            x=dff_share["date"], y=dff_share[f"{var}_pct"],
            name=VAR_LABELS[var],
            mode="lines",
            stackgroup="one",
            line=dict(color=color, width=0.5),
            hovertemplate=f"<b>{VAR_LABELS[var]}</b>: %{{y:.1f}}%<br>%{{x|%b %Y}}<extra></extra>",
        ))
    fig_share.update_layout(
        **PLOTLY_LAYOUT,
        title="Payment Channel Market Share (%) — Stacked",
        yaxis_title="Share of Total Transactions (%)",
        height=360,
        legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h", y=-0.2),
    )
    st.plotly_chart(fig_share, use_container_width=True)

    # Annual aggregated bar
    st.markdown('<div class="section-header">Annual Aggregates</div>', unsafe_allow_html=True)
    dff["year"] = dff["date"].dt.year
    annual = dff.groupby("year")[total_cols].mean().reset_index()

    fig_ann = go.Figure()
    for var, color in VAR_COLORS.items():
        fig_ann.add_trace(go.Bar(
            x=annual["year"], y=annual[var],
            name=VAR_LABELS[var],
            marker_color=color,
            opacity=0.85,
            hovertemplate=f"<b>{VAR_LABELS[var]}</b><br>Avg/month: %{{y:,.0f}}M<extra></extra>",
        ))
    fig_ann.update_layout(
        **PLOTLY_LAYOUT,
        title="Average Monthly Volume by Year (Million Transactions)",
        barmode="group", height=320,
        legend=dict(**PLOTLY_LAYOUT["legend"], orientation="h", y=-0.25),
        yaxis_title="Avg Monthly Volume (M)",
    )
    st.plotly_chart(fig_ann, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# TAB 4 — Strategic Insights
# ─────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
      <div class="insight-title">🔵 Digital Substitution — Measurable but Inelastic</div>
      <div class="insight-body">
        UPI transactions have grown by over 14,000% since January 2018, now processing over 21,700 million
        monthly transactions. Despite this exponential rise, ATM withdrawal volumes have declined only
        modestly—suggesting that cash still maintains a <em>structural floor</em> in India's payments economy,
        particularly in rural and semi-urban segments.
      </div>
    </div>

    <div class="insight-box teal">
      <div class="insight-title">🟢 Structural Transformation — Not Replacement</div>
      <div class="insight-body">
        The −0.623 Pearson correlation between UPI and ATM usage indicates a strong inverse relationship,
        but one that is not fully substitutive. The evidence points to a <em>bifurcated ecosystem</em>:
        digital rails expanding for merchant payments and P2P transfers, while physical infrastructure
        persists for salary disbursal, daily wage labour, and informal sector transactions.
      </div>
    </div>

    <div class="insight-box amber">
      <div class="insight-title">🟡 COVID-19 as a Digital Catalyst</div>
      <div class="insight-body">
        The April 2020 lockdown created a sharp inflection: ATM withdrawals contracted significantly while
        UPI adoption accelerated. This behavioural shift proved <em>sticky</em>—post-COVID ATM volumes never
        fully recovered, while UPI grew at compounding rates, suggesting a permanent reorientation of
        consumer payment behaviour.
      </div>
    </div>

    <div class="insight-box red">
      <div class="insight-title">🔴 Implications for Banking Infrastructure Strategy</div>
      <div class="insight-body">
        Conventional banks face a dual mandate: maintain physical cash infrastructure for financial
        inclusion while investing in digital rails to remain competitive. The data suggests that
        CapEx reallocation from ATM networks toward UPI interoperability and merchant onboarding
        may represent the optimal strategic posture for 2024–2027.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Ecosystem Drivers</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="insight-box">
          <div class="insight-title">Demand-Side Drivers</div>
          <div class="insight-body">
            • Smartphone penetration (780M+ users)<br>
            • Rising digital literacy & Jan Dhan accounts<br>
            • Merchant QR code proliferation<br>
            • Post-COVID behavioural shift to contactless<br>
            • BNPL and credit-on-UPI adoption
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="insight-box teal">
          <div class="insight-title">Supply-Side & Policy Drivers</div>
          <div class="insight-body">
            • NPCI's zero-MDR policy on UPI<br>
            • RBI's digital payment vision 2025<br>
            • PM-WANI & rural broadband expansion<br>
            • Interoperability mandates & UPI 2.0 features<br>
            • Government DBT disbursements via digital rails
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#8A94A8;text-align:center;padding:8px 0'>
        Data Source: RBI DBIE — Payment System Indicators (Table 45) &amp; NPCI Monthly Statistics &nbsp;|&nbsp;
        Research: Arpita Maheshwari, MS25GF132, Term 2 — IBR Project
    </div>
    """, unsafe_allow_html=True)
