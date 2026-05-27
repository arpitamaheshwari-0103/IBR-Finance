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
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.sidebar.title("Explore the Study")

page = st.sidebar.radio(
    "Select Analysis Section",
    [
        "Executive Overview",
        "Trend Analysis",
        "Relationship Analysis",
        "Ecosystem Analysis",
        "Rolling Correlation",
        "Hidden Insights",
        "Strategic Implications"
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

comparison_var = st.sidebar.selectbox(
    "Relationship Variable",
    [
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
)

use_log = st.sidebar.toggle(
    "Use Log Scale",
    value=False
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[
    (df["Month_Year"].dt.year >= year_range[0]) &
    (df["Month_Year"].dt.year <= year_range[1])
]

# ---------------------------------------------------
# COMMON METRICS
# ---------------------------------------------------

corr_value = round(
    filtered_df["UPI_Transactions"].corr(
        filtered_df[comparison_var]
    ),
    3
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("India Banking Transformation Dashboard")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.caption(
    "Analytical exploration of India’s banking transformation using RBI DBIE and NPCI transaction data"
)

st.markdown("---")

# ===================================================
# EXECUTIVE OVERVIEW
# ===================================================

if page == "Executive Overview":

    st.subheader("Executive Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### Digital Transaction Expansion

The study observes strong acceleration in digital transaction systems, particularly after 2020, driven by wider ecosystem adoption and behavioural shifts.
""")

    with col2:

        st.info("""
### Conventional Banking Activity

Despite rapid digital expansion, conventional banking channels such as ATM withdrawals continue at meaningful levels across the observed period.
""")

    col3, col4 = st.columns(2)

    with col3:

        st.info("""
### Payment Ecosystem Transition

The findings suggest coexistence between digital and cash systems rather than immediate elimination of conventional transaction behaviour.
""")

    with col4:

        st.info("""
### Study Coverage

Monthly transaction-level analysis covering UPI, ATM withdrawals, Debit Card POS transactions, and IMPS data from 2018–2026.
""")

    st.markdown("---")

    st.subheader("Core Research Perspective")

    st.success("""
The study does not simply examine digital payment growth.

Instead, it explores how India’s banking ecosystem is transitioning structurally, behaviourally, and operationally as digital transaction systems expand alongside conventional banking infrastructure.
""")

# ===================================================
# TREND ANALYSIS
# ===================================================

elif page == "Trend Analysis":

    st.subheader("Payment System Transformation Trends")

    trend_fig = px.line(
        filtered_df,
        x="Month_Year",
        y=[
            "UPI_Transactions",
            "ATM_Withdrawals",
            "DebitCard_POS",
            "IMPS"
        ],
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

    st.markdown("### Key Observation")

    st.info("""
Digital transaction systems expanded significantly during the observed period, particularly after 2020. However, conventional banking activities continued despite rapid digital acceleration.
""")

    st.markdown("### Strategic Interpretation")

    st.success("""
The findings suggest gradual behavioural substitution rather than complete replacement of conventional banking systems.
""")

    st.markdown("### Possible Implication")

    st.warning("""
Banks may continue managing both physical and digital transaction ecosystems simultaneously during the transition period.
""")

# ===================================================
# RELATIONSHIP ANALYSIS
# ===================================================

elif page == "Relationship Analysis":

    st.subheader("UPI Relationship Analysis")

    comparison_fig = px.scatter(
        filtered_df,
        x="UPI_Transactions",
        y=comparison_var
    )

    comparison_fig.update_layout(
        xaxis_title="UPI Transactions",
        yaxis_title=comparison_var,
        height=550
    )

    st.plotly_chart(comparison_fig, use_container_width=True)

    st.markdown("### Relationship Insight")

    if corr_value < -0.5:

        st.info(f"""
The relationship between UPI transactions and {comparison_var} appears strongly negative during the selected period.

This may suggest measurable substitution effects between digital transaction adoption and conventional banking activity.
""")

    elif corr_value > 0.5:

        st.info(f"""
UPI transactions and {comparison_var} appear to move together positively.

This may indicate complementary ecosystem growth rather than direct substitution.
""")

    else:

        st.info(f"""
The relationship between UPI transactions and {comparison_var} appears moderate or mixed.

This suggests that multiple ecosystem and behavioural factors may influence the observed trends simultaneously.
""")

# ===================================================
# ECOSYSTEM ANALYSIS
# ===================================================

elif page == "Ecosystem Analysis":

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
        height=550
    )

    st.plotly_chart(share_chart, use_container_width=True)

    st.markdown("### Ecosystem Insight")

    st.info("""
The composition of India’s payment ecosystem changed significantly during the observed period, with UPI gradually occupying a larger transaction share.

This suggests ecosystem-wide digital integration rather than isolated payment platform growth.
""")

# ===================================================
# ROLLING CORRELATION
# ===================================================

elif page == "Rolling Correlation":

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
        height=550
    )

    st.plotly_chart(rolling_chart, use_container_width=True)

    st.markdown("### Dynamic Relationship Interpretation")

    st.info("""
The rolling correlation analysis helps observe how the relationship between UPI transactions and ATM withdrawals evolved over time rather than remaining static.

This enables exploration of whether substitution effects strengthened, weakened, or stabilised during different phases of India’s banking transformation.
""")

# ===================================================
# HIDDEN INSIGHTS
# ===================================================

elif page == "Hidden Insights":

    st.subheader("Insights Beyond the Obvious")

    st.success("""
### Cash Persistence Despite Digital Expansion

Even with rapid digital transaction growth, cash infrastructure continues to remain structurally relevant within the Indian economy.
""")

    st.success("""
### Infrastructure Duality

Banks may need to simultaneously finance ATM infrastructure and digital payment ecosystems during the transition phase.
""")

    st.success("""
### Behavioural Transition Lag

Digital transaction adoption may occur faster than behavioural trust transition across all segments of the economy.
""")

    st.success("""
### Ecosystem Transformation

The findings suggest broader transaction ecosystem restructuring rather than growth of a single payment platform alone.
""")

    st.success("""
### Financial Inclusion Layer

Persistent ATM activity may reflect uneven digital penetration across demographic or geographic segments.
""")

# ===================================================
# STRATEGIC IMPLICATIONS
# ===================================================

elif page == "Strategic Implications":

    st.subheader("Strategic Banking Implications")

    st.warning("""
### Banking Infrastructure Planning

Banks may need to optimise allocation between physical cash infrastructure and digital ecosystem investment.
""")

    st.warning("""
### Digital Ecosystem Expansion

Future banking competitiveness may increasingly depend on digital transaction ecosystem participation and merchant integration.
""")

    st.warning("""
### Financial Inclusion Considerations

Conventional banking systems may continue remaining relevant within segments experiencing lower digital accessibility.
""")

    st.warning("""
### Policy & Regulatory Relevance

The observed transition may influence future financial infrastructure planning and digital banking policy direction.
""")

    st.warning("""
### Long-Term Transformation Perspective

The findings suggest that India’s banking transformation reflects gradual ecosystem evolution rather than immediate disruption of conventional banking systems.
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics"
)
