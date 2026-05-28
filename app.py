# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================

# PAGE CONFIG

# =========================

st.set_page_config(
page_title="India Banking Transformation Dashboard",
layout="wide",
initial_sidebar_state="expanded"
)

# =========================

# CUSTOM CSS

# =========================

st.markdown("""

<style>

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
}

.insight-box {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #3B82F6;
    margin-top: 10px;
}

.analyst-panel {
    background-color: #1F2937;
    padding: 20px;
    border-radius: 12px;
}

.small-text {
    font-size: 15px;
    line-height: 1.6;
}

</style>

""", unsafe_allow_html=True)

# =========================

# LOAD DATA

# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("payments_data.csv")
    return df

# =========================

# DATA PREP

# =========================

# Rename columns safely if required

possible_cols = {
'UPI Transactions': 'UPI',
'UPI_Transactions': 'UPI',
'ATM Withdrawals': 'ATM',
'ATM_Withdrawals': 'ATM',
'Debit Card POS Transactions': 'POS',
'DebitCard_POS': 'POS',
'IMPS Transactions': 'IMPS',
'IMPS': 'IMPS'
}

for col in list(df.columns):
if col in possible_cols:
df.rename(columns={col: possible_cols[col]}, inplace=True)

# Detect date column

for col in df.columns:
if 'Month' in col or 'Date' in col:
date_col = col
break

# Convert date

df[date_col] = pd.to_datetime(df[date_col])

df['Year'] = df[date_col].dt.year

# =========================

# SIDEBAR

# =========================

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

# Timeline Filter

min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

selected_years = st.sidebar.slider(
"Select Timeline",
min_year,
max_year,
(min_year, max_year)
)

filtered_df = df[
(df['Year'] >= selected_years[0]) &
(df['Year'] <= selected_years[1])
]

# Payment Selector

metric_options = ['UPI', 'ATM', 'POS', 'IMPS']

selected_metric = st.sidebar.selectbox(
"Select Payment System",
metric_options
)

# Research Questions

research_question = st.sidebar.selectbox(
"Ask the Research",
[
"Is UPI replacing cash?",
"Why does cash still persist?",
"Has merchant digitisation accelerated?",
"Is ATM infrastructure still relevant?",
"What is the hidden insight from the study?"
]
)

# =========================

# HEADER

# =========================

st.title("India Banking Transformation Dashboard")

st.markdown(
"### FinTech’s Contribution to Transforming Conventional Banking: The Indian Experience"
)

st.markdown(
"#### Strategic Banking Transformation & Digital Infrastructure Intelligence"
)

# =========================

# KPI SECTION

# =========================

latest_upi = round(filtered_df['UPI'].iloc[-1], 2)
latest_atm = round(filtered_df['ATM'].iloc[-1], 2)

upi_growth = round(
((filtered_df['UPI'].iloc[-1] - filtered_df['UPI'].iloc[0]) /
filtered_df['UPI'].iloc[0]) * 100,
1
)

atm_change = round(
((filtered_df['ATM'].iloc[-1] - filtered_df['ATM'].iloc[0]) /
filtered_df['ATM'].iloc[0]) * 100,
1
)

correlation = round(filtered_df['UPI'].corr(filtered_df['ATM']), 3)

col1, col2, col3, col4 = st.columns(4)

with col1:
st.markdown(f""" <div class='metric-card'> <h4>Digital Transaction Scale</h4> <h2>{latest_upi:,.0f} M</h2> <p>UPI ecosystem intensity</p> </div>
""", unsafe_allow_html=True)

with col2:
st.markdown(f""" <div class='metric-card'> <h4>Cash Infrastructure</h4> <h2>{latest_atm:,.0f} M</h2> <p>Residual ATM dependence</p> </div>
""", unsafe_allow_html=True)

with col3:
st.markdown(f""" <div class='metric-card'> <h4>Digital Adoption Growth</h4> <h2>{upi_growth}%</h2> <p>Behavioural digitisation acceleration</p> </div>
""", unsafe_allow_html=True)

