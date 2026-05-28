import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="India Banking Transformation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background-color: #0E1117;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3, h4 {
    color: white;
}

p, label, div {
    color: #D1D5DB;
}

.metric-card {
    background-color: #1F2937;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #374151;
    margin-bottom: 10px;
}

.insight-box {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #3B82F6;
    margin-top: 10px;
}

.small-text {
    font-size: 15px;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("payments_data.csv")
    return df

df = load_data()

# ==================================================
# DATA PREP
# ==================================================

date_col = None

for col in df.columns:
    if "Date" in col or "Month" in col:
        date_col = col
        break

df[date_col] = pd.to_datetime(df[date_col])

df["Year"] = df[date_col].dt.year

rename_map = {}

for col in df.columns:

    if "UPI" in col:
        rename_map[col] = "UPI"

    elif "ATM" in col:
        rename_map[col] = "ATM"

    elif "POS" in col:
        rename_map[col] = "POS"

    elif "IMPS" in col:
        rename_map[col] = "IMPS"

df = df.rename(columns=rename_map)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("Research Navigation")

section = st.sidebar.radio(
    "Explore the Study",
    [
        "Executive Intelligence",
        "Digital Payment Shift",
        "Cash Infrastructure Transition",
        "Merchant & Inclusion Analysis",
        "Future Banking Scenarios"
    ]
)

# Timeline filter

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Select Timeline",
    min_year,
    max_year,
    (min_year, max_year)
)

filtered_df = df[
    (df["Year"] >= selected_years[0]) &
    (df["Year"] <= selected_years[1])
]

# Payment System Selector

payment_options = ["UPI", "ATM", "POS", "IMPS"]

selected_payment = st.sidebar.selectbox(
    "Select Payment System",
    payment_options
)

# Ask the Research

research_question = st.sidebar.selectbox(
    "Ask the Research",
    [
        "Is UPI replacing cash?",
        "Why does cash still persist?",
        "Is ATM infrastructure still relevant?",
        "Has merchant digitisation accelerated?",
        "What is the hidden insight from this study?"
    ]
)

# ==================================================
# HEADER
# ==================================================

st.title("India Banking Transformation Dashboard")

st.markdown(
    "### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience"
)

st.markdown(
    "#### Strategic Banking Transformation & Digital Infrastructure Intelligence"
)

# ==================================================
# KPI SECTION
# ==================================================

latest_upi = round(filtered_df["UPI"].iloc[-1], 2)
latest_atm = round(filtered_df["ATM"].iloc[-1], 2)

upi_growth = round(
    (
        (filtered_df["UPI"].iloc[-1] - filtered_df["UPI"].iloc[0])
        / filtered_df["UPI"].iloc[0]
    ) * 100,
    1
)

