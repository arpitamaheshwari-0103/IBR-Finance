import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="FinTech Banking Dashboard",
    layout="wide"
)

# Title
st.title("FinTech vs Conventional Banking Dashboard")
st.markdown("### India’s Banking Transformation (2018–2026)")

# Load Data
df = pd.read_csv("payments_data.csv")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Observations",
    len(df)
)

col2.metric(
    "Latest UPI Transactions",
    f"{df['UPI_Transactions'].iloc[-1]:,.0f} M"
)

col3.metric(
    "Peak ATM Withdrawals",
    f"{df['ATM_Withdrawals'].max():,.0f} M"
)

col4.metric(
    "UPI-ATM Correlation",
    round(df['UPI_Transactions'].corr(df['ATM_Withdrawals']), 3)
)

st.markdown("---")

# Main Trend Chart
fig = px.line(
    df,
    x="Month_Year",
    y=["UPI_Transactions", "ATM_Withdrawals"],
    title="UPI Growth vs ATM Withdrawal Decline",
    markers=True
)

fig.update_layout(
    xaxis_title="Month-Year",
    yaxis_title="Transactions (Million)",
    legend_title="Variables",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Correlation Heatmap
st.markdown("## Correlation Analysis")

corr_df = df[
    ["UPI_Transactions", "ATM_Withdrawals", "DebitCard_POS", "IMPS"]
].corr()

heatmap = px.imshow(
    corr_df,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Correlation Matrix"
)

st.plotly_chart(heatmap, use_container_width=True)

# Strategic Insights
st.markdown("## Strategic Insights")

st.info("""
• UPI growth coincides with gradual ATM withdrawal decline.

• The findings suggest structural transformation in India’s banking ecosystem.

• Digital substitution appears measurable but inelastic, indicating that cash usage still maintains a structural floor.

• The data suggests that banking infrastructure may gradually shift from physical cash infrastructure toward digital transaction ecosystems.
""")

# Future Scope
st.markdown("## Future Scope & Ecosystem Factors")

st.write("""
Potential external factors influencing the transformation:

- Smartphone penetration
- Internet accessibility
- Merchant QR adoption
- Financial literacy
- Rural vs urban transaction behaviour
- Government digital infrastructure initiatives
- Post-COVID behavioural changes
""")

# Footer
st.markdown("---")
st.caption("Source: RBI DBIE Table 45 & NPCI Monthly Statistics")
