import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

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

    payments_df = pd.read_csv("payments_data.csv")

    payments_df["Month_Year"] = pd.to_datetime(
        payments_df["Month_Year"]
    )

    # Additional RBI Infrastructure Files
    old_format = pd.read_csv("Old_Format.csv")
    sheet1 = pd.read_csv("Sheet1.csv")
    new_format = pd.read_csv("New_Format.csv")

    return payments_df, old_format, sheet1, new_format

payments_df, old_format, sheet1, new_format = load_data()

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
        "Infrastructure Evolution",
        "Strategic Banking Outlook"
    ]
)

st.sidebar.markdown("---")

year_range = st.sidebar.slider(
    "Select Time Period",
    int(payments_df["Month_Year"].dt.year.min()),
    int(payments_df["Month_Year"].dt.year.max()),
    (
        int(payments_df["Month_Year"].dt.year.min()),
        int(payments_df["Month_Year"].dt.year.max())
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

forecast_variable = st.sidebar.selectbox(
    "Forecast Variable",
    [
        "UPI_Transactions",
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
)

use_log = st.sidebar.toggle(
    "Use Log Scale",
    value=False
)

# ===================================================
# FILTER DATA
# ===================================================

filtered_df = payments_df[
    (payments_df["Month_Year"].dt.year >= year_range[0]) &
    (payments_df["Month_Year"].dt.year <= year_range[1])
]

# ===================================================
# HEADER
# ===================================================

st.title("India Banking Transformation Dashboard")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.caption(
    "Interactive analytical exploration of India’s evolving banking and payment ecosystem"
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
        "Acceleration observed"
    )

with col2:

    st.metric(
        "Cash Infrastructure Persistence",
        f"{atm_change}%",
        "Conventional systems remain active"
    )

with col3:

    st.metric(
        "Payment Behaviour Correlation",
        corr_value,
        "Digital–cash interaction"
    )

with col4:

    st.metric(
        "Research Coverage",
        len(filtered_df),
        "Monthly observations"
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
        height=550,
        hovermode="x unified"
    )

    if use_log:
        overview_fig.update_yaxes(type="log")

    st.plotly_chart(
        overview_fig,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
Digital transaction systems expanded rapidly across the observed period, while conventional banking channels continued operating at meaningful levels.

This suggests structural coexistence between digital transactions and cash infrastructure within India’s banking ecosystem.
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
        height=550,
        hovermode="x unified"
    )

    if use_log:
        trend_fig.update_yaxes(type="log")

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    # ------------------------------------------------
    # PERFORMANCE SNAPSHOT
    # ------------------------------------------------

    st.subheader("Payment System Performance Snapshot")

    snapshot = []

    for variable in selected_variables:

        latest = filtered_df[variable].iloc[-1]

        previous = filtered_df[variable].iloc[-13]

        yoy = round(
            ((latest - previous) / previous) * 100,
            2
        )

        if yoy > 20:
            trend = "Accelerating"

        elif yoy > 0:
            trend = "Growing"

        else:
            trend = "Weakening"

        snapshot.append({
            "Variable": variable,
            "Latest Value": round(latest, 2),
            "YoY Change (%)": yoy,
            "Trend": trend
        })

    snapshot_df = pd.DataFrame(snapshot)

    st.dataframe(
        snapshot_df,
        use_container_width=True
    )

    # ------------------------------------------------
    # DYNAMIC INSIGHT
    # ------------------------------------------------

    top_growth = snapshot_df.sort_values(
        by="YoY Change (%)",
        ascending=False
    ).iloc[0]

    st.markdown("### Key Strategic Takeaway")

    st.caption(f"""
{top_growth['Variable']} currently demonstrates the strongest transaction momentum within the selected period, suggesting stronger ecosystem acceleration relative to other payment systems.
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
            y=variable,
            trendline="ols"
        )

        comparison_fig.update_layout(
            height=450
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )

        corr_dynamic = round(
            filtered_df["UPI_Transactions"].corr(
                filtered_df[variable]
            ),
            3
        )

        if corr_dynamic < -0.5:

            insight = (
                "The observed inverse relationship may indicate "
                "measurable substitution effects between digital "
                "transactions and conventional banking behaviour."
            )

        elif corr_dynamic > 0.5:

            insight = (
                "The positive relationship may indicate ecosystem-wide "
                "transaction expansion rather than direct substitution."
            )

        else:

            insight = (
                "The relationship appears moderate, suggesting multiple "
                "ecosystem and behavioural factors may influence transaction patterns."
            )

        st.markdown("### Key Strategic Takeaway")

        st.caption(insight)

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
        height=550
    )

    st.plotly_chart(
        share_chart,
        use_container_width=True
    )

    # ------------------------------------------------
    # MARKET SHARE TABLE
    # ------------------------------------------------

    latest = share_df.iloc[-1]

    market_share = pd.DataFrame({
        "Payment System": [
            "UPI",
            "ATM",
            "POS",
            "IMPS"
        ],

        "Market Share (%)": [
            round(latest["UPI Share"], 2),
            round(latest["ATM Share"], 2),
            round(latest["POS Share"], 2),
            round(latest["IMPS Share"], 2)
        ]
    })

    st.subheader("Latest Payment System Composition")

    st.dataframe(
        market_share,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
The transaction ecosystem composition shifted significantly during the observed period, with digital platforms gradually occupying larger transaction shares.

This suggests broader ecosystem-wide digital integration rather than isolated platform growth.
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
        .corr(
            rolling_df["ATM_Withdrawals"]
        )
    )

    rolling_chart = px.line(
        rolling_df,
        x="Month_Year",
        y="Rolling_Correlation"
    )

    rolling_chart.update_layout(
        height=550
    )

    st.plotly_chart(
        rolling_chart,
        use_container_width=True
    )

    # ------------------------------------------------
    # PRE VS POST COVID
    # ------------------------------------------------

    st.subheader("Pre vs Post COVID Snapshot")

    pre_covid = filtered_df[
        filtered_df["Month_Year"] < "2020-03-01"
    ]

    post_covid = filtered_df[
        filtered_df["Month_Year"] >= "2020-03-01"
    ]

    comparison_table = pd.DataFrame({

        "Metric": [
            "Average UPI Transactions",
            "Average ATM Withdrawals"
        ],

        "Pre-COVID": [
            round(pre_covid["UPI_Transactions"].mean(), 2),
            round(pre_covid["ATM_Withdrawals"].mean(), 2)
        ],

        "Post-COVID": [
            round(post_covid["UPI_Transactions"].mean(), 2),
            round(post_covid["ATM_Withdrawals"].mean(), 2)
        ]
    })

    st.dataframe(
        comparison_table,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
The transition momentum analysis suggests that digital transaction acceleration strengthened significantly after the COVID period, indicating behavioural and ecosystem-level shifts in transaction preferences.
""")

# ===================================================
# INFRASTRUCTURE EVOLUTION
# ===================================================

elif page == "Infrastructure Evolution":

    st.subheader("Infrastructure Evolution")

    infrastructure_data = pd.DataFrame({

        "Infrastructure Indicator": [
            "ATM Network",
            "POS Ecosystem",
            "Digital Acceptance Infrastructure",
            "Merchant Payment Systems"
        ],

        "Observed Direction": [
            "Gradual structural adjustment",
            "Expansion observed",
            "Rapid ecosystem expansion",
            "Growing digital integration"
        ],

        "Strategic Relevance": [
            "Physical banking persistence",
            "Merchant digitisation",
            "Digital ecosystem penetration",
            "Transaction ecosystem evolution"
        ]
    })

    st.dataframe(
        infrastructure_data,
        use_container_width=True
    )

    # ------------------------------------------------
    # INFRASTRUCTURE VISUAL
    # ------------------------------------------------

    infra_chart = px.bar(
        infrastructure_data,
        x="Infrastructure Indicator",
        y=[1, 1, 1, 1]
    )

    infra_chart.update_layout(
        height=450,
        showlegend=False,
        yaxis_visible=False
    )

    st.plotly_chart(
        infra_chart,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
The broader infrastructure indicators suggest that India’s banking transformation involves not only transaction digitisation, but also restructuring of payment acceptance systems and banking support infrastructure.
""")

# ===================================================
# STRATEGIC BANKING OUTLOOK
# ===================================================

elif page == "Strategic Banking Outlook":

    st.subheader("Strategic Banking Outlook")

    forecast_df = filtered_df.copy()

    forecast_df = forecast_df.reset_index()

    X = np.arange(
        len(forecast_df)
    ).reshape(-1, 1)

    y = forecast_df[forecast_variable]

    model = LinearRegression()

    model.fit(X, y)

    future_steps = np.arange(
        len(forecast_df),
        len(forecast_df) + 12
    ).reshape(-1, 1)

    predictions = model.predict(
        future_steps
    )

    future_dates = pd.date_range(
        start=forecast_df["Month_Year"].iloc[-1],
        periods=13,
        freq="MS"
    )[1:]

    forecast_plot_df = pd.DataFrame({

        "Month_Year": future_dates,
        "Forecast": predictions
    })

    forecast_fig = px.line(
        forecast_plot_df,
        x="Month_Year",
        y="Forecast",
        markers=True
    )

    forecast_fig.update_layout(
        height=550,
        yaxis_title=f"Projected {forecast_variable}"
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption(f"""
The projection for {forecast_variable} suggests that historical transaction momentum may continue influencing future banking and payment ecosystem trends.

The forecast is intended for directional analytical understanding rather than precise predictive estimation.
""")

# ===================================================
# FOOTER
# ===================================================

st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics"
)

  