correlation = round(
    filtered_df["UPI"].corr(filtered_df["ATM"]),
    3
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Digital Transaction Scale</h4>
        <h2>{latest_upi:,.0f} M</h2>
        <p>UPI ecosystem intensity</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Cash Infrastructure</h4>
        <h2>{latest_atm:,.0f} M</h2>
        <p>Residual ATM dependence</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Digital Adoption Growth</h4>
        <h2>{upi_growth}%</h2>
        <p>Behavioural digitisation acceleration</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Infrastructure Coexistence</h4>
        <h2>{correlation}</h2>
        <p>UPI vs ATM relationship</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================================================
# DYNAMIC INSIGHT ENGINE
# ==================================================

if research_question == "Is UPI replacing cash?":

    insight = """
    UPI adoption accelerated rapidly after COVID-19,
    but ATM withdrawals declined gradually rather than collapsing.
    This suggests coexistence rather than full cash elimination.
    """

elif research_question == "Why does cash still persist?":

    insight = """
    Cash persistence reflects behavioural trust, rural accessibility,
    and continued dependence on physical currency in informal ecosystems.
    """

elif research_question == "Is ATM infrastructure still relevant?":

    insight = """
    ATM infrastructure remains relevant because banking transition
    across India is uneven and financial inclusion gaps still exist.
    """

elif research_question == "Has merchant digitisation accelerated?":

    insight = """
    Merchant QR infrastructure scaled faster than traditional POS systems,
    enabling low-cost payment digitisation across small businesses.
    """

else:

    insight = """
    India is becoming digitally transactional faster than cashless.
    Digital adoption and cash persistence currently coexist.
    """

st.markdown(f"""
<div class='insight-box'>
<h4>Strategic Banking Observation</h4>
<p class='small-text'>{insight}</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# PAGE 1
# ==================================================

if section == "Executive Intelligence":

    st.subheader("Is UPI Actually Replacing Cash Usage?")

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=filtered_df[date_col],
            y=filtered_df["UPI"],
            mode="lines",
            name="UPI Transactions"
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=filtered_df[date_col],
            y=filtered_df["ATM"],
            mode="lines",
            name="ATM Withdrawals"
        )
    )

    fig1.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Analyst Interpretation</h4>
    <p class='small-text'>
    UPI growth accelerated significantly after COVID-19,
    but cash infrastructure remained persistent.
    Banking transition remains additive before fully substitutive.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PAGE 2
# ==================================================

elif section == "Digital Payment Shift":

    st.subheader("Pre vs Post COVID Banking Behaviour")

    pre_covid = filtered_df[filtered_df["Year"] < 2020]
    post_covid = filtered_df[filtered_df["Year"] >= 2020]

    comparison_df = pd.DataFrame({
        "Period": ["Pre-COVID", "Post-COVID"],
        "UPI Average": [
            pre_covid["UPI"].mean(),
            post_covid["UPI"].mean()
        ],
        "ATM Average": [
            pre_covid["ATM"].mean(),
            post_covid["ATM"].mean()
        ]
    })

    fig2 = px.bar(
        comparison_df,
        x="Period",
        y=["UPI Average", "ATM Average"],
        barmode="group",
        template="plotly_dark"
    )

    fig2.update_layout(height=450)

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Strategic Implication</h4>
    <p class='small-text'>
    Digital transaction intensity remained elevated after COVID-19,
    indicating structural behavioural transformation.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PAGE 3
# ==================================================

elif section == "Cash Infrastructure Transition":

    st.subheader("Cash Infrastructure Persistence")

    fig3 = px.line(
        filtered_df,
        x=date_col,
        y="ATM",
        template="plotly_dark"
    )

    fig3.update_layout(height=450)

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Infrastructure Signal</h4>
    <p class='small-text'>
    ATM infrastructure declined slower than digital payment acceleration,
    indicating persistent dependence on physical cash systems.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PAGE 4
# ==================================================

elif section == "Merchant & Inclusion Analysis":

    st.subheader("Has Merchant Digitisation Accelerated?")

    fig4 = px.line(
        filtered_df,
        x=date_col,
        y="POS",
        template="plotly_dark"
    )

    fig4.update_layout(height=450)

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Banking Relevance</h4>
    <p class='small-text'>
    Merchant-side digitisation scaled rapidly through QR infrastructure,
    enabling low-cost financial ecosystem expansion.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PAGE 5
# ==================================================

elif section == "Future Banking Scenarios":

    st.subheader("Future Banking Outlook")

    forecast_df = filtered_df.groupby("Year")[["UPI", "ATM"]].mean().reset_index()

    fig5 = go.Figure()

    fig5.add_trace(
        go.Scatter(
            x=forecast_df["Year"],
            y=forecast_df["UPI"],
            mode="lines+markers",
            name="UPI"
        )
    )

    fig5.add_trace(
        go.Scatter(
            x=forecast_df["Year"],
            y=forecast_df["ATM"],
            mode="lines+markers",
            name="ATM"
        )
    )

    fig5.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Future Banking Scenario</h4>
    <p class='small-text'>
    Conventional banking infrastructure may increasingly transition
    toward digital-first ecosystems while maintaining hybrid cash support.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Data Sources: RBI DBIE, NPCI Statistics, Banking Infrastructure Analysis"
)

