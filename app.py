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
# LOAD MAIN DATA
# ===================================================

@st.cache_data
def load_data():

    payments_df = pd.read_csv("payments_data.csv")
    payments_df["Month_Year"] = pd.to_datetime(
        payments_df["Month_Year"]
    )

    # NEW RBI DATASETS
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
    "Analytical exploration of India’s evolving payment ecosystem"
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
        "Conventional systems active"
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

    st.plotly_chart(
        overview_fig,
        use_container_width=True
    )

    st.markdown("### Analyst Observation")

    st.info("""
Digital transaction systems expanded rapidly during the observed period, while conventional banking channels continued operating at meaningful levels.

This indicates that transaction digitisation and cash dependence currently coexist within the Indian banking ecosystem.
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

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    # YoY Growth Analysis
    st.subheader("Year-over-Year Growth Analysis")

    yoy_df = filtered_df.copy()

    for variable in selected_variables:

        yoy_df[f"{variable}_YoY"] = (
            yoy_df[variable]
            .pct_change(periods=12)
        ) * 100

    yoy_columns = [
        col for col in yoy_df.columns
        if "_YoY" in col
    ]

    yoy_fig = px.line(
        yoy_df,
        x="Month_Year",
        y=yoy_columns
    )

    yoy_fig.update_layout(
        height=450,
        yaxis_title="YoY Growth (%)"
    )

    st.plotly_chart(
        yoy_fig,
        use_container_width=True
    )

    st.markdown("### Analyst Interpretation")

    st.success("""
The transaction landscape demonstrates that digital transaction growth accelerated substantially faster than conventional transaction decline.

This suggests that ecosystem expansion and behavioural adoption may currently be occurring faster than infrastructure replacement.
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

        st.info(f"""
Correlation observed between UPI transactions and {variable}: {corr_dynamic}

The relationship may reflect changing transaction behaviour patterns within India’s evolving payment ecosystem.
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
        height=550
    )

    st.plotly_chart(
        share_chart,
        use_container_width=True
    )

    # Market Share Snapshot
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

    st.markdown("### Analyst Observation")

    st.info("""
The payment ecosystem composition shifted significantly during the observed period, with UPI gradually occupying larger transaction shares.

This suggests ecosystem-wide digital integration rather than isolated platform expansion.
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

    st.markdown("### Analyst Interpretation")

    st.info("""
The rolling correlation analysis allows observation of how the interaction between digital transactions and conventional banking behaviour evolved dynamically across different periods.
""")

# ===================================================
# INFRASTRUCTURE EVOLUTION
# ===================================================

elif page == "Infrastructure Evolution":

    st.subheader("Infrastructure Evolution")

    st.info("""
Additional RBI infrastructure datasets have been integrated to support future analysis of ATM infrastructure, payment acceptance systems, and ecosystem expansion.
""")

    st.write("### Available RBI Infrastructure Data")

    infrastructure_summary = pd.DataFrame({
        "Dataset": [
            "Old_Format.csv",
            "Sheet1.csv",
            "New_Format.csv"
        ],
        "Purpose": [
            "Legacy payment system indicators",
            "Core RBI transaction structure",
            "Updated payment infrastructure indicators"
        ]
    })

    st.dataframe(
        infrastructure_summary,
        use_container_width=True
    )

    st.markdown("### Strategic Relevance")

    st.success("""
Infrastructure-level indicators can help analyse whether India’s banking transition reflects only transaction growth or deeper transformation in banking infrastructure allocation and ecosystem expansion.
""")

# ===================================================
# STRATEGIC BANKING OUTLOOK
# ===================================================

elif page == "Strategic Banking Outlook":

    st.subheader("Strategic Banking Outlook")

    # Forecasting

    forecast_df = filtered_df.copy()

    forecast_df = forecast_df.reset_index()

    X = np.arange(len(forecast_df)).reshape(-1, 1)

    y = forecast_df[forecast_variable]

    model = LinearRegression()

    model.fit(X, y)

    future_steps = np.arange(
        len(forecast_df),
        len(forecast_df) + 12
    ).reshape(-1, 1)

    predictions = model.predict(future_steps)

    future_dates = pd.date_range(
        start=forecast_df["Month_Year"].iloc[-1],
        periods=13,
        freq="M"
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

    st.markdown("### Forecast Interpretation")

    st.warning(f"""
The projection for {forecast_variable} is based on historical transaction trends observed during the selected period.

This forecast is intended for directional analytical understanding rather than precise predictive estimation.
""")

# ===================================================
# FOOTER
# ===================================================

st.markdown("---")

st.caption(
    "Source: RBI DBIE Table 45 & NPCI Monthly Statistics"
)