with col4:
st.markdown(f""" <div class='metric-card'> <h4>UPI vs ATM Relationship</h4> <h2>{correlation}</h2> <p>Infrastructure coexistence indicator</p> </div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================

# QUESTION ENGINE

# =========================

if research_question == "Is UPI replacing cash?":
dynamic_insight = "UPI growth accelerated rapidly after 2020, but ATM withdrawals declined gradually rather than collapsing. This suggests coexistence between digital payments and cash infrastructure rather than immediate replacement."

elif research_question == "Why does cash still persist?":
dynamic_insight = "Cash persistence indicates that behavioural trust, rural accessibility, and informal transaction ecosystems still support physical currency usage despite digital convenience."

elif research_question == "Has merchant digitisation accelerated?":
dynamic_insight = "Merchant QR infrastructure scaled significantly faster than traditional POS infrastructure, enabling low-cost transaction digitisation across small businesses."

elif research_question == "Is ATM infrastructure still relevant?":
dynamic_insight = "ATM infrastructure remains relevant due to uneven digital adoption, financial inclusion gaps, and continued cash dependency in several transaction environments."

else:
dynamic_insight = "The study’s hidden insight is that India is becoming digitally transactional faster than cashless. Banking transformation is additive before fully substitutive."

st.markdown(f"""

<div class='insight-box'>
<h4>Strategic Banking Observation</h4>
<p class='small-text'>{dynamic_insight}</p>
</div>
""", unsafe_allow_html=True)

# =========================

# MAIN ANALYTICS

# =========================

left, right = st.columns(2)

with left:

```
st.subheader("Is UPI Actually Replacing Cash Usage?")

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=filtered_df[date_col],
        y=filtered_df['UPI'],
        name='UPI Transactions',
        line=dict(color='#3B82F6', width=3)
    )
)

fig1.add_trace(
    go.Scatter(
        x=filtered_df[date_col],
        y=filtered_df['ATM'],
        name='ATM Withdrawals',
        line=dict(color='#EF4444', width=3)
    )
)

fig1.update_layout(
    template='plotly_dark',
    height=420,
    paper_bgcolor='#111827',
    plot_bgcolor='#111827'
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<h4>Analyst Interpretation</h4>
<p class='small-text'>
UPI adoption accelerated after COVID-19, but ATM withdrawals declined gradually instead of collapsing.
This indicates behavioural substitution rather than complete cash elimination.
</p>
</div>
""", unsafe_allow_html=True)
```

with right:

```
st.subheader("Pre vs Post COVID Banking Behaviour")

pre_covid = filtered_df[filtered_df['Year'] < 2020]
post_covid = filtered_df[filtered_df['Year'] >= 2020]

comparison_df = pd.DataFrame({
    'Period': ['Pre-COVID', 'Post-COVID'],
    'UPI Average': [pre_covid['UPI'].mean(), post_covid['UPI'].mean()],
    'ATM Average': [pre_covid['ATM'].mean(), post_covid['ATM'].mean()]
})

fig2 = px.bar(
    comparison_df,
    x='Period',
    y=['UPI Average', 'ATM Average'],
    barmode='group',
    template='plotly_dark'
)

fig2.update_layout(
    height=420,
    paper_bgcolor='#111827',
    plot_bgcolor='#111827'
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<h4>Strategic Implication</h4>
<p class='small-text'>
Digital transaction intensity remained elevated after COVID-19, suggesting structural behavioural transformation rather than temporary adoption.
</p>
</div>
""", unsafe_allow_html=True)
```

# =========================

# SECOND ROW

# =========================

left2, right2 = st.columns(2)

with left2:

```
st.subheader("Has Merchant Digitisation Accelerated?")

fig3 = px.line(
    filtered_df,
    x=date_col,
    y='POS',
    template='plotly_dark'
)

fig3.update_layout(
    height=400,
    paper_bgcolor='#111827',
    plot_bgcolor='#111827'
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<h4>Banking Relevance</h4>
<p class='small-text'>
Merchant-side payment infrastructure scaled rapidly through QR-led digitisation, reducing dependency on expensive POS expansion.
</p>
</div>
""", unsafe_allow_html=True)
```

with right2:

```
st.subheader("UPI Relationship Analysis")

corr_df = filtered_df[['UPI', 'ATM', 'POS', 'IMPS']].corr()

fig4 = px.imshow(
    corr_df,
    text_auto=True,
    color_continuous_scale='Blues'
)

fig4.update_layout(
    height=400,
    paper_bgcolor='#111827',
    plot_bgcolor='#111827'
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<h4>Transformation Insight</h4>
<p class='small-text'>
Banking transformation in India is multi-speed and uneven. Digital acceleration coexists with persistent physical infrastructure dependence.
</p>
</div>
""", unsafe_allow_html=True)
```

# =========================

# STRATEGIC PANEL

# =========================

st.markdown("---")

st.subheader("Strategic Banking Outlook")

panel1, panel2, panel3 = st.columns(3)

with panel1:
st.markdown(""" <div class='analyst-panel'> <h4>Infrastructure Transition</h4> <p class='small-text'>
India’s banking transition remains hybrid. Physical and digital systems currently coexist rather than fully substitute one another. </p> </div>
""", unsafe_allow_html=True)

with panel2:
st.markdown(""" <div class='analyst-panel'> <h4>Merchant Ecosystem</h4> <p class='small-text'>
QR infrastructure enabled low-cost merchant digitisation and accelerated financial ecosystem integration. </p> </div>
""", unsafe_allow_html=True)

with panel3:
st.markdown(""" <div class='analyst-panel'> <h4>Future Banking Scenario</h4> <p class='small-text'>
Conventional banks may increasingly shift capital allocation from branch-heavy infrastructure toward digital transaction ecosystems. </p> </div>
""", unsafe_allow_html=True)

# =========================

# FOOTER

# =========================

st.markdown("---")

st.caption(
"Data Sources: RBI DBIE, NPCI Transaction Statistics, Banking Infrastructure Analysis"
)

