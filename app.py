import streamlit as st
import pandas as pd
import plotly.express as px

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

comparison_var = st.sidebar.selectbox(
    "Compare UPI Against",
    [
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
)

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

st.caption("Interactive analysis using RBI DBIE and NPCI data")

st.markdown("---")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

upi_growth = round(
    (
        (
            filtered_df["UPI_Transactions"].iloc[-1]
            /
            filtered_df["UPI_Transactions"].iloc[0]
        ) - 1
    ) * 100,
    1
)

atm_change = round(
    (
        (
            filtered_df["ATM_Withdrawals"].iloc[-1]
            /
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
        f"{upi_growth}%",
        "Selected Period"
    )

with col2:
    st.metric(
        "ATM Withdrawal Change",
        f"{atm_change}%",
        "Selected Period"
    )

with col3:
    st.metric(
        f"UPI vs {comparison_var}",
        corr_value
    )

with col4:
    st.metric(
        "Observations",
        len(filtered_df)
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
# RESEARCH INSIGHT EXPLORER
# ---------------------------------------------------
st.subheader("Research Insight Explorer")

st.markdown("""
Select a research theme or ask a question to explore insights derived from the study.
""")

insight_option = st.selectbox(
    "Choose an Insight Area",
    [
        "UPI vs ATM Relationship",
        "COVID Impact on Digital Payments",
        "Infrastructure Implications",
        "Digital Payment Ecosystem",
        "ATM Persistence Despite UPI Growth",
        "Future Banking Implications"
    ]
)

if insight_option == "UPI vs ATM Relationship":

    st.info(f"""
The selected period shows a correlation of {corr_value} between UPI transactions and ATM withdrawals.

The findings suggest that as UPI transactions expanded rapidly, ATM withdrawals gradually weakened. However, ATM activity did not disappear completely, indicating coexistence between digital payments and cash usage.
""")

elif insight_option == "COVID Impact on Digital Payments":

    st.info("""
Transaction trends after 2020 suggest that digital payment adoption accelerated significantly during and after the COVID period.

The data indicates stronger behavioural reliance on digital transactions after the pandemic disruption.
""")

elif insight_option == "Infrastructure Implications":

    st.info("""
The study suggests that banks may face a dual infrastructure challenge:
maintaining physical ATM infrastructure while simultaneously investing in digital transaction ecosystems.
""")

elif insight_option == "Digital Payment Ecosystem":

    st.info("""
The findings indicate that UPI growth is occurring alongside expansion in other digital transaction systems such as IMPS and POS transactions.

This may suggest ecosystem-wide digital integration rather than isolated platform growth.
""")

elif insight_option == "ATM Persistence Despite UPI Growth":

    st.info("""
Despite exponential growth in UPI transactions, ATM withdrawals continue at meaningful levels.

This may indicate that cash dependency still persists across certain economic segments and transaction categories.
""")

elif insight_option == "Future Banking Implications":

    st.info("""
The observed payment trends may influence future banking strategy in areas such as ATM infrastructure planning, digital investment allocation, merchant onboarding, and transaction ecosystem expansion.
""")

# ---------------------------------------------------
# USER QUERY SECTION
# ---------------------------------------------------
st.markdown("---")

st.subheader("Ask the Dashboard")

user_query = st.text_input(
    "Ask a question about the study"
)

if user_query:

    query = user_query.lower()

    if "atm" in query and "upi" in query:

        st.success("""
The study finds a negative relationship between UPI transactions and ATM withdrawals, suggesting measurable digital substitution effects within the banking ecosystem.
""")

    elif "covid" in query:

        st.success("""
The data suggests digital transaction growth accelerated significantly after 2020, indicating behavioural changes following the COVID disruption period.
""")

    elif "future" in query or "banking" in query:

        st.success("""
The findings may have implications for banking infrastructure strategy, particularly regarding digital ecosystem investment and ATM network optimization.
""")

    elif "cash" in query:

        st.success("""
The findings suggest that cash usage continues to persist despite rapid digital growth, indicating coexistence rather than immediate elimination of cash transactions.
""")

    else:

        st.warning("""
No direct insight found for this query.

Try asking about:
- UPI
- ATM
- COVID
- banking strategy
- cash usage
- infrastructure
""")

# ---------------------------------------------------
# COMPARATIVE ANALYSIS
# ---------------------------------------------------
st.subheader("UPI Relationship Analysis")

comparison_fig = px.scatter(
    filtered_df,
    x="UPI_Transactions",
    y=comparison_var
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
# CORRELATION MATRIX
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
# EXTERNAL DRIVERS
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
