import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Payments Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────
# SIDEBAR FIX
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    min-width: 320px !important;
    max-width: 320px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────
st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0B0F1A;
    color: #E8EDF5;
    font-family: 'Arial', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
}

.kpi-card {
    background-color: #131929;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 10px;
}

.kpi-title {
    font-size: 12px;
    color: #8A94A8;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}

.insight-box {
    background-color: #131929;
    border-left: 4px solid #2F80ED;
    padding: 18px;
    border-radius: 10px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────
@st.cache_data
def load_data():

    df = pd.read_csv("payments_data.csv")

    df["date"] = pd.to_datetime(df["Month_Year"])

    events = pd.read_csv("event_markers.csv")
    events["date"] = pd.to_datetime(events["Date"])

    return df, events

df, events = load_data()

# ─────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────
with st.sidebar:

    st.title("🏦 India Payments")

    min_year = int(df["date"].dt.year.min())
    max_year = int(df["date"].dt.year.max())

    year_range = st.slider(
        "Select Year Range",
        min_year,
        max_year,
        (min_year, max_year)
    )

    selected_vars = st.multiselect(
        "Select Variables",
        [
            "UPI_Transactions",
            "ATM_Withdrawals",
            "DebitCard_POS",
            "IMPS"
        ],
        default=[
            "UPI_Transactions",
            "ATM_Withdrawals"
        ]
    )

    show_events = st.toggle("Show Event Markers", value=True)

# ─────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────
mask = (
    (df["date"].dt.year >= year_range[0]) &
    (df["date"].dt.year <= year_range[1])
)

dff = df[mask]

# ─────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────
st.title("🏦 India Payment Systems Intelligence")

st.markdown("""
### FinTech vs Conventional Banking Transformation Dashboard
Strategic analysis of India’s payment ecosystem using RBI DBIE and NPCI data.
""")

# ─────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

latest_upi = dff["UPI_Transactions"].iloc[-1]

peak_atm = dff["ATM_Withdrawals"].max()

corr_val = round(
    dff["UPI_Transactions"].corr(dff["ATM_Withdrawals"]),
    3
)

upi_growth = round(
    (
        (
            dff["UPI_Transactions"].iloc[-1] /
            dff["UPI_Transactions"].iloc[0]
        ) - 1
    ) * 100,
    1
)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Latest UPI Volume</div>
        <div class="kpi-value">{latest_upi:,.0f}M</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Peak ATM Withdrawals</div>
        <div class="kpi-value">{peak_atm:,.0f}M</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">UPI-ATM Correlation</div>
        <div class="kpi-value">{corr_val}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">UPI Growth Since 2018</div>
        <div class="kpi-value">{upi_growth:,.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# MAIN TREND CHART
# ─────────────────────────────────────────────────────
st.markdown("## 📈 Trend Analysis")

fig = go.Figure()

colors = {
    "UPI_Transactions": "#2F80ED",
    "ATM_Withdrawals": "#F2994A",
    "DebitCard_POS": "#27AE95",
    "IMPS": "#EB5757"
}

labels = {
    "UPI_Transactions": "UPI Transactions",
    "ATM_Withdrawals": "ATM Withdrawals",
    "DebitCard_POS": "Debit Card POS",
    "IMPS": "IMPS"
}

for var in selected_vars:

    fig.add_trace(
        go.Scatter(
            x=dff["date"],
            y=dff[var],
            mode="lines",
            name=labels[var],
            line=dict(
                color=colors[var],
                width=3
            )
        )
    )

if show_events:

    for _, row in events.iterrows():

        fig.add_vline(
            x=row["date"],
            line_dash="dash",
            line_color="gray"
        )

fig.update_layout(
    paper_bgcolor="#0B0F1A",
    plot_bgcolor="#0B0F1A",
    font=dict(color="white"),
    height=500,
    legend=dict(
        orientation="h",
        y=-0.2,
        bgcolor="rgba(0,0,0,0)"
    ),
    title="Payment System Trends"
)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────
# CORRELATION HEATMAP
# ─────────────────────────────────────────────────────
st.markdown("## 🔗 Correlation Analysis")

corr_df = dff[
    [
        "UPI_Transactions",
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
].corr()

heatmap = px.imshow(
    corr_df,
    text_auto=True,
    color_continuous_scale="Blues"
)

heatmap.update_layout(
    paper_bgcolor="#0B0F1A",
    plot_bgcolor="#0B0F1A",
    font=dict(color="white"),
    height=450
)

st.plotly_chart(heatmap, use_container_width=True)

# ─────────────────────────────────────────────────────
# COMPARATIVE ANALYSIS
# ─────────────────────────────────────────────────────
st.markdown("## 📊 Comparative Analysis")

annual = dff.copy()

annual["Year"] = annual["date"].dt.year

annual_summary = annual.groupby("Year")[
    [
        "UPI_Transactions",
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
].mean().reset_index()

bar_fig = go.Figure()

for var in selected_vars:

    bar_fig.add_trace(
        go.Bar(
            x=annual_summary["Year"],
            y=annual_summary[var],
            name=labels[var]
        )
    )

bar_fig.update_layout(
    paper_bgcolor="#0B0F1A",
    plot_bgcolor="#0B0F1A",
    font=dict(color="white"),
    barmode="group",
    height=450,
    legend=dict(
        orientation="h",
        y=-0.2
    )
)

st.plotly_chart(bar_fig, use_container_width=True)

# ─────────────────────────────────────────────────────
# STRATEGIC INSIGHTS
# ─────────────────────────────────────────────────────
st.markdown("## 🔍 Strategic Insights")

st.markdown("""
<div class="insight-box">
<b>Digital Substitution is Measurable but Inelastic</b><br><br>
Despite exponential UPI growth, ATM withdrawals have declined only gradually, suggesting that cash still maintains a structural role in India’s banking ecosystem.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>Banking Infrastructure is Structurally Transforming</b><br><br>
The findings suggest that banks may gradually shift capital allocation from physical ATM infrastructure toward digital transaction ecosystems and merchant onboarding.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>COVID Accelerated Behavioural Change</b><br><br>
Post-2020 transaction patterns suggest that digital payment adoption accelerated permanently after the COVID disruption period.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────
st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics | Research Project Dashboard"
)
