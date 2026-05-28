import streamlit as st
import pandas as pd
import plotly.express as px

# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="India Banking Transformation Dashboard",
    layout="wide"
)

# ===================================================
# LOAD DATA
# ===================================================

@st.cache_data
def load_data():

    df = pd.read_csv("payments_data.csv")

    df["Month_Year"] = pd.to_datetime(df["Month_Year"])

    return df

df = load_data()

# ===================================================
# SIDEBAR
# ===================================================

st.sidebar.title("Banking Transformation Navigator")

page = st.sidebar.radio(
    "Select Analytical Section",
    [
        "Transformation Overview",
        "Transaction Landscape",
        "Payment Behaviour Dynamics",
        "Digital Ecosystem Shift",
        "Transition Momentum Analysis",
        "Structural Banking Insights",
        "Strategic Banking Outlook"
    ]
)

st.sidebar.markdown("---")

year_range = st.sidebar.slider(
    "Select Time Period",
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

comparison_variables = st.sidebar.multiselect(
    "Compare UPI With",
    [
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ],
    default=[
        "ATM_Withdrawals",
        "DebitCard_POS"
    ]
)

use_log = st.sidebar.toggle(
    "Use Log Scale",
    value=False
)

# ===================================================
# FILTER DATA
# ===================================================

filtered_df = df[
    (df["Month_Year"].dt.year >= year_range[0]) &
    (df["Month_Year"].dt.year <= year_range[1])
]

# ===================================================
# HEADER
# ===================================================

st.title("India Banking Transformation Dashboard")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.caption(
    "Interactive analytical exploration of India’s evolving payment ecosystem"
)

st.markdown("---")

# ===================================================
# KPI SECTION
# ===================================================

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
        filtered_df["ATM_Withdrawals"]
    ),
    3
)

with col1:

    st.metric(
        "Digital Transaction Expansion",
        f"{upi_growth}%",
        "Strong acceleration observed"
    )

with col2:

    st.metric(
        "Cash Infrastructure Persistence",
        f"{atm_change}%",
        "Conventional channels remain active"
    )

with col3:

    st.metric(
        "Payment Behaviour Correlation",
        corr_value,
        "Digital–cash interaction observed"
    )

with col4:

    st.metric(
        "Research Coverage",
        len(filtered_df),
        "Monthly transaction dataset"
    )

st.markdown("---")

# ===================================================
# TRANSFORMATION OVERVIEW
# ===================================================

if page == "Transformation Overview":

    st.subheader("Transformation Overview")

    overview_fig = px.line(
        filtered_df,
        x="Month_Year",
        y=[
            "UPI_Transactions",
            "ATM_Withdrawals"
        ],
        markers=True
    )

    overview_fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Transaction Volume (Million)",
        hovermode="x unified",
        height=550
    )

    if use_log:
        overview_fig.update_yaxes(type="log")

    st.plotly_chart(overview_fig, use_container_width=True)

    st.markdown("### Strategic Observation")

    st.info("""
The findings indicate that digital payment systems expanded significantly across the observed period, while conventional banking channels continued operating at meaningful levels.

This suggests structural coexistence rather than immediate replacement within India’s transaction ecosystem.
""")

# ===================================================
# TRANSACTION LANDSCAPE
# ===================================================

elif page == "Transaction Landscape":

    st.subheader("Transaction Landscape")

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
        height=550
    )

    if use_log:
        trend_fig.update_yaxes(type="log")

    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("### Analytical Interpretation")

    st.success("""
The transaction landscape demonstrates rapid digital transaction acceleration, particularly after 2020, while conventional banking activity declined more gradually.

This may indicate behavioural payment substitution occurring faster than infrastructure transition.
""")

# ===================================================
# PAYMENT BEHAVIOUR DYNAMICS
# ===================================================

