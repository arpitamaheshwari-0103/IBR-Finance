import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="India Banking Transformation Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    padding-top: 20px;
}

h1, h2, h3, h4 {
    color: white;
}

section[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
}

.metric-card {
    background: linear-gradient(135deg, #111827, #1F2937);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.25);
}

.insight-box {
    background-color: #111827;
    border-left: 5px solid #3B82F6;
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.small-text {
    color: #9CA3AF;
    font-size: 14px;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():

    df = pd.read_csv("payments_data.csv")

    df["Month_Year"] = pd.to_datetime(df["Month_Year"])

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title("🏦 Dashboard Controls")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Month_Year"].dt.year.min()),
    int(df["Month_Year"].dt.year.max()),
    (
        int(df["Month_Year"].dt.year.min()),
        int(df["Month_Year"].dt.year.max())
    )
)

selected_variables = st.sidebar.multiselect(
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

log_scale = st.sidebar.toggle("Use Log Scale", value=False)

show_markers = st.sidebar.toggle("Show Event Markers", value=True)

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
filtered_df = df[
    (df["Month_Year"].dt.year >= year_range[0]) &
    (df["Month_Year"].dt.year <= year_range[1])
]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🏦 India Banking Transformation Intelligence Dashboard")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.markdown("""
<div class='small-text'>
Interactive analytics dashboard using RBI DBIE and NPCI transaction data (2018–2026)
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

upi_growth = round(
    (
        (
            filtered_df["UPI_Transactions"].iloc[-1] /
            filtered_df["UPI_Transactions"].iloc[0]
        ) - 1
    ) * 100,
    1
)

corr_value = round(
    filtered_df["UPI_Transactions"].corr(
        filtered_df["ATM_Withdrawals"]
    ),
    3
)

with col1:
    st.metric(
        "Latest UPI Transactions",
        f"{filtered_df['UPI_Transactions'].iloc[-1]:,.0f} M",
        "+14,000%+ Growth"
    )

with col2:
    st.metric(
        "Peak ATM Withdrawals",
        f"{filtered_df['ATM_Withdrawals'].max():,.0f} M",
        "Gradual Decline"
    )

with col3:
    st.metric(
        "UPI-ATM Correlation",
        corr_value,
        "Inverse Relationship"
    )

with col4:
    st.metric(
        "Observations",
        len(filtered_df),
        "Monthly Data Points"
    )

st.markdown("---")

# ─────────────────────────────────────────────
# MAIN TREND CHART
# ─────────────────────────────────────────────
st.subheader("📈 Payment System Transformation Trends")

fig = px.line(
    filtered_df,
    x="Month_Year",
    y=selected_variables,
    markers=True,
    template="plotly_dark"
)

fig.update_layout(
    height=550,
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font=dict(color="white"),
    legend_title="Variables",
    xaxis_title="Year",
    yaxis_title="Transactions (Million)",
    hovermode="x unified"
)

if log_scale:
    fig.update_yaxes(type="log")

if show_markers:

    fig.add_vline(
        x="2020-04-01",
        line_dash="dash",
        line_color="red",
        annotation_text="COVID Shock"
    )

    fig.add_vline(
        x="2019-11-01",
        line_dash="dash",
        line_color="orange",
        annotation_text="RBI POS Reporting Change"
    )

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# STRATEGIC INSIGHT BOX
# ─────────────────────────────────────────────
st.markdown("""
<div class='insight-box'>
<h4>🔍 What This Suggests</h4>

The divergence between rapidly increasing UPI transactions and gradually declining ATM withdrawals suggests that India is witnessing behavioural payment substitution rather than complete cash elimination.

The findings indicate a broader transformation in banking infrastructure, transaction behaviour, and payment ecosystem dependence rather than just growth in digital transactions.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CORRELATION ANALYSIS
# ─────────────────────────────────────────────
st.subheader("🔗 Correlation Intelligence")

corr_df = filtered_df[
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
    color_continuous_scale="Blues",
    template="plotly_dark"
)

heatmap.update_layout(
    height=500,
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font=dict(color="white")
)

st.plotly_chart(heatmap, use_container_width=True)

# ─────────────────────────────────────────────
# COMPARATIVE ANALYSIS
# ─────────────────────────────────────────────
st.subheader("📊 Comparative Annual Analysis")

annual_df = filtered_df.copy()

annual_df["Year"] = annual_df["Month_Year"].dt.year

annual_summary = annual_df.groupby("Year")[
    [
        "UPI_Transactions",
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
].mean().reset_index()

bar_fig = px.bar(
    annual_summary,
    x="Year",
    y=selected_variables,
    barmode="group",
    template="plotly_dark"
)

bar_fig.update_layout(
    height=500,
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font=dict(color="white")
)

st.plotly_chart(bar_fig, use_container_width=True)

# ─────────────────────────────────────────────
# ATM INFRASTRUCTURE INSIGHT
# ─────────────────────────────────────────────
st.markdown("""
<div class='insight-box'>
<h4>🏧 Infrastructure Perspective</h4>

The study suggests that while digital transaction infrastructure is expanding exponentially, physical banking infrastructure cannot disappear immediately.

This indicates that banks face a dual challenge:
maintaining ATM infrastructure for financial inclusion while simultaneously investing heavily in digital payment ecosystems.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUTURE ECOSYSTEM FACTORS
# ─────────────────────────────────────────────
st.subheader("🌐 Ecosystem & External Drivers")

col_a, col_b = st.columns(2)

with col_a:
    st.info("""
### Demand-Side Drivers

- Smartphone penetration  
- Merchant QR adoption  
- Consumer convenience behaviour  
- Contactless transaction preference  
- Digital literacy growth  
""")

with col_b:
    st.info("""
### Policy & Infrastructure Drivers

- RBI digital initiatives  
- NPCI ecosystem expansion  
- Internet accessibility  
- Government digital push  
- Financial inclusion programs  
""")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics | MBA Research Dashboard"
)


