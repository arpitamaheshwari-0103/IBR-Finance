```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="India Banking Transformation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS
# ======================================================

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

.signal-card {
    background-color: #1F2937;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #374151;
    text-align: center;
}

.small-text {
    font-size: 15px;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():
    df = pd.read_csv("payments_data.csv")
    return df

df = load_data()

# ======================================================
# DATA PREPARATION
# ======================================================

df["Month_Year"] = pd.to_datetime(df["Month_Year"])

df["Year"] = df["Month_Year"].dt.year

df = df.rename(columns={
    "ATM_Withdrawals": "ATM",
    "UPI_Transactions": "UPI",
    "DebitCard_POS": "POS"
})

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

# Payment system selector

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

# ======================================================
# HEADER
# ======================================================

st.title("India Banking Transformation Dashboard")

st.markdown(
    "### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience"
)

st.markdown("""
<div class='insight-box'>
<h4>Core Research Framework</h4>
<p class='small-text'>
India is becoming digitally transactional faster than cashless.
Digital payment acceleration and cash persistence currently coexist.
</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# KPI SECTION
# ======================================================

latest_value = round(filtered_df[selected_payment].iloc[-1], 2)

growth = round(
    (
        (filtered_df[selected_payment].iloc[-1] -
         filtered_df[selected_payment].iloc[0])
        /
        filtered_df[selected_payment].iloc[0]
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
        <h4>Payment System Focus</h4>
        <h2>{selected_payment}</h2>
        <p>Digital ecosystem scale indicator</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Current Transaction Scale</h4>
        <h2>{latest_value:,.0f}</h2>
        <p>Behavioural digitisation signal</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Transformation Growth</h4>
        <h2>{growth}%</h2>
        <p>Infrastructure transition metric</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>UPI vs ATM Relationship</h4>
        <h2>{correlation}</h2>
        <p>Infrastructure coexistence indicator</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# TRANSFORMATION SIGNALS
# ======================================================

st.markdown("### Transformation Signals")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class='signal-card'>
    <h4>ATM Persistence</h4>
    <p>Incomplete cash transition</p>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class='signal-card'>
    <h4>QR Expansion</h4>
    <p>Merchant digitisation</p>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class='signal-card'>
    <h4>UPI Scale</h4>
    <p>Behavioural digitisation</p>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class='signal-card'>
    <h4>Hybrid Banking</h4>
    <p>Coexistence economy</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# DYNAMIC INSIGHTS
# ======================================================

if research_question == "Is UPI replacing cash?":

    dynamic_title = "Is UPI Actually Replacing Cash Usage?"

    dynamic_insight = """
    UPI accelerated rapidly after COVID-19,
    but ATM withdrawals declined gradually rather than collapsing,
    indicating coexistence rather than full replacement.
    """

elif research_question == "Why does cash still persist?":

    dynamic_title = "Why Does Cash Persistence Continue?"

    dynamic_insight = """
    Cash persistence reflects uneven infrastructure transition,
    behavioural trust in currency,
    and continued reliance on informal transaction systems.
    """

elif research_question == "Is ATM infrastructure still relevant?":

    dynamic_title = "Is ATM Infrastructure Still Relevant?"

    dynamic_insight = """
    ATM infrastructure remains relevant due to hybrid banking behaviour,
    financial inclusion gaps,
    and persistent cash dependency.
    """

elif research_question == "Has merchant digitisation accelerated?":

    dynamic_title = "Has Merchant Digitisation Accelerated?"

    dynamic_insight = """
    Merchant QR infrastructure expanded significantly faster
    than traditional POS systems,
    accelerating low-cost payment digitisation.
    """

else:

    dynamic_title = "What Is the Hidden Insight From the Study?"

    dynamic_insight = """
    India is becoming digitally transactional faster than cashless.
    Digital adoption and cash persistence currently coexist.
    """

st.markdown(f"""
<div class='insight-box'>
<h4>Strategic Banking Observation</h4>
<p class='small-text'>{dynamic_insight}</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# EXECUTIVE INTELLIGENCE
# ======================================================

if section == "Executive Intelligence":

    st.subheader(dynamic_title)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df[selected_payment],
            mode="lines+markers",
            name=selected_payment
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Key Takeaway: Digital transaction adoption accelerated faster than physical infrastructure withdrawal."
    )

    st.markdown("""
    ### Comparative Transformation Analysis
    """)

    compare_fig = go.Figure()

    compare_fig.add_trace(
        go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["UPI"],
            name="UPI"
        )
    )

    compare_fig.add_trace(
        go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["ATM"],
            name="ATM"
        )
    )

    compare_fig.add_trace(
        go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["POS"],
            name="POS"
        )
    )

    compare_fig.add_trace(
        go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["IMPS"],
            name="IMPS"
        )
    )

    compare_fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(compare_fig, use_container_width=True)

    st.markdown("""
    ### Why This Matters

    Banks may increasingly shift from branch-heavy infrastructure
    toward low-cost digital transaction ecosystems.
    """)

# ======================================================
# DIGITAL PAYMENT SHIFT
# ======================================================

elif section == "Digital Payment Shift":

    st.subheader("Pre vs Post COVID Banking Behaviour")

    pre = filtered_df[filtered_df["Year"] < 2020]
    post = filtered_df[filtered_df["Year"] >= 2020]

    comparison_df = pd.DataFrame({
        "Period": ["Pre-COVID", "Post-COVID"],
        "Average": [
            pre[selected_payment].mean(),
            post[selected_payment].mean()
        ]
    })

    fig2 = px.bar(
        comparison_df,
        x="Period",
        y="Average",
        color="Period",
        template="plotly_dark"
    )

    fig2.update_layout(height=500)

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "Key Takeaway: COVID accelerated structural behavioural transformation in digital transactions."
    )

    st.markdown("""
    ### Why This Matters

    Digital payment systems became embedded into everyday banking behaviour
    rather than remaining temporary adoption trends.
    """)

# ======================================================
# CASH INFRASTRUCTURE
# ======================================================

elif section == "Cash Infrastructure Transition":

    st.subheader("Cash Infrastructure Persistence")

    fig3 = px.line(
        filtered_df,
        x="Month_Year",
        y=["ATM", "UPI"],
        template="plotly_dark"
    )

    fig3.update_layout(height=500)

    st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "Key Takeaway: Cash infrastructure declined slower than digital payment acceleration."
    )

    st.markdown("""
    ### Why This Matters

    Banking infrastructure transition remains hybrid rather than fully substitutive.
    """)

# ======================================================
# MERCHANT ANALYSIS
# ======================================================

elif section == "Merchant & Inclusion Analysis":

    st.subheader("Merchant Digitisation Analysis")

    fig4 = px.area(
        filtered_df,
        x="Month_Year",
        y=["POS", "UPI"],
        template="plotly_dark"
    )

    fig4.update_layout(height=500)

    st.plotly_chart(fig4, use_container_width=True)

    st.info(
        "Key Takeaway: Merchant QR expansion scaled faster than traditional POS deployment."
    )

    st.markdown("""
    ### Why This Matters

    QR-led infrastructure enabled low-cost merchant onboarding
    and accelerated digital ecosystem penetration.
    """)

# ======================================================
# FUTURE SCENARIOS
# ======================================================

elif section == "Future Banking Scenarios":

    st.subheader("Future Banking Outlook")

    yearly_df = filtered_df.groupby("Year")[selected_payment].mean().reset_index()

    fig5 = go.Figure()

    fig5.add_trace(
        go.Scatter(
            x=yearly_df["Year"],
            y=yearly_df[selected_payment],
            mode="lines+markers",
            name=selected_payment
        )
    )

    fig5.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.info(
        "Key Takeaway: Future banking ecosystems may become increasingly digital-first while retaining hybrid support systems."
    )

    st.markdown("""
    ### Why This Matters

    Conventional banks may increasingly allocate infrastructure investment
    toward digital transaction ecosystems and merchant integration layers.
    """)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Data Sources: RBI DBIE, NPCI Transaction Statistics, Banking Infrastructure Analysis"
)
```
