import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="India Payments Transformation Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# EXECUTIVE ALERT
# ======================================================

st.success(
    "India’s banking transformation remains hybrid: digital transaction acceleration is scaling faster than physical cash infrastructure decline."
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main {
    background-color: #0B1120;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3, h4 {
    color: white;
}

p, div, label {
    color: #D1D5DB;
}

.metric-card {
    background-color: #172033;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #2A364D;
    margin-bottom: 10px;
}

.signal-card {
    background-color: #172033;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #2A364D;
    text-align: center;
}

.insight-box {
    background-color: #172033;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #3B82F6;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():
    return pd.read_csv("payments_data.csv")

df = load_data()

# ======================================================
# COLUMN STANDARDIZATION
# ======================================================

rename_map = {}

for col in df.columns:

    if "Month" in col or "Date" in col:
        rename_map[col] = "Month_Year"

    elif "UPI" in col:
        rename_map[col] = "UPI"

    elif "ATM" in col:
        rename_map[col] = "ATM"

    elif "POS" in col:
        rename_map[col] = "POS"

    elif "IMPS" in col:
        rename_map[col] = "IMPS"

df = df.rename(columns=rename_map)

# ======================================================
# DATE PREP
# ======================================================

if "Month_Year" not in df.columns:
    st.error("Date column not found in dataset.")
    st.stop()

df["Month_Year"] = pd.to_datetime(df["Month_Year"])

df["Year"] = df["Month_Year"].dt.year

# ======================================================
# REQUIRED COLUMNS
# ======================================================

required_cols = ["UPI", "ATM"]

for col in required_cols:
    if col not in df.columns:
        st.error(f"Required column missing: {col}")
        st.stop()

if "POS" not in df.columns:
    df["POS"] = 0

if "IMPS" not in df.columns:
    df["IMPS"] = 0

# ======================================================
# NUMERIC CONVERSION
# ======================================================

numeric_cols = ["UPI", "ATM", "POS", "IMPS"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["UPI", "ATM"])

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("Research Navigation")

section = st.sidebar.radio(
    "Explore the Study",
    [
        "Executive Intelligence",
        "Digital Payment Shift",
        "Cash Infrastructure Transition",
        "Merchant Digitisation",
        "Future Banking Scenarios"
    ]
)

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

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

selected_payment = st.sidebar.selectbox(
    "Select Payment System",
    ["UPI", "ATM", "POS", "IMPS"]
)

research_question = st.sidebar.selectbox(
    "Ask the Research",
    [
        "Is UPI replacing cash?",
        "Why does cash still persist?",
        "Is ATM infrastructure still relevant?",
        "Has merchant digitisation accelerated?",
        "What is the hidden transformation insight?"
    ]
)

# ======================================================
# HEADER
# ======================================================

st.title("India Payments Transformation Intelligence")

st.markdown("""
### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience
""")

st.markdown("""
<div class='insight-box'>
<h4>Core Research Framework</h4>
<p>
India is becoming digitally transactional faster than cashless.
Digital payment acceleration and cash persistence currently coexist across the banking ecosystem.
</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# KPI SECTION
# ======================================================

latest_value = round(filtered_df[selected_payment].iloc[-1], 2)

growth = round(
    filtered_df[selected_payment].pct_change().mean() * 100,
    2
)

correlation = round(
    filtered_df["UPI"].corr(filtered_df["ATM"]),
    2
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='metric-card'>
    <h4>Payment Rail Focus</h4>
    <h2>{selected_payment}</h2>
    <p>Digital ecosystem indicator</p>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='metric-card'>
    <h4>Transaction Scale</h4>
    <h2>{latest_value:,.0f}</h2>
    <p>Behavioural adoption intensity</p>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='metric-card'>
    <h4>Digital Expansion Index</h4>
    <h2>{growth}%</h2>
    <p>Infrastructure transition signal</p>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='metric-card'>
    <h4>UPI-ATM Relationship</h4>
    <h2>{correlation}</h2>
    <p>Hybrid banking coexistence metric</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# TRANSFORMATION SIGNALS
# ======================================================

st.markdown("### Transformation Signals")

s1, s2, s3, s4 = st.columns(4)

signals = [
    ("ATM Persistence", "Incomplete cash transition"),
    ("QR Expansion", "Merchant digitisation"),
    ("UPI Scale", "Behavioural digitisation"),
    ("Hybrid Banking", "Coexistence economy")
]

for col, signal in zip([s1, s2, s3, s4], signals):

    with col:
        st.markdown(f"""
        <div class='signal-card'>
        <h4>{signal[0]}</h4>
        <p>{signal[1]}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# DYNAMIC QUESTION ENGINE
# ======================================================

if research_question == "Is UPI replacing cash?":

    dynamic_title = "Digital Adoption vs Cash Persistence"

    insight_heading = "Structural Finding"

    insight = """
    UPI transaction intensity accelerated materially faster than ATM withdrawal decline,
    indicating coexistence rather than full cash elimination.
    """

    takeaway = """
    Digital transaction growth is scaling faster than cash infrastructure withdrawal.
    """

    banking_implication = """
    Banks may increasingly optimize physical infrastructure
    while prioritizing transaction ecosystems.
    """

elif research_question == "Why does cash still persist?":

    dynamic_title = "Cash Persistence Across a Digital Economy"

    insight_heading = "Infrastructure Observation"

    insight = """
    Cash persistence reflects uneven banking transition,
    informal transaction ecosystems,
    and continued dependence on physical currency infrastructure.
    """

    takeaway = """
    ATM infrastructure remains materially relevant despite digital acceleration.
    """

    banking_implication = """
    Physical banking infrastructure may remain strategically relevant
    across hybrid banking ecosystems.
    """

elif research_question == "Is ATM infrastructure still relevant?":

    dynamic_title = "Residual Dependence on Physical Banking Infrastructure"

    insight_heading = "Strategic Signal"

    insight = """
    ATM infrastructure continues demonstrating behavioural relevance
    despite rapid payment digitisation.
    """

    takeaway = """
    Banking transition remains hybrid rather than fully substitutive.
    """

    banking_implication = """
    Banks may increasingly optimize rather than eliminate ATM infrastructure.
    """

elif research_question == "Has merchant digitisation accelerated?":

    dynamic_title = "Merchant Ecosystem Transformation"

    insight_heading = "Merchant Infrastructure Insight"

    insight = """
    QR-led merchant onboarding scaled materially faster
    than traditional POS deployment.
    """

    takeaway = """
    Merchant QR infrastructure accelerated low-cost payment digitisation.
    """

    banking_implication = """
    Merchant ecosystems may increasingly determine
    transaction data ownership and customer engagement economics.
    """

else:

    dynamic_title = "Hidden Transformation Dynamics"

    insight_heading = "Transformation Insight"

    insight = """
    India's banking transformation remains additive before fully substitutive.
    Digital adoption and cash persistence currently coexist.
    """

    takeaway = """
    India's banking transition remains multi-speed and hybrid.
    """

    banking_implication = """
    Digital acceleration does not yet imply complete infrastructure replacement.
    """

# ======================================================
# DYNAMIC INSIGHT BOX
# ======================================================

st.markdown(f"""
<div class='insight-box'>
<h4>{insight_heading}</h4>
<p>{insight}</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# EXECUTIVE INTELLIGENCE
# ======================================================

if section == "Executive Intelligence":

    st.subheader(dynamic_title)

    executive_fig = go.Figure()

    for col in ["UPI", "ATM", "POS", "IMPS"]:

        executive_fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df[col],
            mode="lines",
            name=col
        ))

    executive_fig.update_layout(
        template="plotly_dark",
        height=520
    )

    st.plotly_chart(executive_fig, use_container_width=True)

    st.info(f"Key Takeaway: {takeaway}")

    st.markdown(f"""
    ### Banking Implication

    {banking_implication}
    """)

    st.markdown("""
    ### Executive Observations

    - UPI growth accelerated structurally after COVID.
    - ATM decline remains slower than digital acceleration.
    - Merchant QR ecosystems reduced onboarding friction.
    - India's banking transition remains coexistence-driven.
    """)

# ======================================================
# DIGITAL PAYMENT SHIFT
# ======================================================

elif section == "Digital Payment Shift":

    st.subheader("Pre vs Post COVID Payment Acceleration")

    pre = filtered_df[filtered_df["Year"] < 2020]
    post = filtered_df[filtered_df["Year"] >= 2020]

    compare_df = pd.DataFrame({
        "Period": ["Pre-COVID", "Post-COVID"],
        "Average": [
            pre[selected_payment].mean(),
            post[selected_payment].mean()
        ]
    })

    fig2 = px.bar(
        compare_df,
        x="Period",
        y="Average",
        color="Period",
        template="plotly_dark"
    )

    fig2.update_layout(height=500)

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "Key Takeaway: COVID accelerated behavioural adoption of digital payment systems."
    )

    st.markdown("""
    ### Analytical Lens

    This section evaluates how payment adoption structurally accelerated
    after the pandemic across India's digital banking ecosystem.
    """)

# ======================================================
# CASH INFRASTRUCTURE TRANSITION
# ======================================================

elif section == "Cash Infrastructure Transition":

    st.subheader("ATM vs Digital Payment Coexistence")

    fig3 = px.line(
        filtered_df,
        x="Month_Year",
        y=["ATM", "UPI"],
        template="plotly_dark"
    )

    fig3.update_layout(height=500)

    st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "Key Takeaway: ATM decline remains materially slower than UPI acceleration."
    )

    corr = filtered_df[["UPI", "ATM", "POS", "IMPS"]].corr()

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    ### Analytical Lens

    This section evaluates whether digital payment growth
    is substituting or coexisting with cash infrastructure.
    """)

# ======================================================
# MERCHANT DIGITISATION
# ======================================================

elif section == "Merchant Digitisation":

    st.subheader("Merchant Ecosystem Transformation")

    fig4 = px.area(
        filtered_df,
        x="Month_Year",
        y=["POS", "UPI"],
        template="plotly_dark"
    )

    fig4.update_layout(height=500)

    st.plotly_chart(fig4, use_container_width=True)

    st.info(
        "Key Takeaway: Merchant QR infrastructure scaled faster than traditional POS systems."
    )

    st.markdown("""
    ### Analytical Lens

    This section evaluates how low-cost QR ecosystems
    accelerated merchant-side payment digitisation.
    """)

# ======================================================
# FUTURE BANKING SCENARIOS
# ======================================================

elif section == "Future Banking Scenarios":

    st.subheader("Future Banking Infrastructure Outlook")

    yearly_df = filtered_df.groupby("Year")[selected_payment].mean().reset_index()

    fig5 = go.Figure()

    fig5.add_trace(go.Scatter(
        x=yearly_df["Year"],
        y=yearly_df[selected_payment],
        mode="lines+markers",
        name="Actual"
    ))

    fig5.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig5, use_container_width=True)

    future_df = yearly_df.copy()

    future_df["Forecast"] = (
        future_df[selected_payment]
        .rolling(2)
        .mean()
    )

    forecast_fig = go.Figure()

    forecast_fig.add_trace(go.Scatter(
        x=future_df["Year"],
        y=future_df[selected_payment],
        mode="lines+markers",
        name="Actual"
    ))

    forecast_fig.add_trace(go.Scatter(
        x=future_df["Year"],
        y=future_df["Forecast"],
        mode="lines",
        name="Projected Trend"
    ))

    forecast_fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(forecast_fig, use_container_width=True)

    st.info(
        f"Key Takeaway: Future banking infrastructure may increasingly depend on {selected_payment}-driven ecosystems."
    )

    st.markdown(f"""
    ### Strategic Outlook

    This section evaluates how {selected_payment}
    may influence future digital banking infrastructure and ecosystem economics.
    """)

# ======================================================
# WHY THIS RESEARCH MATTERS
# ======================================================

st.markdown("""
### Why This Research Matters

India's banking transition represents one of the world's largest real-time payment ecosystem transformations.

The coexistence of digital acceleration and cash persistence has major implications for:
- banking strategy
- infrastructure optimization
- merchant ecosystems
- financial inclusion policy
""")

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Data Sources: RBI DBIE, NPCI Transaction Statistics, Banking Infrastructure Analysis"
)



