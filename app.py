```python
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
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background-color: #0B1120;
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
    background-color: #172033;
    padding: 18px;
    border-radius: 14px;
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

.small-text {
    font-size: 15px;
    line-height: 1.7;
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

payment_options = ["UPI", "ATM", "POS", "IMPS"]

selected_payment = st.sidebar.selectbox(
    "Select Payment System",
    payment_options
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
<p class='small-text'>
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

observations = len(filtered_df)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Active Payment Rail</h4>
        <h2>{selected_payment}</h2>
        <p>Digital ecosystem focus indicator</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Transaction Scale</h4>
        <h2>{latest_value:,.0f}</h2>
        <p>Behavioural adoption intensity</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Transformation Shift</h4>
        <h2>{growth}%</h2>
        <p>Infrastructure transition signal</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>UPI–ATM Relationship</h4>
        <h2>{correlation}</h2>
        <p>Hybrid banking coexistence metric</p>
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
# DYNAMIC INSIGHT ENGINE
# ======================================================

if research_question == "Is UPI replacing cash?":

    dynamic_title = "Digital Adoption vs Cash Persistence"

    dynamic_insight = """
    Digital transaction growth is scaling materially faster than cash infrastructure withdrawal.
    This suggests behavioural digitisation without full cash elimination.
    """

    chart_type = "UPI_ATM"

elif research_question == "Why does cash still persist?":

    dynamic_title = "Cash Persistence Across a Digital Economy"

    dynamic_insight = """
    ATM dependence remains structurally significant despite UPI acceleration,
    indicating uneven banking transition across customer and merchant ecosystems.
    """

    chart_type = "ATM_ONLY"

elif research_question == "Is ATM infrastructure still relevant?":

    dynamic_title = "Residual Dependence on Physical Banking Infrastructure"

    dynamic_insight = """
    ATM infrastructure remains economically relevant because India's banking transition
    remains hybrid rather than fully substitutive.
    """

    chart_type = "ATM_ONLY"

elif research_question == "Has merchant digitisation accelerated?":

    dynamic_title = "Merchant-Side Payment Infrastructure Transformation"

    dynamic_insight = """
    QR-led merchant onboarding scaled faster than traditional POS expansion,
    enabling low-cost payment digitisation.
    """

    chart_type = "POS_UPI"

else:

    dynamic_title = "Hidden Transformation Dynamics"

    dynamic_insight = """
    India is becoming digitally transactional faster than cashless.
    Digital adoption and cash persistence currently coexist.
    """

    chart_type = "ALL"

st.markdown(f"""
<div class='insight-box'>
<h4>Structural Finding</h4>
<p class='small-text'>{dynamic_insight}</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# EXECUTIVE INTELLIGENCE
# ======================================================

if section == "Executive Intelligence":

    st.subheader(dynamic_title)

    fig = go.Figure()

    if chart_type == "UPI_ATM":

        fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["UPI"],
            name="UPI",
            mode="lines"
        ))

        fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["ATM"],
            name="ATM",
            mode="lines"
        ))

    elif chart_type == "ATM_ONLY":

        fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["ATM"],
            name="ATM",
            mode="lines"
        ))

    elif chart_type == "POS_UPI":

        fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["POS"],
            name="POS",
            mode="lines"
        ))

        fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df["UPI"],
            name="UPI",
            mode="lines"
        ))

    else:

        for col in ["UPI", "ATM", "POS", "IMPS"]:
            fig.add_trace(go.Scatter(
                x=filtered_df["Month_Year"],
                y=filtered_df[col],
                name=col,
                mode="lines"
            ))

    fig.update_layout(
        template="plotly_dark",
        height=520
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Key Takeaway: Banking transformation in India remains hybrid rather than fully digital."
    )

    st.markdown("""
    ### Banking Implication

    Banks may increasingly optimize physical infrastructure
    while reallocating strategic focus toward transaction ecosystems,
    merchant integration, and digital behavioural data.
    """)

# ======================================================
# DIGITAL PAYMENT SHIFT
# ======================================================

elif section == "Digital Payment Shift":

    st.subheader("Pre vs Post COVID Digital Shift")

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
        "Key Takeaway: COVID accelerated structural behavioural transformation in digital payments."
    )

    st.markdown("""
    ### Banking Implication

    Post-pandemic payment behaviour indicates durable ecosystem transformation
    rather than temporary digital adoption spikes.
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
        "Key Takeaway: Cash infrastructure withdrawal is materially slower than digital acceleration."
    )

    st.markdown("""
    ### Banking Implication

    Physical banking infrastructure may remain strategically relevant
    despite accelerating transaction digitisation.
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
        "Key Takeaway: QR-led merchant onboarding scaled faster than traditional POS deployment."
    )

    st.markdown("""
    ### Banking Implication

    Merchant payment ecosystems may increasingly determine
    transaction data ownership and customer engagement economics.
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
        name=selected_payment
    ))

    fig5.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.info(
        "Key Takeaway: India's banking future may become increasingly digital-first while retaining hybrid support systems."
    )

    st.markdown("""
    ### Banking Implication

    Future banking strategy may increasingly shift toward
    low-cost transaction ecosystems and merchant integration infrastructure.
    """)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Data Sources: RBI DBIE, NPCI Transaction Statistics, Banking Infrastructure Analysis"
)
```
