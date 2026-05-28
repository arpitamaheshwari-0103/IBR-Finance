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

if "Month_Year" in df.columns:
    df["Month_Year"] = pd.to_datetime(df["Month_Year"])
else:
    st.error("Date column not found in dataset.")
    st.stop()


df["Year"] = df["Month_Year"].dt.year

# ======================================================
# REQUIRED COLUMN CHECK
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

st.markdown(
    "### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience"
)

st.markdown("""
<div class='insight-box'>
<h4>Core Research Framework</h4>
<p>
India is becoming digitally transactional faster than cashless.
Digital payment acceleration and cash persistence currently coexist.
</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# KPI CARDS
# ======================================================

latest_value = round(filtered_df[selected_payment].iloc[-1], 2)

start_value = filtered_df[selected_payment].iloc[0]

if start_value != 0:
    growth = round(((latest_value - start_value) / start_value) * 100, 1)
else:
    growth = 0

correlation = round(filtered_df["UPI"].corr(filtered_df["ATM"]), 2)

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
    <h4>Transformation Shift</h4>
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

    insight = "Digital transaction growth is accelerating materially faster than ATM infrastructure withdrawal."

elif research_question == "Why does cash still persist?":

    insight = "Cash persistence reflects uneven banking transition, informal transaction dependency, and infrastructure coexistence."

elif research_question == "Is ATM infrastructure still relevant?":

    insight = "ATM infrastructure remains strategically relevant due to hybrid banking behaviour across India."

elif research_question == "Has merchant digitisation accelerated?":

    insight = "QR-led merchant onboarding scaled significantly faster than traditional POS deployment."

else:

    insight = "India is becoming digitally transactional faster than cashless across the banking ecosystem."

st.markdown(f"""
<div class='insight-box'>
<h4>Structural Finding</h4>
<p>{insight}</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# PAGE 1
# ======================================================

if section == "Executive Intelligence":

    st.subheader("Payments Transformation Overview")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df["Month_Year"],
        y=filtered_df[selected_payment],
        mode="lines",
        name=selected_payment
    ))

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Key Takeaway: Banking transformation in India remains hybrid rather than fully digital."
    )

    st.subheader("Comparative Transformation Dynamics")

    compare_fig = go.Figure()

    for col in ["UPI", "ATM", "POS", "IMPS"]:
        compare_fig.add_trace(go.Scatter(
            x=filtered_df["Month_Year"],
            y=filtered_df[col],
            mode="lines",
            name=col
        ))

    compare_fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(compare_fig, use_container_width=True)

    st.markdown("""
    ### Banking Implication

    Banks may increasingly optimize physical infrastructure while reallocating strategic focus toward digital transaction ecosystems.
    """)

# ======================================================
# PAGE 2
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

# ======================================================
# PAGE 3
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
        "Key Takeaway: ATM infrastructure decline remains materially slower than digital transaction acceleration."
    )

# ======================================================
# PAGE 4
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

# ======================================================
# PAGE 5
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

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Data Sources: RBI DBIE, NPCI Transaction Statistics, Banking Infrastructure Analysis"
)
```

