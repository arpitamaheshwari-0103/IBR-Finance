import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="India Banking Transformation Dashboard",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    payments_df = pd.read_csv("payments_data.csv")

    payments_df["Month_Year"] = pd.to_datetime(
        payments_df["Month_Year"]
    )

    # Optional RBI infrastructure files
    old_format = pd.read_csv("Old_Format.csv")
    sheet1 = pd.read_csv("Sheet1.csv")
    new_format = pd.read_csv("New_Format.csv")

    return payments_df, old_format, sheet1, new_format


payments_df, old_format, sheet1, new_format = load_data()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Banking Transformation Navigator")

page = st.sidebar.radio(
    "Select Analytical Section",
    [
        "Transformation Overview",
        "Transaction Landscape",
        "Payment Behaviour Dynamics",
        "Digital Ecosystem Shift",
        "Transition Momentum",
        "Structural Transformation Indicators",
        "Strategic Banking Outlook"
    ]
)

st.sidebar.markdown("---")

# -----------------------------------------------------
# FILTERS
# -----------------------------------------------------

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
    "Select Payment Systems",
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
    "Analyse UPI Relationship With",
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
    "Forecast Payment System",
    [
        "UPI_Transactions",
        "ATM_Withdrawals",
        "DebitCard_POS",
        "IMPS"
    ]
)

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = payments_df[
    (payments_df["Month_Year"].dt.year >= year_range[0]) &
    (payments_df["Month_Year"].dt.year <= year_range[1])
]

# =====================================================
# HEADER
# =====================================================

st.title("India Banking Transformation Dashboard")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.caption("""
Interactive analytical exploration of India’s evolving banking and payment ecosystem
""")

st.markdown("---")

# =====================================================
# KPI SECTION
# =====================================================

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
        "Digital adoption accelerating"
    )

with col2:

    st.metric(
        "Cash Infrastructure Persistence",
        f"{atm_change}%",
        "Cash ecosystem still active"
    )

with col3:

    st.metric(
        "Payment Behaviour Correlation",
        corr_value,
        "Digital–cash coexistence"
    )

with col4:

    st.metric(
        "Research Coverage",
        len(filtered_df),
        "Monthly observations"
    )

st.markdown("---")

# =====================================================
# 1. TRANSFORMATION OVERVIEW
# =====================================================

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

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
India’s transaction ecosystem is becoming digitally intensive faster than it is becoming cash-independent.

The findings suggest coexistence between digital expansion and residual dependence on conventional banking infrastructure.
""")

# =====================================================
# 2. TRANSACTION LANDSCAPE
# =====================================================

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

    # -------------------------------------------------
    # PERFORMANCE SNAPSHOT
    # -------------------------------------------------

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

            "Payment System": variable,

            "Latest Value (Million)": round(
                latest,
                2
            ),

            "YoY Change (%)": yoy,

            "Trend Direction": trend
        })

    snapshot_df = pd.DataFrame(snapshot)

    st.dataframe(
        snapshot_df,
        use_container_width=True
    )

    # -------------------------------------------------
    # DYNAMIC INSIGHT
    # -------------------------------------------------

    top_growth = snapshot_df.sort_values(
        by="YoY Change (%)",
        ascending=False
    ).iloc[0]

    weakest = snapshot_df.sort_values(
        by="YoY Change (%)"
    ).iloc[0]

    st.markdown("### Key Strategic Takeaway")

    st.caption(f"""
{top_growth['Payment System']} currently demonstrates the strongest ecosystem momentum, while {weakest['Payment System']} reflects relatively weaker transaction acceleration.

