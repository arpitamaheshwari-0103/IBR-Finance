
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FinTech Banking Dashboard", layout="wide")

st.title("FinTech vs Conventional Banking Dashboard")
st.markdown("### India’s Banking Transformation (2018–2026)")

df = pd.read_csv("data/payments_data.csv")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Observations", len(df))
col2.metric("Latest UPI", f"{df['UPI_Transactions'].iloc[-1]:,.0f} M")
col3.metric("Peak ATM", f"{df['ATM_Withdrawals'].max():,.0f} M")
col4.metric("UPI-ATM Correlation", round(df['UPI_Transactions'].corr(df['ATM_Withdrawals']),3))

st.markdown("---")

fig = px.line(
    df,
    x="Month_Year",
    y=["ATM_Withdrawals","UPI_Transactions"],
    title="UPI Growth vs ATM Withdrawals"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("## Strategic Insights")

st.info(
"""
• UPI growth coincides with gradual ATM withdrawal decline.

• Digital payment adoption reflects broader behavioural transformation.

• The findings suggest structural shifts in India’s banking ecosystem.
"""
)
