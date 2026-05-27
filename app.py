import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="India Banking Transformation Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("payments_data.csv")

    df["Month_Year"] = pd.to_datetime(df["Month_Year"])

    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("Dashboard Controls")

# Year Filter
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Month_Year"].dt.year.min()),
    int(df["Month_Year"].dt.year.max()),
    (
        int(df["Month_Year"].dt.year.min()),
        int(df["Month_Year"].dt.year.max())
    )
)

# Variable Selection
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

# Comparison Selector
comparison_var = st.sidebar.selectbox(
    "Compare UPI Against",
    [
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
)

# Scale Toggle
use_log = st.sidebar.toggle("Use Log Scale", value=False)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
filtered_df = df[
    (df["Month_Year"].dt.year >= year_range[0]) &
    (df["Month_Year"].dt.year <= year_range[1])
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("India Banking Transformation Dashboard")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.caption("Interactive analysis of India’s payment ecosystem using RBI DBIE and NPCI data")

st.markdown("---")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
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

atm_change = round(
    (
        (
            filtered_df["ATM_Withdrawals"].iloc[-1] /
            filtered_df["ATM_Withdrawals"].iloc[0]
        ) - 1
    ) * 100,
    1
)

corr_value = round(
    filtered_df["UPI_Transactions"].corr(
        filtered_df[comparison_var]
    ),
    3
)

with col1:
    st.metric(
        "UPI Growth",
        f"{upi_growth:,.1f}%",
        "Since Selected Period"
    )

with col2:
    st.metric(
        "ATM Withdrawal Change",
        f"{atm_change:,.1f}%",
        "Structural Shift"
    )

with col3:
    st.metric(
        f"UPI vs {comparison_var}",
        corr_value,
        "Relationship Strength"
    )

with col4:
    st.metric(
        "Observations",
        len(filtered_df),
        "Monthly Data"
    )

st.markdown("---")

# ---------------------------------------------------
# MAIN TREND ANALYSIS
# ---------------------------------------------------
st.subheader("Payment System Transformation Trends")

trend_fig = px.line(
    filtered_df,
    x="Month_Year",
    y=selected_variables,
    markers=True
)

trend_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Transaction Volume (Million)",
    hovermode="x unified",
    height=500
)

if use_log:
    trend_fig.update_yaxes(type="log")

st.plotly_chart(trend_fig, use_container_width=True)

# ---------------------------------------------------
# WHAT CHANGED SECTION
# ---------------------------------------------------
st.subheader("What Changed During This Period?")

upi_change = round(
    (
        (
            filtered_df["UPI_Transactions"].iloc[-1] -
            filtered_df["UPI_Transactions"].iloc[0]
        )
        /
        filtered_df["UPI_Transactions"].iloc[0]
    ) * 100,
    1
)

atm_decline = round(
    (
        (
            filtered_df["ATM_Withdrawals"].iloc[-1] -
            filtered_df["ATM_Withdrawals"].iloc[0]
        )
        /
        filtered_df["ATM_Withdrawals"].iloc[0]
    ) * 100,
    1
)

st.info(f"""
Between {year_range[0]} and {year_range[1]},
UPI transactions changed by {upi_change}% while ATM withdrawals changed by {atm_decline}%.

This suggests that digital payment adoption is increasing rapidly, but cash usage has not disappeared completely, indicating behavioural substitution rather than full cash elimination.
""")

# ---------------------------------------------------
# COMPARATIVE ANALYSIS
# ---------------------------------------------------
st.subheader("UPI Relationship Analysis")

comparison_fig = px.scatter(
    filtered_df,
    x="UPI_Transactions",
    y=comparison_var,
    trendline="ols"
)

comparison_fig.update_layout(
    xaxis_title="UPI Transactions",
    yaxis_title=comparison_var,
    height=500
)

st.plotly_chart(comparison_fig, use_container_width=True)

# ---------------------------------------------------
# PAYMENT SHARE ANALYSIS
# ---------------------------------------------------
st.subheader("Payment Ecosystem Share Analysis")

share_df = filtered_df.copy()

share_df["Total"] = (
    share_df["UPI_Transactions"] +
    share_df["ATM_Withdrawals"] +
    share_df["DebitCard_POS"] +
    share_df["IMPS"]
)

share_df["UPI Share"] = (
    share_df["UPI_Transactions"] /
    share_df["Total"]
) * 100

share_df["ATM Share"] = (
    share_df["ATM_Withdrawals"] /
    share_df["Total"]
) * 100

share_df["POS Share"] = (
    share_df["DebitCard_POS"] /
    share_df["Total"]
) * 100

share_df["IMPS Share"] = (
    share_df["IMPS"] /
    share_df["Total"]
) * 100

share_chart = px.area(
    share_df,
    x="Month_Year",
    y=[
        "UPI Share",
        "ATM Share",
        "POS Share",
        "IMPS Share"
    ]
)

share_chart.update_layout(
    yaxis_title="Share of Payment Ecosystem (%)",
    height=500
)

st.plotly_chart(share_chart, use_container_width=True)

# ---------------------------------------------------
# ROLLING CORRELATION
# ---------------------------------------------------
st.subheader("Rolling Correlation Analysis")

rolling_df = filtered_df.copy()

rolling_df["Rolling_Correlation"] = (
    rolling_df["UPI_Transactions"]
    .rolling(window=12)
    .corr(rolling_df["ATM_Withdrawals"])
)

rolling_chart = px.line(
    rolling_df,
    x="Month_Year",
    y="Rolling_Correlation"
)

rolling_chart.update_layout(
    yaxis_title="12-Month Rolling Correlation",
    height=450
)

st.plotly_chart(rolling_chart, use_container_width=True)

# ---------------------------------------------------
# INFRASTRUCTURE STRESS INDICATOR
# ---------------------------------------------------
st.subheader("Infrastructure Perspective")

if upi_growth > 500 and atm_change > -40:

    st.warning("""
Digital transactions are growing significantly faster than ATM withdrawals are declining.

This suggests that banks may currently face a dual-infrastructure burden:
maintaining cash infrastructure while simultaneously investing in digital payment ecosystems.
""")

else:

    st.success("""
The data suggests that digital substitution is occurring more uniformly across payment infrastructure.
""")

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------
st.subheader("Correlation Matrix")

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
    color_continuous_scale="Blues"
)

