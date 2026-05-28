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
    return pd.read_csv("payments_data.csv")

df = load_data()

# ======================================================
# DATA PREP
# ======================================================

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

st.markdown(
    "#### Strategic Banking Transformation & Digital Infrastructure Intelligence"
)

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
        <h4>Selected Payment System</h4>
        <h2>{selected_payment}</h2>
        <p>Active analytical focus</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Current Scale</h4>
        <h2>{latest_value:,.0f}</h2>
        <p>Latest transaction intensity</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Growth Rate</h4>
        <h2>{growth}%</h2>
        <p>Transformation acceleration</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>UPI vs ATM Correlation</h4>
        <h2>{correlation}</h2>
        <p>Infrastructure coexistence indicator</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# DYNAMIC INSIGHT ENGINE
# ======================================================

if research_question == "Is UPI replacing cash?":

    dynamic_title = "Is UPI Actually Replacing Cash Usage?"

    dynamic_insight = """
    UPI adoption accelerated rapidly after COVID-19,
    but ATM withdrawals declined gradually rather than collapsing.
    This suggests coexistence rather than immediate cash elimination.
    """

elif research_question == "Why does cash still persist?":

    dynamic_title = "Why Does Cash Persistence Continue?"

    dynamic_insight = """
    Cash persistence reflects behavioural trust,
    rural accessibility limitations,
    and continued dependence on physical currency ecosystems.
    """

elif research_question == "Is ATM infrastructure still relevant?":

    dynamic_title = "Is ATM Infrastructure Still Relevant?"

    dynamic_insight = """
    ATM infrastructure remains relevant because
    banking transition across India remains uneven
    across regions and user groups.
    """

elif research_question == "Has merchant digitisation accelerated?":

    dynamic_title = "Has Merchant Digitisation Accelerated?"

    dynamic_insight = """
    Merchant QR infrastructure scaled significantly faster
    than traditional POS expansion,
    enabling low-cost payment digitisation.
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
            x=filtered_df[date_col],
            y=filtered_df[selected_payment],
            mode="lines+markers",
            name=selected_payment
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
    <h4>Analyst Interpretation</h4>
    <p class='small-text'>
    The selected payment system demonstrates structural transformation
    across India's banking ecosystem during the selected timeline period.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# DIGITAL PAYMENT SHIFT
# ======================================================

elif section == "Digital Payment Shift":

    st.subheader("Pre vs Post COVID Banking Behaviour")

    pre_covid = filtered_df[filtered_df["Year"] < 2020]
    post_covid = filtered_df[filtered_df["Year"] >= 2020]

    comparison_df = pd.DataFrame({
        "Period": ["Pre-COVID", "Post-COVID"],
        "Average": [
            pre_covid[selected_payment].mean(),
            post_covid[selected_payment].mean()
        ]
    })

    fig2 = px.bar(
        comparison_df,
        x="Period",
        y="Average",
        color="Period",
        template="plotly_dark"
    )

    fig2.update_layout(
        height=450,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
    <h4>Strategic Implication</h4>
    <p class='small-text'>
    The selected payment system experienced accelerated behavioural change
    after COVID-19, indicating structural digital transformation.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# CASH INFRASTRUCTURE TRANSITION
# ======================================================

elif section == "Cash Infrastructure Transition":

    st.subheader("Cash Infrastructure Persistence")

    fig3 = px.line(
        filtered_df,
        x=date_col,
        y=["ATM", "UPI"],
        template="plotly_dark"
    )

    fig3.update_layout(
        height=450,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Infrastructure Signal</h4>
    <p class='small-text'>
    Digital payment acceleration and cash infrastructure persistence
    currently coexist across India’s banking ecosystem.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# MERCHANT & INCLUSION ANALYSIS
# ======================================================

elif section == "Merchant & Inclusion Analysis":

    st.subheader("Merchant Digitisation Analysis")

    fig4 = px.area(
        filtered_df,
        x=date_col,
        y=["POS", "UPI"],
        template="plotly_dark"
    )

    fig4.update_layout(
        height=450,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <h4>Banking Relevance</h4>
    <p class='small-text'>
    Merchant-side QR infrastructure enabled low-cost ecosystem expansion
    and accelerated digital payment accessibility.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# FUTURE BANKING SCENARIOS
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
        height=450,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
    <h4>Future Banking Scenario</h4>
    <p class='small-text'>
    Future banking infrastructure may increasingly shift toward
    digitally transactional ecosystems while retaining hybrid support systems.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Data Sources: RBI DBIE, NPCI Transaction Statistics, Banking Infrastructure Analysis"
)