elif page == "Payment Behaviour Dynamics":

    st.subheader("Payment Behaviour Dynamics")

    for variable in comparison_variables:

        st.markdown(f"#### UPI vs {variable}")

        comparison_fig = px.scatter(
            filtered_df,
            x="UPI_Transactions",
            y=variable
        )

        comparison_fig.update_layout(
            xaxis_title="UPI Transactions",
            yaxis_title=variable,
            height=450
        )

        st.plotly_chart(comparison_fig, use_container_width=True)

        corr_dynamic = round(
            filtered_df["UPI_Transactions"].corr(
                filtered_df[variable]
            ),
            3
        )

        st.info(f"""
Correlation between UPI transactions and {variable}: {corr_dynamic}

The observed relationship may reflect changing transaction behaviour patterns within India’s evolving banking ecosystem.
""")

# ===================================================
# DIGITAL ECOSYSTEM SHIFT
# ===================================================

elif page == "Digital Ecosystem Shift":

    st.subheader("Digital Ecosystem Shift")

    share_df = filtered_df.copy()

    share_df["Total"] = (
        share_df["UPI_Transactions"] +
        share_df["ATM_Withdrawals"] +
        share_df["DebitCard_POS"] +
        share_df["IMPS"]
    )

    share_df["UPI Share"] = (
        share_df["UPI_Transactions"]
        /
        share_df["Total"]
    ) * 100

    share_df["ATM Share"] = (
        share_df["ATM_Withdrawals"]
        /
        share_df["Total"]
    ) * 100

    share_df["POS Share"] = (
        share_df["DebitCard_POS"]
        /
        share_df["Total"]
    ) * 100

    share_df["IMPS Share"] = (
        share_df["IMPS"]
        /
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
        height=550
    )

    st.plotly_chart(share_chart, use_container_width=True)

    st.markdown("### Ecosystem Interpretation")

    st.info("""
The composition of India’s transaction ecosystem shifted significantly during the observed period, with digital platforms gradually occupying larger transaction shares.

This suggests ecosystem-wide transformation rather than isolated payment platform growth.
""")

# ===================================================
# TRANSITION MOMENTUM ANALYSIS
# ===================================================

elif page == "Transition Momentum Analysis":

    st.subheader("Transition Momentum Analysis")

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
        height=550
    )

    st.plotly_chart(rolling_chart, use_container_width=True)

    st.markdown("### Dynamic Transition Interpretation")

    st.info("""
The rolling correlation analysis allows observation of how the relationship between digital and conventional transaction systems evolved across different periods.

This helps identify whether behavioural substitution effects strengthened, weakened, or stabilised over time.
""")

# ===================================================
# STRUCTURAL BANKING INSIGHTS
# ===================================================

elif page == "Structural Banking Insights":

    st.subheader("Structural Banking Insights")

    st.success("""
### Cash Persistence Despite Digital Expansion

Even with strong digital transaction growth, cash infrastructure continues to remain structurally relevant within the Indian economy.
""")

    st.success("""
### Infrastructure Duality

Banks may need to simultaneously finance ATM infrastructure and digital payment ecosystems during the transition phase.
""")

    st.success("""
### Behavioural Transition Lag

Digital transaction adoption may occur faster than behavioural trust transition across all economic segments.
""")

    st.success("""
### Financial Inclusion Layer

Persistent ATM activity may reflect uneven digital penetration across demographic or geographic segments.
""")

    st.success("""
### Ecosystem Restructuring

The findings suggest broader transaction ecosystem transformation rather than growth of a single payment platform alone.
""")

# ===================================================
# STRATEGIC BANKING OUTLOOK
# ===================================================

elif page == "Strategic Banking Outlook":

    st.subheader("Strategic Banking Outlook")

    st.warning("""
### Banking Infrastructure Allocation

Banks may increasingly need to optimise allocation between physical transaction infrastructure and digital ecosystem investment.
""")

    st.warning("""
### Merchant Ecosystem Expansion

Future transaction competitiveness may depend significantly on merchant onboarding and ecosystem integration strategies.
""")

    st.warning("""
### Financial Inclusion Considerations

Conventional banking systems may continue remaining relevant within segments experiencing lower digital accessibility.
""")

    st.warning("""
### Long-Term Banking Transformation

The findings suggest gradual banking ecosystem evolution rather than immediate disruption of conventional banking systems.
""")

    st.warning("""
### Strategic Industry Relevance

The transition observed in the study may influence future banking strategy, fintech partnerships, transaction infrastructure planning, and policy direction.
""")

# ===================================================
# FOOTER
# ===================================================

st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics"
)
