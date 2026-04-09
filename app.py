import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Neuro-Quant Dashboard", layout="wide")

st.title("🧠 Neuro-Quant Trading Dashboard")
st.markdown("---")

# 2. Sidebar for Controls
st.sidebar.header("Navigation")
if st.sidebar.button("Run Live Signal"):
    st.sidebar.write("Fetching latest EUR/USD data...")
    # Later, we can link your live_signal.py logic here

# 3. Key Metrics (Visual Cards)
col1, col2, col3 = st.columns(3)

# We'll pull these from your actual backtest results later
col1.metric("Strategy Return", "11,946%", "+149%")
col2.metric("Market Return", "-11.91%", "-2.5%")
col3.metric("Bot Confidence", "52.45%", "Stable")

# 4. The Main Performance Chart
st.subheader("Interactive Performance Growth")
try:
    df = pd.read_csv("backtest_results.csv")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Bot_Performance'], name="Bot"))
    fig.add_trace(go.Scatter(x=df.index, y=df['Market_Performance'], name="Market"))
    fig.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)
except:
    st.warning("Please run a backtest first to generate data.")

st.write("Current Status: Monitoring Sell Trade @ 1.16620")