This suggests that India’s banking transition is occurring unevenly across transaction channels rather than through uniform substitution.
""")

# =====================================================
# 3. PAYMENT BEHAVIOUR DYNAMICS
# =====================================================

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
                "The observed inverse relationship suggests "
                "that digital adoption may be substituting "
                "certain conventional banking behaviours."
            )

        elif corr_dynamic > 0.5:

            insight = (
                "The positive relationship suggests broader "
                "transaction ecosystem expansion rather than "
                "pure replacement effects."
            )

        else:

            insight = (
                "The moderate relationship suggests coexistence "
                "between digital and conventional transaction systems."
            )

        st.markdown("### Key Strategic Takeaway")

        st.caption(insight)

# =====================================================
# 4. DIGITAL ECOSYSTEM SHIFT
# =====================================================

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

    # -------------------------------------------------
    # MARKET SHARE TABLE
    # -------------------------------------------------

    latest = share_df.iloc[-1]

    market_share = pd.DataFrame({

        "Payment System": [
            "UPI",
            "ATM",
            "POS",
            "IMPS"
        ],

        "Current Market Share (%)": [
            round(latest["UPI Share"], 2),
            round(latest["ATM Share"], 2),
            round(latest["POS Share"], 2),
            round(latest["IMPS Share"], 2)
        ]
    })

    st.subheader("Current Payment Ecosystem Composition")

    st.dataframe(
        market_share,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
The ecosystem composition suggests that India’s transaction transformation is increasingly platform-centric, with UPI gradually dominating transaction share while conventional channels remain operationally relevant.
""")

# =====================================================
# 5. TRANSITION MOMENTUM
# =====================================================

elif page == "Transition Momentum":

    st.subheader("Transition Momentum")

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

    # -------------------------------------------------
    # COVID SNAPSHOT
    # -------------------------------------------------

    st.subheader("Pre vs Post COVID Comparison")

    pre_covid = filtered_df[
        filtered_df["Month_Year"] < "2020-03-01"
    ]

    post_covid = filtered_df[
        filtered_df["Month_Year"] >= "2020-03-01"
    ]

    comparison_table = pd.DataFrame({

        "Metric": [
            "Average UPI Transactions (Million)",
            "Average ATM Withdrawals (Million)"
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
The post-COVID transaction environment reflects a structural behavioural shift rather than a temporary digital adoption spike.

Digital transaction intensity remained permanently elevated even after mobility restrictions ended.
""")

# =====================================================
# 6. STRUCTURAL TRANSFORMATION INDICATORS
# =====================================================

elif page == "Structural Transformation Indicators":

    st.subheader("Structural Transformation Indicators")

    transformation_table = pd.DataFrame({

        "Observed Pattern": [

            "UPI acceleration",

            "ATM persistence",

            "POS ecosystem growth",

            "Cash activity stability",

            "Platform dominance"

        ],

        "Structural Meaning": [

            "Consumer behavioural digitisation",

            "Incomplete infrastructure transition",

            "Merchant-side digitisation",

            "Residual cash dependency",

            "Network-effect driven ecosystem expansion"
        ]
    })

    st.dataframe(
        transformation_table,
        use_container_width=True
    )

    transformation_chart = px.bar(
        transformation_table,
        x="Observed Pattern",
        y=[1, 1, 1, 1, 1]
    )

    transformation_chart.update_layout(
        height=450,
        showlegend=False,
        yaxis_visible=False
    )

    st.plotly_chart(
        transformation_chart,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption("""
The findings suggest that India’s banking transformation is not merely digital payment growth.

Instead, the data reflects behavioural, infrastructural, and ecosystem-level transition occurring at different speeds across the financial system.
""")

# =====================================================
# 7. STRATEGIC BANKING OUTLOOK
# =====================================================

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

    # -------------------------------------------------
    # HISTORICAL DATA
    # -------------------------------------------------

    historical = pd.DataFrame({

        "Month_Year": forecast_df["Month_Year"],

        "Value": forecast_df[forecast_variable],

        "Type": "Historical"
    })

    # -------------------------------------------------
    # FORECAST DATA
    # -------------------------------------------------

    forecast_future = pd.DataFrame({

        "Month_Year": future_dates,

        "Value": predictions,

        "Type": "Projected"
    })

    combined_forecast = pd.concat([
        historical,
        forecast_future
    ])

    forecast_fig = px.line(
        combined_forecast,
        x="Month_Year",
        y="Value",
        color="Type",
        markers=True
    )

    forecast_fig.update_layout(
        height=550,
        yaxis_title=f"{forecast_variable}"
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True
    )

    st.markdown("### Key Strategic Takeaway")

    st.caption(f"""
The projection for {forecast_variable} suggests that transaction digitisation may continue expanding faster than conventional banking infrastructure withdrawal.

This indicates that India’s banking ecosystem may experience prolonged coexistence between digital and legacy transaction systems.
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption("""
Source: RBI DBIE Table 45 & NPCI Monthly Statistics
""")