heatmap.update_layout(
    height=500
)

st.plotly_chart(heatmap, use_container_width=True)

# ---------------------------------------------------
# KEY TAKEAWAY GENERATOR
# ---------------------------------------------------
st.subheader("Key Takeaway Generator")

if corr_value < -0.5:

    st.info(f"""
The relationship between UPI transactions and {comparison_var}
shows a strong inverse relationship.

This may indicate measurable substitution effects between digital payment adoption and conventional banking activity.
""")

elif corr_value > 0.5:

    st.info(f"""
UPI transactions and {comparison_var}
appear to move together positively.

This may indicate complementary growth within India’s digital transaction ecosystem rather than direct substitution.
""")

else:

    st.info(f"""
The relationship between UPI transactions and {comparison_var}
appears moderate or mixed, suggesting that multiple ecosystem factors may influence the observed trends.
""")

# ---------------------------------------------------
# FUTURE ECOSYSTEM FACTORS
# ---------------------------------------------------
st.subheader("Potential External Drivers")

col_a, col_b = st.columns(2)

with col_a:

    st.write("""
### Demand-Side Drivers

- Smartphone penetration
- QR code adoption
- Digital literacy
- Consumer convenience
- Contactless payment preference
""")

with col_b:

    st.write("""
### Infrastructure & Policy Drivers

- RBI digital initiatives
- NPCI ecosystem expansion
- Internet accessibility
- Financial inclusion programs
- COVID behavioural shifts
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics"
)

